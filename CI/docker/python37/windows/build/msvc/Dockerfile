# escape=`
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.7
FROM ${PYTHON_DOCKER_IMAGE_BASE}

RUN certutil -generateSSTFromWU roots.sst ; `
    certutil -addstore -f root roots.sst ; `
    del roots.sst

ADD  requirements.txt c:/temp/

RUN python -m pip install pip upgrade ; python -m pip install -r c:\temp\requirements.txt pytest-cov flake8 appdirs cx_Freeze mypy lxml
RUN python -m pip install setuptools --upgrade
