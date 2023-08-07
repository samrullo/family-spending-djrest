import logging
from typing import Union
from .models import Balance,AssetAccount,Spending,Income,IncomeName, SpendingName
from .serializers import SpendingSerializer,IncomeSerializer,AssetAccountSerializer


# def update_asset_account(asset_account_name,business,adate):
#     asset_account = AssetAccount.objects.filter(asset_account_name=asset_account_name).first()
#     logging.debug(f"Found asset account {asset_account} for {asset_account_name} business {business} adate {adate}")
#     total_income,total_spending = calculate_totals_for_asset_account(asset_account_name,business,adate)    
#     asset_account.account_income = total_income
#     asset_account.account_liability = total_spending
#     asset_account.account_balance = asset_account.original_balance + total_income - total_spending
#     asset_account.save()

def update_asset_account(asset_account_name, business, adate,request):
    asset_account = AssetAccount.objects.filter(asset_account_name=asset_account_name).filter(business=business).filter(adate=adate).first()
    logging.debug(f"Found asset account {asset_account} for {asset_account_name} business {business} adate {adate}")
    total_income, total_spending = calculate_totals_for_asset_account(asset_account_name, business, adate)

    serializer = AssetAccountSerializer(instance=asset_account, data={
        'account_income': total_income,
        'account_liability': total_spending,
        'account_balance': asset_account.original_balance + total_income - total_spending
    }, partial=True, context={"request":request})

    if serializer.is_valid():
        serializer.save()
        logging.debug("Asset account updated successfully.")
    else:
        logging.error("Error occurred while updating asset account:", serializer.errors)



from .serializers import BalanceSerializer
def update_balance(business,adate,request):    
    balances = Balance.objects.filter(business=business).filter(adate=adate)
    total_asset,total_income,total_spending,total_net = calculate_totals_for_balance(business,adate)
    if len(balances)>0:
        balance = balances[0]        
        balance.total_asset = total_asset
        balance.total_income = total_income
        balance.total_spending = total_spending
        balance.total_net = total_net
        balance.save()
    else:
        balance = BalanceSerializer(data={"business":business.id,
                                          "adate":adate,
                          "total_asset":total_asset,
                          "total_income":total_income,
                          "total_spending":total_spending,
                          "total_net":total_net,},
                          context={"request":request})
        if balance.is_valid():
            logging.debug("balance was valid")
            balance.save()
        else:
            logging.debug("balance was invalid")



def calculate_totals_for_balance(business,adate):
    asset_accounts = AssetAccount.objects.filter(business=business).filter(adate=adate)
    logging.debug(f"Fetched {len(asset_accounts)} asset_accounts as of {adate} for business {business}")
    total_asset = sum([aa.original_balance for aa in asset_accounts]) if len(asset_accounts)>0 else 0
    logging.debug(f"Calculated total asset of {total_asset}")
    incomes = Income.objects.filter(business=business).filter(adate=adate)
    logging.debug(f"Fetched {len(incomes)} incomes for business {business} adate {adate}")
    total_income = sum([income.amount for income in incomes]) if len(incomes)>0 else 0
    logging.debug(f"Calculated total income of {total_income}")
    spendings = Spending.objects.filter(business=business).filter(adate=adate)
    logging.debug(f"Fetched {len(spendings)} spendings")
    total_spending = sum([spending.amount for spending in spendings]) if len(spendings)>0 else 0
    logging.debug(f"Calculated total spending {total_spending}")
    total_net = total_asset + total_income - total_spending
    logging.debug(f"Total net is {total_net}")
    return total_asset,total_income,total_spending,total_net

def calculate_totals_for_asset_account(asset_account_name,business,adate):    
    income_names = IncomeName.objects.filter(business=business).filter(associated_asset_account_name=asset_account_name)
    logging.debug(f"fetched {len(income_names)} income names")
    incomes = Income.objects.filter(business=business).filter(adate=adate).filter(income_name__in=income_names)
    logging.debug(f"filtered {len(incomes)} incomes")
    spending_names = SpendingName.objects.filter(business=business).filter(associated_asset_account_name=asset_account_name)
    logging.debug(f"found {len(spending_names)} spending names for business {business} adate {adate} asset account name {asset_account_name}")
    spendings = Spending.objects.filter(business=business).filter(adate=adate).filter(spending_name__in=spending_names)
    logging.debug(f"found {len(spendings)} spendings")
    total_income = sum([income.amount for income in incomes]) if len(incomes)>0 else 0
    total_spending = sum([spending.amount for spending in spendings]) if len(spendings)>0 else 0
    logging.debug(f"calculated total income {total_income}, total spending {total_spending}")
    return total_income,total_spending
