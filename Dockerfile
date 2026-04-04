FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    net-tools \
    iputils-ping \
    unzip \
    gettext \
    zip \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir Django==5.2.12 \
                               psycopg2-binary==2.9.11 \
                               django-bootstrap5==26.2
# requests \
# gunicorn dotenv \

EXPOSE 8000

WORKDIR /workspace

CMD ["/bin/bash"]

# docker build -t navaja-suiza .
# docker run -p 8000:8000 -it --rm -v "$(pwd)":/workspace navaja-suiza 
# python manage.py runserver 0.0.0.0:8000
# alias rt="python3 manage.py runserver 0.0.0.0:8000"
# apt-get update && apt-get install -y gettext