#--------- Base image with cloned repo
FROM python:3.7-bullseye as base

RUN apt update \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

# Clone repo
ARG RICHIE_REPOSITORY=https://github.com/openfun/richie.git
ARG RICHIE_VERSION={{ RICHIE_RELEASE_VERSION }}
RUN git clone $RICHIE_REPOSITORY --branch $RICHIE_VERSION --depth 1 /richie

#--------- Front-end builder image
FROM node:14 as frontend-builder

COPY --from=base /richie/src/frontend /app/richie/src/frontend
WORKDIR /app/richie/src/frontend
RUN yarn install --frozen-lockfile && \
    yarn compile-translations && \
    yarn build-ts-production && \
    yarn build-sass-production

#--------- Production image
FROM python:3.7-bullseye as production

RUN apt update \
    && apt install -y gettext git default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# User creation
RUN useradd --home-dir /app --create-home --uid=1000 openedx
RUN mkdir -p /data/media /data/static && chown -R openedx:openedx /data
USER openedx

COPY --from=base --chown=openedx:openedx /richie /app/richie
WORKDIR /app/richie

# Install project (with requirements)
RUN python -m venv /app/venv
ENV PATH /app/venv/bin:${PATH}
RUN pip install pip==21.3.1 setuptools==60.0.1 wheel==0.37.0
RUN pip install -e .[sandbox]
RUN pip install uwsgi==2.0.20
RUN pip install mysqlclient==2.1.0
# Use temporarily a forked version of djangocms-admin-style
# Remove this when djangocms-admin-style 2.0.3 will be released\
# See upstream Dockerfile https://github.com/openfun/richie/blob/master/Dockerfile
RUN pip install --prefix=/install git+https://github.com/jbpenrath/djangocms-admin-style@fun#egg=djangocms-admin-style
# Install requirements for storing media assets on S3/MinIO
RUN pip install django-storages==1.12.3 boto3==1.20.25

ENV DJANGO_SETTINGS_MODULE settings
ENV DJANGO_CONFIGURATION Production
ENV DJANGO_SECRET_KEY setme

# Collect static assets
COPY --from=frontend-builder --chown=openedx:openedx \
  /app/richie/src/richie/static/richie/js \
  /app/richie/src/richie/static/richie/js
COPY --from=frontend-builder --chown=openedx:openedx \
  /app/richie/src/richie/static/richie/css/main.css \
  /app/richie/src/richie/static/richie/css/main.css
RUN ./sandbox/manage.py collectstatic

# Compile translations
RUN ./sandbox/manage.py compilemessages

# Run server
EXPOSE 8000
CMD cd sandbox && uwsgi \
    --static-map /static=/data/static/ \
    --static-map /media=/data/media/ \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=${UWSGI_WORKERS:-2} \
    --buffer-size=8192 \
    --wsgi-file wsgi.py
