ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} as wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
RUN python -m pip install --no-cache-dir --upgrade pip &&  \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir setuptools --upgrade && \
    pip wheel \
        --no-cache-dir \
        --wheel-dir=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt \
        -v

FROM python:${PYTHON_VERSION}

COPY --from=wheel_builder /wheels /wheels/
COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
ENV PIP_FIND_LINKS=/wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels \
    -r /tmp/requirements.txt -r /tmp/requirements-ci.txt

USER user
WORKDIR /home/user

