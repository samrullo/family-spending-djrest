import os

import django

# Set the path to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from family_spending.models import Spending,Income, SpendingName,IncomeName

spendings=Spending.objects.all()
print(f"There are {len(spendings):,} spending records in the database")