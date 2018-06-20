#!/bin/bash -x

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
PY_BIN="${ROOT_DIR}/venv/bin/python"

cd "${ROOT_DIR}/src"
git pull
webservice restart
${PY_BIN} data_updater.py
