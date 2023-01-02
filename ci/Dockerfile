ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

ARG DJANGO_VERSION
ARG PILLOW_VERSION

WORKDIR /usr/src/app

COPY . .

RUN \
    export PIP_DISABLE_PIP_VERSION_CHECK=1 && \
    export PIP_NO_CACHE_DIR=1 && \
    python -m pip install "Django ${DJANGO_VERSION}" "Pillow ${PILLOW_VERSION}"

CMD ["python", "ci/runtests.py"]
