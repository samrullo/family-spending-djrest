FROM samrullo/ubuntu_2204_nginx_pyenv_python_311

RUN mkdir /var/www/family_spending
WORKDIR /var/www/family_spending

COPY ./data/etc/systemd/system/family_spending.service /etc/systemd/system/
COPY ./data/nginx/etc/nginx/sites-available/family-spending-local.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/family-spending-local.conf /etc/nginx/sites-enabled/

COPY ./requirements.txt .
RUN /root/.pyenv/shims/pip install -r ./requirements.txt
