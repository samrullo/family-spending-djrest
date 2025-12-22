import os

import django

# Set the path to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Setup Django
django.setup()

import datetime
from django.contrib.auth import get_user_model
from family_spending.models import Spending,Income, SpendingName,IncomeName

spendings=Spending.objects.all()
print(f"There are {len(spendings):,} spending records in the database")
adate=datetime.date(2025,12,31)
dec_spending_rows = (
    Spending.objects
    .filter(adate=adate)
    .values(
        "id",
        "amount",
        "adate",
        "due_date",
        "spending_name_id",
        "spending_name__name",
        "spending_name__associated_asset_account_name_id",
        "spending_name__associated_asset_account_name__name",
    )
)