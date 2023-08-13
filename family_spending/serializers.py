from rest_framework import serializers
from .models import Business,SpendingName,Spending,IncomeName,Income,AssetAccountName,AssetAccount,Balance
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'] in ['POST','PATCH','UPDATE']:
            fields.pop('modified_by',None)
        return fields

class BusinessSerializer(BaseSerializer):
    owner_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Business
        fields = "__all__"
    
    def get_owner_name(self,obj):
        return obj.owner.username

class SpendingNameSerializer(BaseSerializer):
    business_name = serializers.SerializerMethodField(read_only=True)
    asset_account_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SpendingName
        fields = "__all__"
    
    def get_business_name(self,obj):
        return obj.business.name
    
    def get_asset_account_name(self,obj):
        return obj.associated_asset_account_name.name

class SpendingSerializer(BaseSerializer):
    spending_name_name = serializers.SerializerMethodField(read_only=True)
    business_name = serializers.SerializerMethodField(read_only=True)
    asset_account_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Spending
        fields="__all__"
    
    def get_spending_name_name(self,obj):
        return obj.spending_name.name
    
    def get_business_name(self,obj):
        return obj.business.name
    
    def get_asset_account_name(self,obj):
        return obj.spending_name.associated_asset_account_name.name

class IncomeNameSerializer(BaseSerializer):
    business_name = serializers.SerializerMethodField(read_only=True)
    asset_account_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = IncomeName
        fields="__all__"
    
    def get_business_name(self,obj):
        return obj.business.name
    
    def get_asset_account_name(self,obj):
        return obj.associated_asset_account_name.name

class IncomeSerializer(BaseSerializer):
    income_name_name = serializers.SerializerMethodField(read_only=True)
    business_name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Income
        fields = "__all__"
    
    def get_income_name_name(self,obj):
        return obj.income_name.name
    
    def get_business_name(self,obj):
        return obj.business.name
    
class AssetAccountNameSerializer(BaseSerializer):
    business_name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = AssetAccountName
        fields = "__all__"
    
    def get_business_name(self,obj):
        return obj.business.name

class AssetAccountSerializer(BaseSerializer):
    asset_account_name_name = serializers.SerializerMethodField(read_only=True)
    business_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AssetAccount
        fields = "__all__"
    
    def get_asset_account_name_name(self,obj):
        return obj.asset_account_name.name
    
    def get_business_name(self,obj):
        return obj.business.name

class BalanceSerializer(BaseSerializer):
    business_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Balance
        fields = "__all__"
    
    def get_business_name(self,obj):
        return obj.business.name