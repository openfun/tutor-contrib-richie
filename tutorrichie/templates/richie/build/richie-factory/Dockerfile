ARG SITE={{ RICHIE_FACTORY_SITE }}

#--------- Base image with cloned repo
FROM python:3.7-bullseye as base

RUN apt update \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

# Clone repo
ARG RICHIE_FACTORY_REPOSITORY={{ RICHIE_FACTORY_REPOSITORY }}
ARG RICHIE_FACTORY_VERSION={{ RICHIE_FACTORY_VERSION }}
ARG SITE
RUN git clone $RICHIE_FACTORY_REPOSITORY --branch $RICHIE_FACTORY_VERSION --depth 1 /richie

#--------- Front-end builder image
FROM node:16 as frontend-builder

ARG SITE

COPY --from=base /richie/sites/${SITE}/src/frontend /app/richie/sites/${SITE}/src/frontend
WORKDIR /app/richie/sites/${SITE}/src/frontend
# --frozen-lockfile
RUN yarn install && \
    yarn compile-translations && \
    yarn build-ts-production && \
    yarn build-sass-production

#--------- Production image
FROM python:3.7-bullseye as production

ARG SITE

RUN apt update \
    && apt install -y gettext git default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# User creation
RUN useradd --home-dir /app --create-home --uid=1000 openedx
RUN mkdir -p /data/media /data/static && chown -R openedx:openedx /data
USER openedx

COPY --from=base --chown=openedx:openedx /richie /app/richie
WORKDIR /app/richie/sites/${SITE}

# Install project (with requirements)
RUN python -m venv /app/venv
ENV PATH /app/venv/bin:${PATH}
RUN pip install pip==22.0.4 setuptools==62.1.0 wheel==0.37.1
RUN pip install -r requirements/base.txt
RUN pip install uwsgi==2.0.20
RUN pip install mysqlclient==2.1.0
# The django-cms fork includes drillable search feature,
# it should be removed when this feature will be officially released
# See upstream Dockerfile https://github.com/openfun/fun-richie-site-factory/blob/main/Dockerfile
RUN pip install git+https://github.com/jbpenrath/django-cms@fun-3.11.0#egg=django-cms
# Install requirements for storing media assets on S3/MinIO
RUN pip install django-storages==1.12.3 boto3==1.20.25

WORKDIR /app/richie/sites/${SITE}/src/backend

ENV PYTHONPATH "${PYTHONPATH}:/app/richie/sites/${SITE}/src/backend"
ENV DJANGO_SETTINGS_MODULE ${SITE}.settings
ENV DJANGO_CONFIGURATION Production
ENV DJANGO_SECRET_KEY setme
ENV DJANGO_AWS_ACCESS_KEY_ID setme
ENV DJANGO_AWS_SECRET_ACCESS_KEY setme

ENV SITE=${SITE}

# Collect static assets
COPY --from=frontend-builder --chown=openedx:openedx \
    /app/richie/sites/${SITE}/src/backend/base/static/richie \
    /app/richie/sites/${SITE}/src/backend/base/static/richie
RUN ./manage.py collectstatic

# Compile translations
RUN mkdir -p locale && ./manage.py compilemessages

# Run server
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/data/static/ \
    --static-map /media=/data/media/ \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=${UWSGI_WORKERS:-2} \
    --buffer-size=8192 \
    --wsgi-file ${SITE}/wsgi.py
