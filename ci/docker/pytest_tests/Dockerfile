FROM python:3.7

ADD ["requirements.txt", "./"]
RUN pip install --no-cache-dir \
    pytest \
    mypy \
    flake8 \
    coverage \
    pylint \
     -r requirements.txt