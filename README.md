# Introduction
This is an application to record assets, incomes and spendings on a monthly basis.
The intended use case is as following. I am someone who works at a company and earns salary 
on a monthly basis. At the end of the month, before I embark on the next month I want to 
find out how much I will be left with after paying out all my debts. Me as a middle aged salary
man, can have recurring debts such as mortgages, car loans, visa card loans.
In my personal case, my spouse has her little business and she heavily uses my numerous visa cards.
She pays me back what she used for her business but with some delay.
So, nevertheless, at the end of the month it becomes important for me to find out if I have
enough cash in my bank accounts to pay out all visa debts.

# How to run the application
Later in the application architecture I will explain that the application consists of front end and back end. Back end serves ```Django Rest Framework``` based APIs, including ```endpoints``` for user registration and authentication. Frontend is ```React``` based and provides UI to interact with the backend.
When you clone this repository front end comes embedded withing ```family_spending.static```. Front end app was ```built``` and files were copied into that location. Some slight changes are made to ```index.html``` to make it work. More about that in later sections.
Once you clone the app to your PC, ensure you have installed all libraries in ```requirements.txt``` (which assumes you have python3.9 and above), you can navigate to the application base folder and run below commands.

The application assumes that you will run it on docker and you will use ```postgres``` as database. If you don't have ```docker``` or ```postgres``` yet on your PC, then you can use ```sqlite``` simple database by uncommenting following lines in ```config.settings.py``` and commenting existing ```DATABASES``` config.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- Make migrations: Next you run ```makemigrations``` to generate instructions to create tables matching Data model definitions.

```bash
python manage.py makemigrations family_spending
```

- Then actually run migrate. This will also create user related tables

```python
python manage.py migrate
```

- Finally start the server and you should be able to access the application by visiting http://localhost:8000

```python
python manage.py runserver
```

# Data model
Below are data models that I define as ```Django``` models (which are essentially database SQL tables)

- **Business** : the namme of the business. This application assumes that multiple users will benefit from it. Each user's assets, incomes and spendings will have to be isolated from other users. So we have this model to achieve that. Each of the afore mentioned db models will be tied to a ```Business``` model.

- **Asset Account Name** : These are my bank accounts. I have about three of them. At the end of the month each of 
my bank accounts will have some amount of cash in it. This model simply defines bank account names. Later I will use it 
as a foreign key of my ```Asset Account``` model, which will actually record the amount of money the associated 
bank account has at the end of the month

- **Asset Account** : this is the db model where I will record how much cash my bank account has as of certain date (which is usually the end of month). It will have ```asset_account_name``` foreign key pointing to ```Asset Account Name```

- **Income Name** : the name of my income. Obviously, in my case ```Salary``` will be the first record in this table.

- **Income** : to record income amount as of certain date. It will have ```income_name``` as a foreign key pointing to ```Income Name``` db model.

- **Spending Name** : spending names. In my case, two house loans will go into it as first two records. Next, each of my visa card name will also be saved in this table.

- **Spending** : to record spending amount for each spending name as of month end. It will have ```spending_name``` as a foreign key pointing to ```Spending Name``` db model.

- **Business Balance** : This db model will sum up all assets, incomes and spendings, subtract debts from assets and report the net balance as of month end.