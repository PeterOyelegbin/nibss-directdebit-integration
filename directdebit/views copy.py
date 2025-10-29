from rest_framework import views, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from utils import IsAuthorized, format_date, request_api_token, make_api_request


class CreateMandateView(generics.CreateAPIView):
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO']
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['startDate'] = format_date(data.get('startDate'))
        data['endDate'] = format_date(data.get('endDate'))
        # Handle file upload
        file = data.pop('mandateImageFile', None)
        if not file:
            return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Prepare payload for file upload
        file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint="ndd/api/MandateRequest/CreateMandateDirectDebit",
            payload=data,
            files=file_upload,
        )
        

class BalanceEnquiryView(generics.GenericAPIView):
    serializer_class = CreateMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO']
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['startDate'] = format_date(data.get('startDate'))
        data['endDate'] = format_date(data.get('endDate'))
        # Handle file upload
        file = data.pop('mandateImageFile', None)
        if not file:
            return Response({'status': 'error', 'message': 'File field is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Prepare payload for file upload
        file_upload = [('mandateImageFile', (file.name, file, file.content_type))]
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint="ndd/api/MandateRequest/CreateMandateBalanceEnquiry",
            payload=data,
            files=file_upload,
        )
    

class MandateStatusView(generics.GenericAPIView):
    serializer_class = MandateStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO', 'CREDIT', 'IT']
    parser_classes = [JSONParser,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mandate_code = serializer.validated_data['mandate_code']
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint=f"ndd/api/MandateRequest/MandateStatus?MandateCode={mandate_code}",
        )
    

class CreateEMandateView(generics.GenericAPIView):
    serializer_class = EMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO']
    parser_classes = [JSONParser,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['startDate'] = format_date(data.get('startDate'))
        data['endDate'] = format_date(data.get('endDate'))
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint=f"ndd/api/MandateRequest/CreateEmandate",
            payload=data,
        )
    

class FetchMandateView(generics.GenericAPIView):
    serializer_class = FetchMandateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO', 'CREDIT', 'IT']
    parser_classes = [JSONParser,]

    def post(self, request, page, pageSize, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint=f"ndd/api/MandateRequest/FetchMandate/{page}/{pageSize}",
            payload=data,
        )
    

class UpdateMandateStatusView(generics.GenericAPIView):
    serializer_class = UpdateMandateStatus
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CREDIT']
    parser_classes = [JSONParser,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return make_api_request(
            auth_user=request.user.email,
            method="POST",
            endpoint=f"ndd/api/MandateRequest/UpdateMandateStatus",
            payload=data,
        )
    

class GetProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['CSO', 'CREDIT', 'IT']

    def get(self, request, billerID, *args, **kwargs):
        return make_api_request(
            auth_user=request.user.email,
            endpoint=f"ndd/api/Biller/GetProduct/{billerID}",
            method="GET",
        )
        

class GetAPIKeyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorized]
    allowed_roles = ['IT']

    def get(self, request, *args, **kwargs):
        try:
            response = request_api_token()
            return Response({'status': 'success', 'message': 'Fetched key successfully', 'token': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'fail', 'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        