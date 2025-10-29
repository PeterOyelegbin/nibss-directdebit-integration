from rest_framework import views, generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordRequestToken
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from threading import Thread
from utils import IsAuthorized, log_audit_event, send_async_email, general_logger
from .models import Role, UserModel
from .serializers import *
import asyncio


# Create your views here.
class RoleChoicesView(views.APIView):
    serializer_class = None
    def get(self, request):
        return Response(dict(Role.choices))
    

class UserListCreateView(generics.ListCreateAPIView):
    """
        User Management Endpoint

        List, or add users
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=UserSerializer, responses={200: 'OK', 401: 'UNAUTHORIZED', 500:'SERVER ERROR'})
    def list(self, request, *args, **kwargs):
        # Users List Endpoint
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({'status': 'success', 'message': 'Users retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except (Exception, ObjectDoesNotExist) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=UserSerializer, responses={201: 'CREATED', 401: 'UNAUTHORIZED', 400: 'BAD REQUEST', 500:'SERVER ERROR'})
    def create(self, request, *args, **kwargs):
        # Users Signup Endpoint
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            email_subject = 'Alert Group Direct Debit: User Created'
            email_boby = f"""Dear {data['first_name']} {data['last_name']},\n
            You have been created successfully on the ALERT GROUP Direct Debit platform. Your default password is {data['password']}.\n\n
            Kindly click forget password to change the default password.\n\n
            Regards,\n
            Alert Group Direct Debit\n
            https://ndd.dap-alertgroup.com.ng"""
            # Asynchronously handle send mail
            Thread(target=send_async_email, args=(email_subject, email_boby, [data['email']])).start()
            # log account created for audit monitoring
            asyncio.run(log_audit_event(
                user=request.user.email,
                action='CREATE USER',
                details=f'User created {data["email"]} account'
            ))
            return Response({'status': 'success', 'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except (ValidationError, IntegrityError) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (Exception, ValueError) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserRetrUpdtDelView(generics.RetrieveUpdateDestroyAPIView):
    """
        User Profile Management Endpoint

        View, update, or delete user details
    """
    queryset = UserModel.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=UserSerializer, responses={200: 'OK', 401: 'UNAUTHORIZED', 404:'NOT FOUND'})
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'status': 'success', 'message': 'User details retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except (Exception, ObjectDoesNotExist) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

    @swagger_auto_schema(request_body=UserSerializer, responses={200: 'OK', 401: 'UNAUTHORIZED', 400:'BAD REQUEST', 404: 'NOT FOUND'})
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                # log account updated for audit monitoring
                asyncio.run(log_audit_event(
                    user=request.user.email,
                    action='UPDATE USER',
                    details=f'User updated "{instance}" information'
                ))
                return Response({'status': 'success', 'message': 'User updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            except (Exception, IntegrityError, ValidationError, ValueError) as e:
                general_logger.error("An error occurred: %s", e)
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                
    
    @swagger_auto_schema(request_body=UserSerializer, responses={204: 'NO CONTENT', 401: 'UNAUTHORIZED', 404: 'NOT FOUND'})
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            # log account daleted for audit monitoring
            asyncio.run(log_audit_event(
                user=request.user.email,
                action='DELETE USER',
                details=f'User deleted "{instance}" account'
            ))
            return Response({'status': 'success', 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except (Exception, ObjectDoesNotExist) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

class LoginView(TokenObtainPairView):
    """
        User Login Endpoint

        User log in with their email and password
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser,]

    @swagger_auto_schema(responses={200: 'OK', 400: 'BAD REQUEST', 401:'UNAUTHORIZED'})
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({'status': 'error', 'message': 'Email and password fields are required!'}, status=status.HTTP_400_BAD_REQUEST)
            response = super().post(request, *args, **kwargs)
            # log successful user login for audit monitoring
            asyncio.run(log_audit_event(
                user=email,
                action='USER LOGIN',
                details='User successfully logged in'
            ))
            return Response({'status': 'success', 'message': 'User logged in successfully', 'data': response.data}, status=status.HTTP_200_OK)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            return Response({'status': 'error', 'message': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(generics.GenericAPIView):
    """
        User Logout Endpoint

        Logs out user by blacklisting their refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer
    parser_classes = [JSONParser,]

    @swagger_auto_schema(responses={205: 'RESET CONTENT', 400: 'BAD REQUEST', 500:'SERVER ERROR'})
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            token = RefreshToken(data['refresh'])
            token.blacklist()
            return Response({'status': 'success', 'message': 'User logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            general_logger.error("Token error occurred: %s", e)
            return Response({'status': 'error', 'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            return Response({'status': 'error', 'message': 'refresh: '+str(e.detail['refresh']).split("'")[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PasswordResetView(ResetPasswordRequestToken):
    """
        Password Reset Endpoint

        Initiate a password reset as a register user. 
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser,]

    @swagger_auto_schema(responses={200: 'OK', 400: 'BAD REQUEST', 500:'SERVER ERROR'})
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            if not email:
                return Response({'status': 'error', 'message': 'Email field is required!'}, status=status.HTTP_400_BAD_REQUEST)
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                token = ResetPasswordToken.objects.get(user__email=email)
                email_subject = 'Alert Group Direct Debit: Password Reset Request'
                email_body = f"""Dear {token.user},\n
                You have requested a password reset. Use the following token to reset your password:\n
                Token: {token.key}\n\n
                PS: Please ignore if you did not initiate this process.\n\n
                Regards,\n
                Alert Group Direct Debit"""
                recipient = [token.user.email]
                # Asynchronously handle send mail
                Thread(target=send_async_email, args=(email_subject, email_body, recipient)).start()
                # log password reset request for audit monitoring
                asyncio.run(log_audit_event(
                    user=email,
                    action='PASSWORD RESET REQUEST',
                    details='User made request to rest password'
                ))
                return Response({'status': 'success', 'message': 'Password reset email has been sent!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Error generating reset token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            return Response({'status': 'error', 'message': 'Invalid email or email does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PasswordConfirmView(generics.GenericAPIView):
    """
        Password Confirmation Endpoint

        Confirm the new password as a register user. 
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordConfirmSerializer
    parser_classes = [JSONParser,]
    
    @swagger_auto_schema(request_body=PasswordConfirmSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 500:'SERVER ERROR'})
    def post(self, request, *args, **kwargs):
        data = request.data
        otp_token = data.get('token')
        password = data.get('password')
        if not otp_token or not password:
            return Response({'status': 'error', 'message': 'Token and password fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            token = ResetPasswordToken.objects.select_related('user').get(key=otp_token)
            user = token.user
            user.set_password(password)
            user.save()
            token.delete()
            # log changed password for audit monitoring
            asyncio.run(log_audit_event(
                user=user.email,
                action='CREATE NEW PASSWORD',
                details='User created new password'
            ))
            return Response({'status': 'success', 'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        except ResetPasswordToken.DoesNotExist as e:
            general_logger.error("Token error occurred: %s", e)
            return Response({'status': 'error', 'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            general_logger.error("Exception error occurred: %s", e)
            return Response({'status': 'error', 'message': 'Password: '+str(e.detail['password']).split("'")[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AuditLogView(generics.ListAPIView):
    """
        Audit Log Endpoint

        List records of all event/activity by a user
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']
    parser_classes = [JSONParser,]

    @swagger_auto_schema(request_body=AuditLogSerializer, responses={200: 'OK', 401: 'UNAUTHORIZED', 500:'SERVER ERROR'})
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response({'status': 'success', 'message': 'Audit log retrieved successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except (Exception, ObjectDoesNotExist) as e:
            general_logger.error("An error occurred: %s", e)
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        