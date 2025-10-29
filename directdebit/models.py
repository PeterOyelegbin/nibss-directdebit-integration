from django.db import models

# Create your models here.
# Branches
class Branch(models.TextChoices):
    Head_Office = 'HEAD OFFICE'
    Ebute_Metta = 'EBUTE METTA'
    Idumagbo = 'IDUMAGBO'
    Idumota = 'IDUMOTA'
    Sango = 'SANGO'
    Ikeja = 'IKEJA'
    Agege = 'AGEGE'
    Ikorodu = 'IKORODU'
    Mushin = 'MUSHIN'
    Trade_Fair = 'TRADE FAIR'
    Ikotun = 'IKOTUN'
    Ajah = 'AJAH'
    Abeokuta = 'ABEOKUTA'
    Ibandan = 'IBANDAN'

# Bank Codes
class BankCode(models.TextChoices):
    ACCESS_DIAMOND = '044', "Access or Diamond Bank"
    ECOBANK = '050', "Ecobank Nigeria"
    ENTERPRISE = '084', "Enterprise Bank"
    FIDELITY = '070', "Fidelity Bank"
    FIRST_BANK = '011', "First Bank"
    FCMB = '214', "FCMB"
    GTB = '058', "Guaranty Trust Bank"
    JAIZ = '301', "Jaiz Bank"
    KEYSTONE = '082', "Keystone Bank"
    MAINSTREET = '014', "Mainstreet Bank"
    SKYE = '076', "Skye Bank"
    STANBIC = '039', "Stanbic IBTC"
    STERLING = '232', "Sterling Bank"
    UNION = '032', "Union Bank"
    UBA = '033', "UBA"
    UNITY = '215', "Unity Bank"
    WEMA = '035', "WEMA Bank"
    ZENITH = '057', "Zenith Bank"
    PROVIDUS = '101', "Providus Bank"
    PARALLEX = '104', "Parallex Bank"
    LOTUS = '303', "Lotus Bank"
    PREMIUM_TRUST = '105', "Premium Trust Bank"
    SIGNATURE = '106', "Signature Bank"
    GLOBUS = '103', "Globus Bank"
    TITAN_TRUST = '102', "Titan Trust Bank"
    POLARIS = '067', "Polaris Bank"
    OPTIMUS = '107', "Optimus Bank"
    STANDARD_CHARTERED = '068', "Standard Chartered Bank"
    SUNTRUST = '100', "Suntrust Bank"

# Mandate Types
class MandateType(models.TextChoices):
    DIRECT_DEBIT = "1", "Direct Debit"
    BALANCE_ENQUIRY = "2", "Balance Enquiry"

# Frequency Types
class Frequency(models.TextChoices):
    VARIABLE = "0", "Variable"
    WEEKLY = "1", "Weekly"
    EVERY_2_WEEKS = "2", "Every 2 Weeks"
    MONTHLY = "4", "Monthly"

# Mandate Status
class MandateStatus(models.TextChoices):
    ACTIVE = "1", "Active"
    SUSPEND = "2", "Suspend"
    DELETE = "3", "Delete"

# Biller Status
class BillerStatus(models.TextChoices):
    DISABLE = "0", "Disable"
    ENABLE = "1", "Enable"

# Workflow Status
class WorkflowStatus(models.TextChoices):
    BILLER_INITIATED = "1", "Biller Initiated"
    BILLER_AUTHORIZED = "2", "Biller Authorized"
    BILLER_REJECTED = "3", "Biller Rejected"
    BILLER_APPROVED = "4", "Biller Approved"
    BILLER_DISAPPROVED = "5", "Biller Disapproved"
    BANK_AUTHORIZED = "6", "Bank Authorized"
    BANK_REJECTED = "7", "Bank Rejected"
    BANK_APPROVED = "8", "Bank Approved"
    BANK_DISAPPROVED = "9", "Bank Disapproved"
    BANK_INITIATED = "10", "Bank Initiated"
    

class Mandate(models.Model):
    """
    This model will serve as the storade for mandate successfully created
    """
    mandateCode = models.CharField(max_length=255, primary_key=True)
    branch = models.CharField(choices= Branch.choices, max_length=255)
    productId = models.IntegerField()
    accountNumber = models.CharField(max_length=10)
    accountName = models.CharField(max_length=255)
    payerName = models.CharField(max_length=255)
    payerEmail = models.EmailField(max_length=255)
    amount = models.IntegerField()
    phoneNumber = models.CharField(max_length=11)
    subscriberCode = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.mandateCode} | {self.branch}"
    