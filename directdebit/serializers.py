from rest_framework import serializers
from .models import *
from utils import BILLER_ID


class CreateBillerSerializer(serializers.Serializer):
    rcNumber = serializers.CharField(min_length=5, max_length=50, help_text="The CAC registration number of the biller")
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phoneNumber = serializers.CharField(max_length=11)
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    accountName = serializers.CharField(max_length=255)
    bankCode = serializers.ChoiceField(choices=BankCode.choices, help_text="The bank code of the biller's account number")
    mandateStatusNotificationUrl = serializers.CharField(max_length=255)
    

class UpdateBillerSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="The CAC registration number of the biller")
    billerName = serializers.CharField(max_length=255)
    accountName = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phoneNumber = serializers.CharField(max_length=11)
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    bankCode = serializers.ChoiceField(choices=BankCode.choices, help_text="The bank code of the biller's account number")
    mandateStatusNotificationUrl = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=BillerStatus.choices, help_text='(Biller Status, {0=Disable, 1=Enable}):')


class CreateProductSerializer(serializers.Serializer):
    billerId = serializers.HiddenField(default=BILLER_ID)
    productName = serializers.CharField(min_length=5, max_length=100)


class DisableProductSerializer(serializers.Serializer):
    productID = serializers.CharField(max_length=25)


class CreateMandateSerializer(serializers.Serializer):
    branch = serializers.ChoiceField(choices=Branch.choices)
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    bankCode = serializers.ChoiceField(choices=BankCode.choices, help_text='3-digit CBN assigned code of the bank')
    payerName = serializers.CharField(max_length=255)
    payerEmail = serializers.EmailField()
    payerAddress = serializers.CharField(max_length=255)
    accountName = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(help_text="The amount to be debited in Naira and Kobo (5000.00).")
    narration = serializers.CharField(max_length=255, help_text='DD/AMFB/customer_name/account_number')
    phoneNumber = serializers.CharField(max_length=11)
    subscriberCode = serializers.CharField(max_length=255, help_text='Unique ID assigned to the Payer by the Payee (AMFB/alert_account_num).')
    startDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='Start Date (YYYY-MM-DD)')
    endDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='End Date (YYYY-MM-DD)')
    mandateImageFile = serializers.FileField(help_text='Upload Mandate File (jpeg, png & pdf)')
    billerId = serializers.HiddenField(default=BILLER_ID)


class EMandateSerializer(serializers.Serializer):
    branch = serializers.ChoiceField(choices=Branch.choices)
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    billerId = serializers.HiddenField(default=BILLER_ID)
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    bankCode = serializers.ChoiceField(choices=BankCode.choices, help_text='3-digit CBN assigned code of the bank')
    payerName = serializers.CharField(max_length=255)
    payerEmail = serializers.EmailField(max_length=255)
    mandateType = serializers.ChoiceField(choices=MandateType.choices, help_text='(Mandate Type, {1=Direct Debit, 2=Balance Enquiry})')
    payerAddress = serializers.CharField(max_length=255)
    accountName = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(help_text="The amount to be debited in Naira and Kobo (5000.00).")
    frequency = serializers.ChoiceField(choices=Frequency.choices, help_text='(Rate at which a customer is debited, {1=weekly, 2=2weeks, 4=monthly}):')
    narration = serializers.CharField(max_length=255, help_text='DD/AMFB/customer_name/account_number')
    phoneNumber = serializers.CharField(max_length=11)
    subscriberCode = serializers.CharField(max_length=255, help_text='Unique ID assigned to the Payer by the Payee (AMFB/alert_account_num).')
    startDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='Start Date (YYYY-MM-DD)')
    endDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='End Date (YYYY-MM-DD)')


class MandateStatusSerializer(serializers.Serializer):
    mandate_code = serializers.CharField(min_length=10, max_length=50)


class UpdateMandateStatusSerializer(serializers.Serializer):
    mandateCode = serializers.CharField(min_length=10, max_length=50)
    billerId = serializers.HiddenField(default=BILLER_ID)
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    mandateStatus = serializers.ChoiceField(choices=MandateStatus.choices, help_text='(Mandate Status, {1=Active, 2=Suspend, 3=Delete}):')


class ProcessMandateSerializer(serializers.Serializer):
    billerId = serializers.HiddenField(default=BILLER_ID)
    mandateCode = serializers.CharField(min_length=10, max_length=50)
    workflowStatus = serializers.ChoiceField(choices=WorkflowStatus.choices)


class FetchMandateSerializer(serializers.Serializer):
    billerId = serializers.HiddenField(default=BILLER_ID)
    accountNumber = serializers.CharField(min_length=10, max_length=10)


class DBMandateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandate
        fields = '__all__'
        