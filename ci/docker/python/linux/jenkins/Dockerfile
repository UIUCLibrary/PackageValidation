ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
ARG PYTHON_INDEX=https://devpi.library.illinois.edu/production/release
RUN python -m pip install --upgrade pip &&  \
    pip install wheel && \
    pip install setuptools --upgrade && \
    pip wheel \
        --no-cache-dir \
        --wheel-dir=/wheels \
        -i ${PYTHON_INDEX} \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt \
        -v

FROM python:${PYTHON_VERSION}
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN if id $USER_ID ; then \
        echo 'Existing user id found: Creating an alias' ;\
        groupadd --non-unique --gid $GROUP_ID user ; \
        useradd  --non-unique --uid $USER_ID -s /bin/sh -m -d /home/user -g user user  ; \
    else \
        groupadd -g $GROUP_ID user ; \
        useradd  -u $USER_ID -s /bin/sh -m -d /home/user -g user user ;\
    fi

COPY --from=wheel_builder /wheels /wheels/
COPY requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
ENV PIP_EXTRA_INDEX_URL="${PYTHON_INDEX}"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"
ENV PIP_FIND_LINKS=/wheels

RUN pip install --no-index --find-links=/wheels \
    -r /tmp/requirements.txt -r /tmp/requirements-ci.txt

USER user
WORKDIR /home/user