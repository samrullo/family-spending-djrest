FROM samrullo/ubuntu_2204_pyenv_311

RUN mkdir /var/www/family_spending
WORKDIR /var/www/family_spending

COPY ./data/etc/systemd/system/family_spending.service /etc/systemd/system/

COPY ./requirements.txt .
RUN /root/.pyenv/shims/pip install -r ./requirements.txt
