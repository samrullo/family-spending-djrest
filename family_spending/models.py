from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Business(models.Model):
    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="business_owner")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="business_modified_by")

    class Meta:
        unique_together=['owner','name']

    def __str__(self) -> str:
        return self.name

class AssetAccountName(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    is_enabled = models.BooleanField(default=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","name"]

    def __str__(self) -> str:
        return self.name

class AssetAccount(models.Model):
    asset_account_name = models.ForeignKey(AssetAccountName, on_delete=models.CASCADE)
    adate = models.DateField()
    original_balance = models.IntegerField()
    account_income = models.IntegerField()
    account_liability = models.IntegerField()
    account_balance = models.IntegerField()    
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","asset_account_name","adate"]


class SpendingName(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    is_enabled = models.BooleanField(default=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    associated_asset_account_name = models.ForeignKey(AssetAccountName,on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","name"]

    def __str__(self) -> str:
        return self.name

# Create your models here.
class Spending(models.Model):
    spending_name = models.ForeignKey(SpendingName,on_delete=models.CASCADE)
    amount = models.IntegerField()
    adate = models.DateField()
    due_date = models.DateField()
    business = models.ForeignKey(Business,on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","spending_name","adate"]

class IncomeName(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    is_enabled = models.BooleanField(default=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    associated_asset_account_name = models.ForeignKey(AssetAccountName,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","name"]

    def __str__(self) -> str:
        return self.name

class Income(models.Model):
    income_name = models.ForeignKey(IncomeName, on_delete=models.CASCADE)
    amount = models.IntegerField()
    adate = models.DateField()
    due_date = models.DateField()
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )

    class Meta:
        unique_together = ["business","income_name","adate"]


class Balance(models.Model):
    adate = models.DateField()
    total_asset = models.IntegerField()
    total_income = models.IntegerField()
    total_spending = models.IntegerField()
    total_net = models.IntegerField()
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["business","adate"]