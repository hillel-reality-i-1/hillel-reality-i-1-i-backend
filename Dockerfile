FROM python:3.12

ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade --yes

COPY --chown=${USER} requirements.txt requirements.txt
COPY --chown=${USER} requirements requirements

RUN pip install --upgrade pip && \
    pip install --requirement requirements/production.txt

COPY --chown=${USER} --chmod=555 ./docker/app/entrypoint.sh /entrypoint.sh
COPY --chown=${USER} --chmod=555 ./docker/app/start.sh /start.sh

COPY --chown=${USER} ./Makefile     Makefile
COPY --chown=${USER} ./manage.py manage.py
COPY --chown=${USER} ./core core
COPY --chown=${USER} ./apps apps

# Вставка команд для создания директории /var/www/static/
USER root
RUN mkdir -p /var/www/static/ \
    &&  chmod -R 775 /var/www/static/ \
    
    && mkdir -p /var/www/media/ \
    &&  chmod -R 775 /var/www/media/

RUN  mkdir -p /var/www/static/images/

USER ${USER}

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

USER root
RUN chmod --recursive a+w /usr/local/lib/python3.12/site-packages/cities_light
USER ${USER}

USER root
CMD ["/start.sh"]
