import logging
from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics,status
from rest_framework.response import Response

from .models import Business,SpendingName,Spending,IncomeName,Income,AssetAccountName,AssetAccount,Balance
from .serializers import BusinessSerializer,SpendingNameSerializer,SpendingSerializer,IncomeNameSerializer,IncomeSerializer,AssetAccountNameSerializer,AssetAccountSerializer,BalanceSerializer
from .utils import update_balance,update_asset_account


class ModifiedByMixin:
    def perform_create(self,serializer):
        serializer.save(modified_by=self.request.user)
    
    def perform_update(self,serializer):
        serializer.save(modified_by=self.request.user)

class BusinessViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

class SpendingNameViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SpendingName.objects.all()
    serializer_class = SpendingNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        return queryset

class SpendingViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Spending.objects.all()
    serializer_class = SpendingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('spending_name','business')
        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        create_view = SpendingAPICreateView.as_view()
        return create_view(request._request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        update_view = SpendingUpdateAPIView.as_view()
        return update_view(request._request,*args,**kwargs)



class SpendingAPICreateView(ModifiedByMixin,generics.CreateAPIView):
    serializer_class = SpendingSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        with transaction.atomic():
            spending = serializer.save()
            spending.modified_by = self.request.user
            spending.save()
            asset_account_name = spending.spending_name.associated_asset_account_name
            update_asset_account(asset_account_name,spending.business,spending.adate,self.request)
            update_balance(spending.business,spending.adate,self.request)

class SpendingUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SpendingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Spending.objects.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            spending = serializer.save()
            spending.modified_by = self.request.user
            spending.save()
            asset_account_name = spending.spending_name.associated_asset_account_name
            update_asset_account(asset_account_name,spending.business,spending.adate,self.request)
            update_balance(spending.business,spending.adate,self.request)


class SpendingDeleteAPIView(generics.DestroyAPIView):
    queryset = Spending.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            associated_asset_account_name = instance.spending_name.associated_asset_account_name

            # First, delete the Spending instance
            instance.delete()

            # Now, update the associated asset account and balance
            update_asset_account(associated_asset_account_name, instance.business, instance.adate, request)
            update_balance(instance.business, instance.adate, request)

            return Response(status=status.HTTP_204_NO_CONTENT)

class IncomeNameViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = IncomeName.objects.all()
    serializer_class = IncomeNameSerializer

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset = queryset.select_related("business")

        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        return queryset

class IncomeViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("income_name","business")

        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        create_view = IncomeCreateAPIView.as_view()
        return create_view(request._request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        update_view = IncomeUpdateAPIView.as_view()
        return update_view(request._request,*args,**kwargs)

class IncomeCreateAPIView(ModifiedByMixin,generics.CreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        with transaction.atomic():
            income = serializer.save()
            income.modified_by = self.request.user
            income.save()
            asset_account_name=income.income_name.associated_asset_account_name            
            update_asset_account(asset_account_name,income.business,income.adate,self.request)
            update_balance(income.business,income.adate,self.request)

class IncomeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Income.objects.all()

    def perform_update(self, serializer):
        with transaction.atomic():
            income = serializer.save()
            income.modified_by = self.request.user
            income.save()
            asset_account_name=income.income_name.associated_asset_account_name
            update_asset_account(asset_account_name,income.business,income.adate,self.request)
            update_balance(income.business,income.adate,self.request)

class IncomeDeleteAPIView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            asset_account_name = instance.income_name.associated_asset_account_name

            # First, delete the instance
            instance.delete()

            # Now, update the asset account and balance
            update_asset_account(asset_account_name, instance.business, instance.adate, request)
            update_balance(instance.business, instance.adate, request)

            return Response(status=status.HTTP_204_NO_CONTENT)


class AssetAccountNameViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AssetAccountName.objects.all()
    serializer_class = AssetAccountNameSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.select_related("business")

        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        return queryset

class AssetAccountViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AssetAccount.objects.all()
    serializer_class = AssetAccountSerializer

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset = queryset.select_related("asset_account_name","business")

        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        
        return queryset

    def create(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        try:
            logging.debug(f"about to create new asset account with request {request._request}")
            create_view = AssetAccountCreateAPIView.as_view()
            return create_view(request._request,*args,**kwargs)
        except Exception as e:
            logging.debug(f"exception while creatingnew asset account {e}")
    
    # def update(self, request, *args, **kwargs):
    #     update_view = AssetAccountUpdateAPIView.as_view()
    #     return update_view(request._request,*args,**kwargs)


class AssetAccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AssetAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        logging.debug(f"about to create in AssetAccountCreateAPIView received serializer {serializer}")
        try:
            with transaction.atomic():
                logging.debug(f"about to create in AssetAccountCreateAPIView received serializer {serializer}")
                asset_account_s=serializer.save()
                asset_account_s.modified_by=self.request.user
                asset_account_s.save()
                update_asset_account(asset_account_s.asset_account_name,asset_account_s.business,asset_account_s.adate,self.request)
                update_balance(asset_account_s.business,asset_account_s.adate,self.request)
        except Exception as e:
            logging.debug(f"exception inside AssetAccountCreateAPIView {e}")

class AssetAccountUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AssetAccountSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AssetAccount.objects.all()

    def perform_update(self,serializer):
        with transaction.atomic():
            asset_account_s=serializer.save()
            asset_account_s.modified_by=self.request.user
            asset_account_s.save()
            update_asset_account(asset_account_s.asset_account_name,asset_account_s.business,asset_account_s.adate,self.request)
            update_balance(asset_account_s.business,asset_account_s.adate,self.request)


class AssetAccountDeleteAPIView(generics.DestroyAPIView):
    queryset = AssetAccount.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            business = instance.business
            adate = instance.adate

            # First, delete the AssetAccount instance
            instance.delete()

            # Now, update the balance
            update_balance(business, adate, request)

            return Response(status=status.HTTP_204_NO_CONTENT)

class BalanceViewSet(ModifiedByMixin,viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get_queryset(self):
        queryset= super().get_queryset()
        queryset = queryset.select_related("business")
        if not self.request.user.is_staff:
            queryset = queryset.filter(business__owner=self.request.user)
        
        return queryset


