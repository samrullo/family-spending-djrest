# Migrate django models
When you build the application for the first time, you will need to ssh to family spending container and run migrations

```bash
docker exec -it family_spending bash
```

And then within container

Make migrations

```bash
root@c150cae299b2:/var/www/family_spending#python manage.py makemigrations family_spending
```

Run migrations

```bash
root@c150cae299b2:/var/www/family_spending#python manage.py migrate
```