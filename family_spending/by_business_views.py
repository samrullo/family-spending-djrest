from rest_framework import generics
from rest_framework import permissions
from .models import AssetAccountName,SpendingName,IncomeName
from .models import AssetAccount,Income,Spending,Balance
from .serializers import AssetAccountNameSerializer,SpendingNameSerializer, IncomeNameSerializer
from .serializers import AssetAccountSerializer,IncomeSerializer,SpendingSerializer,BalanceSerializer

class BusinessAssetAccountNameListAPIView(generics.ListAPIView):
    serializer_class = AssetAccountNameSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return AssetAccountName.objects.filter(business = business_id)

class BusinessSpendingNameListAPIView(generics.ListAPIView):
    serializer_class = SpendingNameSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return SpendingName.objects.filter(business = business_id)

class BusinessIncomeNameListAPIView(generics.ListAPIView):
    serializer_class = IncomeNameSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return IncomeName.objects.filter(business = business_id)

class BusinessAssetAccountListAPIView(generics.ListAPIView):
    serializer_class=AssetAccountSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return AssetAccount.objects.filter(business=business_id)

class BusinessIncomeListAPIView(generics.ListAPIView):
    serializer_class=IncomeSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return Income.objects.filter(business=business_id)

class BusinessSpendingListAPIView(generics.ListAPIView):
    serializer_class=SpendingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return Spending.objects.filter(business=business_id)

class BusinessBalanceListAPIView(generics.ListAPIView):
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return Balance.objects.filter(business=business_id)