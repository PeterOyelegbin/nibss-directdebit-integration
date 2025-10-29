from rest_framework import views, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from requests.exceptions import RequestException
from django.db import transaction
from .models import *
from accounts.models import Role
from .serializers import *
from utils import IsAuthorized, format_date, request_api_token, make_api_request, log_audit_event, general_logger
import asyncio


class ChoicesView(views.APIView):
    serializer_class = None

    def get(self, request):
        data = {
            "branches": dict(Branch.choices),
            "roles": dict(Role.choices),
            "bank_codes": dict(BankCode.choices),
            "mandate_types": dict(MandateType.choices),
            "frequencies": dict(Frequency.choices),
            "mandate_status": dict(MandateStatus.choices),
            "biller_status": dict(BillerStatus.choices),
            "workflow_status": dict(WorkflowStatus.choices),
        }
        return Response(data)
    

class CreateBillerView(generics.GenericAPIView):
    """
        Biller Management Endpoint

        Create biller for mandate management
    """
    serializer_class = CreateBillerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=CreateBillerSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="POST", endpoint="ndd/api/Biller/CreateBiller", payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'CREATE BILLER',
                details=f'Created biller named {res.get("data", {"billerName"})}'
            ))
            return Response({"status": "success", "message": "Biller created successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to create biller: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateBillerView(generics.GenericAPIView):
    """
        Biller Management Endpoint

        Update biller details
    """
    serializer_class = UpdateBillerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=UpdateBillerSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="PUT", endpoint="ndd/api/Biller/UpdateBillerDetails", payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'UPDATE BILLER',
                details=f'Updated biller details for {res.get("data", {"name"})}'
            ))
            return Response({"status": "success", "message": "Biller updated successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to update biller: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateProductView(generics.GenericAPIView):
    """
        Product Management Endpoint

        Create product for mandate initiation
    """
    serializer_class = CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=CreateProductSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="POST", endpoint="ndd/api/Biller/CreateProduct", payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'CREATE PRODUCT',
                details=f'Created product named {res.get("data", {"name"})}'
            ))
            return Response({"status": "success", "message": "Product created successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to create product: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetProductView(views.APIView):
    """
        Product Management Endpoint

        Retrieve created products
    """
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def get(self, request, *args, **kwargs):
        try:
            response = make_api_request(method="GET", endpoint="ndd/api/Biller/GetProduct/455")
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            return Response({"status": "success", "message": "Products fetched successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to fetch product: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DisableProductView(generics.GenericAPIView):
    """
        Product Management Endpoint

        Disable created product
    """
    serializer_class = DisableProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=DisableProductSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="POST", endpoint=f"ndd/api/Biller/DisableProduct/455/{data.get('productID')}")
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'DISABLE PRODUCT',
                details=f'Disabled product named {res.get("data", {"name"})}'
            ))
            return Response({"status": "success", "message": "Product disabled successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to disable product: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateMandateView(generics.CreateAPIView):
    """
        Mandate Management Endpoint

        Initiate paper based direct debit mandate for customer
    """
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO', 'IT']
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=CreateMandateSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            api_payload = serializer.validated_data
            db_payload = api_payload.copy()
            api_payload['startDate'] = format_date(api_payload.get('startDate'))
            api_payload['endDate'] = format_date(api_payload.get('endDate'))
            api_payload.pop("branch", None)
            # Handle file upload
            file = api_payload.pop('mandateImageFile', None)
            if not file:
                return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Prepare payload for file upload
            file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
            response = make_api_request(
                method="POST",
                endpoint="ndd/api/MandateRequest/CreateMandateDirectDebit",
                payload=api_payload,
                files=file_upload,
            )
            if isinstance(response, Response) and response.status_code >= 400:
                general_logger.error(f"Failed to create papaer mandate: {response.data}")
                return response
            
            # Parse API response safely
            try:
                res = response.json().get("data")
                if not res or "mandateCode" not in res:
                    general_logger.error(f"Invalid API response: {response.text}")
                    return Response({"status": "error", "message": "Invalid API response"}, status=status.HTTP_502_BAD_GATEWAY)
            except Exception as parse_err:
                general_logger.error(f"Failed to parse API response: {parse_err}")
                return Response({"status": "error", "message": "Failed to parse API response"}, status=status.HTTP_502_BAD_GATEWAY)
            
            # Persist data into DB atomically
            try:
                db_payload['mandateCode'] = res['mandateCode']
                fields_to_remove = ["billerId", "bankCode", "mandateType", "payerAddress", "frequency", "narration", "mandateImageFile"]
                for field in fields_to_remove:
                    db_payload.pop(field, None)
                with transaction.atomic():
                    Mandate.objects.create(**db_payload)
            except Exception as db_err:
                general_logger.error(f"Database error: {db_err}")
                return Response({"status": "error", "message": "Failed to save mandate in database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Log audit event asynchronously
            asyncio.run(log_audit_event(
                user=request.user,
                action="CREATE PAPER MANDATE",
                details=f"Created paper mandate for {api_payload.get('accountNumber')} - {api_payload.get('payerName')}"
            ))
            return Response({"status": "success", "message": "Paper mandate created successfully", "data": res}, status=response.status_code)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BalanceEnquiryView(generics.GenericAPIView):
    """
        Mandate Management Endpoint

        Initiate paper based balance enquiry mandate for customer
    """
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO']
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=CreateMandateSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            api_payload = serializer.validated_data
            db_payload = api_payload.copy()
            api_payload['startDate'] = format_date(api_payload.get('startDate'))
            api_payload['endDate'] = format_date(api_payload.get('endDate'))
            api_payload.pop("branch", None)
            # Handle file upload
            file = api_payload.pop('mandateImageFile', None)
            if not file:
                return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Prepare payload for file upload
            file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
            response = make_api_request(
                method="POST",
                endpoint="ndd/api/MandateRequest/CreateMandateBalanceEnquiry",
                payload=api_payload,
                files=file_upload,
            )
            if isinstance(response, Response) and response.status_code >= 400:
                general_logger.error(f"Failed to create balance enquiry mandate: {response.data}")
                return response
            
            # Parse API response safely
            try:
                res = response.json().get("data")
                if not res or "mandateCode" not in res:
                    general_logger.error(f"Invalid API response: {response.text}")
                    return Response({"status": "error", "message": "Invalid API response"}, status=status.HTTP_502_BAD_GATEWAY)
            except Exception as parse_err:
                general_logger.error(f"Failed to parse API response: {parse_err}")
                return Response({"status": "error", "message": "Failed to parse API response"}, status=status.HTTP_502_BAD_GATEWAY)
            
            # Persist data into DB atomically
            try:
                db_payload['mandateCode'] = res['mandateCode']
                fields_to_remove = ["billerId", "bankCode", "mandateType", "payerAddress", "frequency", "narration", "mandateImageFile"]
                for field in fields_to_remove:
                    db_payload.pop(field, None)
                with transaction.atomic():
                    Mandate.objects.create(**db_payload)
            except Exception as db_err:
                general_logger.error(f"Database error: {db_err}")
                return Response({"status": "error", "message": "Failed to save balance enquiry mandate in database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Log audit event asynchronously
            asyncio.run(log_audit_event(
                user=request.user,
                action="INITIATE BALANCE ENQUIRY MANDATE",
                details=f"Initiated balance enquiry mandate for {api_payload.get('accountNumber')} - {api_payload.get('payerName')}"
            ))
            return Response({"status": "success", "message": "Balance enquiry initiated successfully", "data": res}, status=response.status_code)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CreateEMandateView(generics.GenericAPIView):
    """
        Mandate Management Endpoint

        Intiate E-mandate direct debit or balance enquiry for customer
    """
    serializer_class = EMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO', 'IT']
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=EMandateSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            api_payload = serializer.validated_data
            db_payload = api_payload.copy()
            api_payload['startDate'] = format_date(api_payload.get('startDate'))
            api_payload['endDate'] = format_date(api_payload.get('endDate'))
            api_payload.pop("branch", None)
            response = make_api_request(method="POST", endpoint="ndd/api/MandateRequest/CreateEmandate", payload=api_payload)
            if isinstance(response, Response) and response.status_code >= 400:
                general_logger.error(f"Failed to create e-mandate: {response.data}")
                return response
            
            # Parse API response safely
            try:
                res = response.json().get("data")
                if not res or "mandateCode" not in res:
                    general_logger.error(f"Invalid API response: {response.text}")
                    return Response({"status": "error", "message": "Invalid API response"}, status=status.HTTP_502_BAD_GATEWAY)
            except Exception as parse_err:
                general_logger.error(f"Failed to parse API response: {parse_err}")
                return Response({"status": "error", "message": "Failed to parse API response"}, status=status.HTTP_502_BAD_GATEWAY)
            
            # Persist data into DB atomically
            try:
                db_payload['mandateCode'] = res['mandateCode']
                fields_to_remove = ["billerId", "bankCode", "mandateType", "payerAddress", "frequency", "narration"]
                for field in fields_to_remove:
                    db_payload.pop(field, None)
                with transaction.atomic():
                    Mandate.objects.create(**db_payload)
            except Exception as db_err:
                general_logger.error(f"Database error: {db_err}")
                return Response({"status": "error", "message": "Failed to save mandate in database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Log audit event asynchronously
            asyncio.run(log_audit_event(
                user=request.user,
                action="CREATE E-MANDATE",
                details=f"Created e-mandate for {api_payload.get('accountNumber')} - {api_payload.get('payerName')}"
            ))
            return Response({"status": "success", "message": "Mandate created successfully", "data": res}, status=response.status_code)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MandateStatusView(generics.GenericAPIView):
    """
        Mandate Management Endpoint

        View mandate status created for customer
    """
    serializer_class = MandateStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    @swagger_auto_schema(request_body=MandateStatusSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mandate_code = serializer.validated_data["mandate_code"]
        try:
            response = make_api_request(method="POST", endpoint=f"ndd/api/MandateRequest/MandateStatus?MandateCode={mandate_code}")
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            return Response({"status": "success", "message": "Mandate status fetched successfully", "data": res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to fetch mandate status: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateMandateStatusView(generics.GenericAPIView):
    """
        Mandate Management Endpoint

        Update mandate status created for customer
    """
    serializer_class = UpdateMandateStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CREDIT', 'IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=UpdateMandateStatusSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="POST", endpoint=f"ndd/api/MandateRequest/UpdateMandateStatus", payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'UPDATE MANDATE STATUS',
                details=f'Updated mandate for {data.get("mandateCode")} - {data.get("accountNumber")} to {data.get("status")}'
            ))
            return Response({'status': 'success', 'message': 'Mandate status updated successfully', 'data': res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to update mandate status: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProcessMandateView(generics.GenericAPIView):
    serializer_class = ProcessMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CREDIT', 'IT']
    parser_classes = [JSONParser,]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            response = make_api_request(method="POST", endpoint=f"ndd/api/MandateRequest/BillerProcesMandate", payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            asyncio.run(log_audit_event(
                user=request.user,
                action=f'PROCESS MANDATE',
                details=f'Mandate code {data.get("mandateCode")} processed to {data.get("workflowStatus")}'
            ))
            return Response({'status': 'success', 'message': 'Mandate processed successfully', 'data': res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Failed to process mandate: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FetchMandateView(generics.GenericAPIView):
    serializer_class = FetchMandateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=FetchMandateSerializer, responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            endpoint="ndd/api/MandateRequest/FetchMandate/1/20"
            # endpoint="ndd/api/MandateRequest/FetchMandate?page=1&pageSize=20"
            response = make_api_request(method="POST", endpoint=endpoint, payload=data)
            # If make_api_request returned a DRF Response, return it directly
            if isinstance(response, Response):
                return response
            res = response.json()
            return Response({'status': 'success', 'message': 'Mandate fetched successfully', 'data': res.get("data", {})}, status=response.status_code)
        except RequestException as e:
            # Handles token and HTTP request-related issues
            error_msg = f"Mandate fetch request failed: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            error_msg = f"Server error: {str(e)}"
            general_logger.error(error_msg)
            return Response({"status": "error", "message": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAPIKeyView(views.APIView):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']

    def get(self, request, *args, **kwargs):
        try:
            response = request_api_token()
            return Response({'status': 'success', 'message': 'Fetched key successfully', 'token': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MandateListView(generics.GenericAPIView):
    """
        Mandate Management Endpoint

        Retrieve all created mandate
    """
    serializer_class = DBMandateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200:'OK', 401:'UNAUTHORIZED', 403:'FORBIDDEN', 500:'SERVER ERROR', 502:'BAD GATEWAY'})
    def get(self, request, *args, **kwargs):
        try:
            queryset = Mandate.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'status': 'success', 'message': 'Fetched created mandate successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        