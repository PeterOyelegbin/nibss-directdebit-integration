from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions
from datetime import datetime
from requests.exceptions import RequestException
from asgiref.sync import sync_to_async
import logging, requests


# Get the email and general error logger
email_logger = logging.getLogger('email_logger')
general_logger = logging.getLogger('general_logger')


BILLER_ID='455'

# Permission that checks if the user's role is allowed. It reads allowed_roles from the view.
class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_roles = getattr(view, 'allowed_roles', [])
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) in allowed_roles
        )
    

# Async function to create audit log entry
async def log_audit_event(user, action, details):
    from accounts.models import AuditLog  # Local import to avoid circular imports
    try:
        await sync_to_async(AuditLog.objects.create)(
            user=user, action=action, details=details
        )
    except Exception as e:
        await sync_to_async(general_logger.error)(f"Failed to create audit log: {str(e)}")


# Asynchronous email sending
def send_async_email(subject, message, recipient_list):
    try:
        email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        email.send()
    except Exception as e:
        email_logger.error(f"Error sending email: {e}")
        

# Format date
def format_date(date):
    return date.isoformat() if isinstance(date, datetime) else date


timeout = int(settings.API_REQUEST_TIMEOUT)


# Request API Token
def request_api_token():
    """
    Retrieves an API token from cache if available; otherwise fetches a new one from NIBSS API.
    Automatically caches the token with proper expiry handling.
    """
    if cached_token := cache.get('token_key'):
        general_logger.info("Using cached API token")
        return cached_token

    url = "https://api.nibss-plc.com.ng/v2/reset"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*", "apikey": settings.API_KEY}
    payload = {
        "grant_type": "client_credentials",
        "client_secret": settings.CLIENT_SECRET,
        "client_Id": settings.CLIENT_ID,
        "scope": settings.SCOPE,
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        # Validate token response
        token = data.get("access_token")
        expires_in = int(data.get("expires_in", 3600))
        if not token:
            raise RequestException("API did not return an access token")

        # Set cache expiry to 5 mins before actual expiry for safety
        cache_timeout = max(expires_in - 300, 60)
        cache.set("token_key", token, timeout=cache_timeout)
        general_logger.info(f"New API token obtained, expires in {cache_timeout}s")
        return token
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error fetching API token: {e.response.text}"
        general_logger.error(error_msg)
        raise RequestException(error_msg)
    except requests.exceptions.Timeout:
        general_logger.error("API token request timed out")
        raise RequestException("Token request timed out")
    except Exception as e:
        general_logger.error(f"Unexpected error fetching API token: {e}")
        raise RequestException(str(e))
    

# Make API request function
def make_api_request(method: str, endpoint: str, payload=None, params=None, files=None):
    """
    Makes an API request to the NIBSS endpoint using Bearer token authentication.
    Supports GET, POST, PUT and file uploads.
    """
    try:
        token = request_api_token()
    except RequestException as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    url = f"https://api.nibss-plc.com.ng/{endpoint.lstrip('/')}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        general_logger.info(f"Making API request: {method.upper()} {url}")
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, headers=headers, data=payload, files=files, timeout=timeout)
            else:
                response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=payload, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        # Raise exception for 4xx & 5xx responses
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        try:
            error_message = response.json().get("message", "HTTP error")
        except Exception:
            error_message = str(e)
        general_logger.error(f"API request failed: {error_message}")
        return Response({"status": "error", "message": error_message}, status=response.status_code)
    except requests.exceptions.Timeout:
        general_logger.error(f"API request timed out for {url}")
        return Response({"status": "error", "message": "Request timed out"}, status=504)
    except Exception as e:
        general_logger.error(f"Unexpected API request error: {e}")
        return Response({"status": "error", "message": str(e)}, status=500)
    