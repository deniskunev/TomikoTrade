FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash yt && chmod 777 /opt /run

WORKDIR /yt

RUN mkdir /yt/static && mkdir /yt/media && chown -R yt:yt /yt && chmod 755 /yt

COPY --chown=yt:yt . .

RUN pip install -r requirements.txt

USER yt

CMD ["cd myproject","python manage.py runserver"]
