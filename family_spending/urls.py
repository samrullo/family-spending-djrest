from django.urls import path,include
from rest_framework import routers
from .views import BusinessViewSet,SpendingNameViewSet,SpendingViewSet,IncomeNameViewSet,IncomeViewSet,AssetAccountNameViewSet,AssetAccountViewSet,BalanceViewSet
from .views import AssetAccountCreateAPIView,IncomeCreateAPIView,SpendingAPICreateView
from .views import AssetAccountUpdateAPIView,IncomeUpdateAPIView,SpendingUpdateAPIView
from .views import AssetAccountDeleteAPIView,IncomeDeleteAPIView,SpendingDeleteAPIView
from .by_business_views import BusinessAssetAccountNameListAPIView,BusinessIncomeNameListAPIView,BusinessSpendingNameListAPIView,BusinessBalanceListAPIView
from .by_business_adate_views import BusinessAdateAssetAccountListAPIView,BusinessAdateIncomeListAPIView,BusinessAdateSpendingListAPIView,BusinessAdateBalanceListAPIView

router = routers.DefaultRouter()
router.register('businesses',BusinessViewSet)
router.register('spending_names',SpendingNameViewSet)
router.register('spendings',SpendingViewSet)
router.register('income_names',IncomeNameViewSet)
router.register('incomes',IncomeViewSet)
router.register('asset_account_names',AssetAccountNameViewSet)
router.register('asset_accounts',AssetAccountViewSet)
router.register('balances',BalanceViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('business/<int:business_id>/asset_account_names/',BusinessAssetAccountNameListAPIView.as_view(),name="business-asset-account-names"),
    path('business/<int:business_id>/income_names/',BusinessIncomeNameListAPIView.as_view(),name="business-income-names"),
    path('business/<int:business_id>/spending_names/',BusinessSpendingNameListAPIView.as_view(),name="business-spending-names"),
    path('business/<int:business_id>/balances/',BusinessBalanceListAPIView.as_view(),name="business-balances"),
    path('business/<int:business_id>/<str:adate>/asset_accounts/',BusinessAdateAssetAccountListAPIView.as_view(),name="business-adate-asset-accounts"),
    path('business/<int:business_id>/<str:adate>/incomes/', BusinessAdateIncomeListAPIView.as_view(), name='business-adate-incomes'),
    path('business/<int:business_id>/<str:adate>/spendings/', BusinessAdateSpendingListAPIView.as_view(), name='business-adate-spendings'),
    path('business/<int:business_id>/<str:adate>/balances/', BusinessAdateBalanceListAPIView.as_view(), name='business-adate-balances'),
    path('asset_accounts_new/',AssetAccountCreateAPIView.as_view(),name="new_asset_accounts"),
    path('asset_accounts_update/<int:pk>',AssetAccountUpdateAPIView.as_view(),name="asset_account_update"),
    path('asset_accounts_delete/<int:pk>',AssetAccountDeleteAPIView.as_view(),name="asset_account_delete"),
    path('incomes_new/',IncomeCreateAPIView.as_view(),name="new_income"),
    path('incomes_update/<int:pk>',IncomeUpdateAPIView.as_view(),name="income_update"),
    path('incomes_delete/<int:pk>',IncomeDeleteAPIView.as_view(),name="income_delete"),
    path('spendings_new/',SpendingAPICreateView.as_view(),name="new_spending"),
    path('spendings_update/<int:pk>',SpendingUpdateAPIView.as_view(),name="spending_update"),
    path('spendings_delete/<int:pk>',SpendingDeleteAPIView.as_view(),name="spending_delete")
    ]