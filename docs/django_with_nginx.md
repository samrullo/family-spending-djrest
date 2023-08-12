First I ensured that I am installing ```uwsgi``` when building the image.

```uwsgi.ini``` looks like below
The value of the ```module``` is ```<project name>.wsgi:<callable>```
It just happens that when running ```django-admin startproject <projectname>``` I gave it a name ```config```, because the newly created folder will mostly contain configs for my django applications, which will be a separate subfolder.

```ini
[uwsgi]
module = config.wsgi:application
master = true

socket = config.sock
chmod-socket = 664
vacuum = true

die-on-term = true
```

I had to add every possible ```hostname``` that may send request to django app into ```ALLOWED_HOSTS``` list in ```settings.py```

```/etc/nginx/sites-available/family-spending-local.conf``` looks like below.
I bought a domain for it, added A record pointint to azure vm.
You will notice I have path to serve static files. I have ```volume``` directive pointing app folder to ```/var/www/family_spending```
Then I am using ```uwsgi_pass``` directive to direct requests to the socket, which is then probably passed by uwsgi server to django

```bash
server {
    listen 80;
    listen [::]:80;
    server_name samrullobusiness.shop www.samrullobusiness.shop;
    server_tokens off;

    location /static/ {
        alias /var/www/family_spending/family_spending/static/;
        expires 30d;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/var/www/family_spending/config.sock;
    }
}
```

I iniate a system service called ```family_spending.service``` which starts uwsgi server and listens on a socket

You can see that the service executes uwsgi command and uses uwsgi.ini file for configs. This in turn starts uwsgi server that listens to nginx reverse proxied web requests, processes them as djnago would have dones and pass them back to nginx web server.

```ini
[Unit]
Description=uWSGI occasion to serve family_spending
After=community.goal

[Service]
Person=root
Group=www-data
WorkingDirectory=/var/www/family_spending
ExecStart=/root/.pyenv/shims/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.goal
```