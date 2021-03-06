FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi


# - add code folder inside
# - set the working directory for all further commands
RUN mkdir /code
WORKDIR /code

# Requirements are installed here to ensure they will be cached.
COPY web/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker/production/web/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/production/web/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

# - copy all other files to /code/ directory
ADD ./web/ /code/

RUN chmod 777 -R /code/logs

# WORKDIR /app

ENTRYPOINT ["/entrypoint"]