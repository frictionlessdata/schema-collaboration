FROM debian:buster-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

RUN apt-get update && apt-get install --no-install-recommends --yes \
	python3-pip python3-setuptools \
	libmariadbclient-dev libmariadb-dev-compat libmariadb3 mariadb-client \
	python3-wheel libpython3.7-dev \
	gcc-7 gcc git \
	pandoc texlive-latex-base texlive-fonts-recommended lmodern \
	nginx supervisor
COPY requirements.txt docker/entrypoint.sh /code/
RUN pip3 install -r /code/requirements.txt
RUN apt-get purge -y libmariadbclient-dev libmariadb-dev-compat \
	gcc-7 gcc libpython3.7-dev && \
    apt-get autoremove -y && \
    apt-get clean
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY SchemaCollaboration/ /code/SchemaCollaboration
WORKDIR /code/SchemaCollaboration
ENTRYPOINT ["/code/entrypoint.sh"]
