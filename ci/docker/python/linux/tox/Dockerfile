FROM ubuntu:20.04 as wheel_builder_base
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/
RUN apt-get update && \
    apt-get install -y software-properties-common=0.99.9.10 --no-install-recommends && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    < /tmp/apt-packages.txt xargs apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

# ==============================================================================
FROM wheel_builder_base as WHEEL_BUILDER_PY37
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
RUN PYTHON=python3.7 && \
    $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir  \
      -r /tmp/requirements-ci.txt  \
      -r /tmp/requirements.txt

# ==============================================================================
FROM wheel_builder_base as WHEEL_BUILDER_PY38
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
RUN PYTHON=python3.8 && \
    $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir  \
      -r /tmp/requirements-ci.txt  \
      -r /tmp/requirements.txt

# ==============================================================================
FROM wheel_builder_base as WHEEL_BUILDER_PY39
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
RUN PYTHON=python3.9 && \
    $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir  \
      -r /tmp/requirements-ci.txt  \
      -r /tmp/requirements.txt

# ==============================================================================
FROM wheel_builder_base as WHEEL_BUILDER_PY310
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements /tmp/requirements
RUN PYTHON=python3.10 && \
    $PYTHON -m ensurepip --upgrade && \
    $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir  \
      -r /tmp/requirements-ci.txt  \
      -r /tmp/requirements.txt

# ==============================================================================
FROM wheel_builder_base
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
COPY --from=WHEEL_BUILDER_PY37 /wheels/* /wheels/
COPY --from=WHEEL_BUILDER_PY38 /wheels/* /wheels/
COPY --from=WHEEL_BUILDER_PY39 /wheels/* /wheels/
COPY --from=WHEEL_BUILDER_PY310 /wheels/* /wheels/
ENV PIP_FIND_LINKS=/wheels
COPY requirements/requirements_tox.txt /requirements/requirements_tox.txt
RUN pip3 install --no-cache-dir -r /requirements/requirements_tox.txt "devpi-client<6.0"
WORKDIR /src
CMD ["tox", "--workdir", "/tmp/tox", "--recreate"]

