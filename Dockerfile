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

COPY --chown=${USER} ./Makefile Makefile
COPY --chown=${USER} ./manage.py manage.py
COPY --chown=${USER} ./core core
COPY --chown=${USER} ./apps apps

USER ${USER}

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]

