FROM samrullo/ubuntu_2204_nginx_pyenv_python_311

RUN mkdir /root/app
WORKDIR /root/app

COPY ./requirements.txt .
RUN /root/.pyenv/shims/pip install -r ./requirements.txt

COPY . .
