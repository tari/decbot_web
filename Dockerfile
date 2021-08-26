FROM python:3.8-slim as requirements

ADD ./ /app
RUN pip install pipenv && cd /app && pipenv lock -r | tee requirements.txt

FROM python:3.8-slim

ADD ./ /app
COPY --from=requirements /app/requirements.txt /app/requirements.txt
RUN cd /app && pip install -r requirements.txt PyMySQL whitenoise gunicorn

ENV DJANGO_SETTINGS_MODULE=decbot_web.settings_container
RUN DECBOT_WEB_SECRET_KEY=ignoreme manage.py collectstatic

ENTRYPOINT ["gunicorn", "decbot_web.wsgi:application"]
CMD ["-k", "gthread", "--threads", "4", "--capture-output"]
