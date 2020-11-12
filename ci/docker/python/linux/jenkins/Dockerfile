ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

COPY requirements.txt ci/docker/python/linux/jenkins/requirements-ci.txt /tmp/
ARG PYTHON_INDEX=https://devpi.library.illinois.edu/production/release
RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel
RUN pip wheel \
        --no-cache-dir \
        --wheel-dir=/wheels \
        -i ${PYTHON_INDEX} \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt \
        -v

FROM python:${PYTHON_VERSION}
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID user && \
    useradd -u $USER_ID -s /bin/sh -m -d /home/user -g user user

COPY --from=wheel_builder /wheels /wheels/
COPY requirements.txt ci/docker/python/linux/jenkins/requirements-ci.txt /tmp/
ENV PIP_EXTRA_INDEX_URL="${PYTHON_INDEX}"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"
ENV PIP_FIND_LINKS=/wheels

RUN pip install --no-index --find-links=/wheels \
    -r /tmp/requirements.txt -r /tmp/requirements-ci.txt

USER user
WORKDIR /home/user