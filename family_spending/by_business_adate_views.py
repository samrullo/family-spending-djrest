from rest_framework import generics
from rest_framework import permissions
from .models import AssetAccount, Income, Spending, Balance
from .serializers import (
    AssetAccountSerializer, IncomeSerializer, SpendingSerializer, BalanceSerializer
)
import datetime

class BusinessAdateAssetAccountListAPIView(generics.ListAPIView):
    serializer_class = AssetAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        adate_str = self.kwargs.get('adate')
        adate = datetime.datetime.strptime(adate_str, "%Y-%m-%d")
        return AssetAccount.objects.filter(business=business_id, adate=adate)


class BusinessAdateIncomeListAPIView(generics.ListAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        adate_str = self.kwargs.get('adate')
        adate = datetime.datetime.strptime(adate_str, "%Y-%m-%d")
        return Income.objects.filter(business=business_id, adate=adate)


class BusinessAdateSpendingListAPIView(generics.ListAPIView):
    serializer_class = SpendingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        adate_str = self.kwargs.get('adate')
        adate = datetime.datetime.strptime(adate_str, "%Y-%m-%d")
        return Spending.objects.filter(business=business_id, adate=adate)


class BusinessAdateBalanceListAPIView(generics.ListAPIView):
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        adate_str = self.kwargs.get('adate')
        adate = datetime.datetime.strptime(adate_str, "%Y-%m-%d")
        return Balance.objects.filter(business=business_id, adate=adate)
