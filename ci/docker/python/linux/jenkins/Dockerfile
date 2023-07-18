ARG PYTHON_VERSION=3.11
ARG PIP_FIND_LINKS=/wheels/
FROM python:${PYTHON_VERSION} AS base_image
FROM base_image AS wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
COPY requirements-ci.txt /requirements/
COPY requirements/ /requirements/requirements/

ARG PIP_FIND_LINKS
RUN mkdir -p ${PIP_FIND_LINKS} &&  \
    pip wheel --wheel-dir=${PIP_FIND_LINKS} --no-cache-dir -r /requirements/requirements-ci.txt

FROM base_image

ARG PIP_FIND_LINKS
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
COPY --from=wheel_builder ${PIP_FIND_LINKS}/* ${PIP_FIND_LINKS}/
COPY --from=wheel_builder requirements/ /requirements
RUN pip install --no-index --no-cache-dir --find-links=${PIP_FIND_LINKS} \
    -r /requirements/requirements-ci.txt

USER user
WORKDIR /home/user

