#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

export ORIG_PATH=${PATH}

while read ver; do
  echo
  echo "###################################"
  echo "## Starting tests on Python $ver "
  echo "###################################"
  echo
  export PATH="$(get_python_path ${ver}):${ORIG_PATH}"
  LOCAL_CI=1 PYTHON_VERSION=${ver} ${_RESTAFARI_HOME}/dev/install_local_python3.sh
  cd ${_RESTAFARI_HOME}/ci
  ./build.sh
  ./test.sh
done < python-versions

