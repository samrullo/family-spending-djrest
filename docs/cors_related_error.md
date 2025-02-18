# When you get CORS related errors

This error occurs because your backend (Django) is not configured to allow requests from your frontend (React running on `http://localhost:3000`). To fix this issue, you need to properly configure **CORS (Cross-Origin Resource Sharing)** in your Django settings.

### Steps to Fix:

#### 1. Install `django-cors-headers`
Ensure you have the `django-cors-headers` package installed in your Django project.

```bash
pip install django-cors-headers
```

#### 2. Add `corsheaders` to Installed Apps
Modify `settings.py` and include `'corsheaders'` in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
```

#### 3. Add Middleware
Make sure you add `'corsheaders.middleware.CorsMiddleware'` **above** `'django.middleware.common.CommonMiddleware'` in `MIDDLEWARE`:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
```

#### 4. Configure Allowed Origins
In your `settings.py`, add the following configuration to allow requests from `http://localhost:3000`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
]
```

In my case I had below settings

```python
CORS_ORIGIN_WHITELIST = ['http://family-spending.local','http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True
```

Alternatively, if you want to allow all origins (for development only), use:

```python
CORS_ALLOW_ALL_ORIGINS = True  # Not recommended for production
```

If your backend uses authentication via cookies or authorization headers (e.g., JWT tokens), also enable:

```python
CORS_ALLOW_CREDENTIALS = True
```

#### 5. Restart Your Django Server
After making these changes, restart your Django server:

```bash
python manage.py runserver
```

#### 6. Verify and Debug
If the issue persists:
- Check Django logs to confirm if CORS headers are being applied.
- Ensure the correct Django settings file is being used.
- Try adding `"*"` to `CORS_ALLOWED_ORIGINS` temporarily to debug.

Let me know if you need further troubleshooting! 🚀