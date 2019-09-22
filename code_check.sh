#!/bin/bash
# ** does not work out of the box on our jenkins machine
start=`date +%s`
set -e

shopt -s extglob

BRANCH=${CHANGE_BRANCH:-local}

# If run in local, add `local` as a param to the script to not recreate the venv
echo "Building ${BRANCH}"
if ! [ -z "${1+x}" ] && [ "$1" == "local" ]; then
  echo "Executing locally"
  echo "Assuming we are in a venv, that is up-to-date"
  if [ -z "${VIRTUAL_ENV+x}" ]; then
    echo "Not in a virtualenv, aborting"
    exit 1
  fi

else
  echo "Creating the venv"
  VENV=venv
  if [ ! -d ${VENV} -o ! -f ${VENV}/bin/activate ]; then
    virtualenv -p python3.6 ${VENV}
  fi
  source ${VENV}/bin/activate

  set -x
  pip install -r requirements/dev.txt
  set +x
fi

# New apps should have all their code under a folder. This is not the case here yet
# APP="cloud_processing git_helpers tests utils web_mapper"
APPS=()
APPS_NO_TESTS=()
for folder in `find . -maxdepth 1 -type d | grep -v settings | sed s^\.\/^^`
do
  if [ -f "${folder}/__init__.py" ]; then
    APPS+=("$folder")
    if [ "${folder}" != "tests" ]; then
      APPS_NO_TESTS+=("$folder")
    fi
  fi
done

echo "Re-creating the reports folder"
REPORTS=reports
if [ -d ${REPORTS} ]; then
  rm -rf ${REPORTS}
fi
mkdir ${REPORTS}

# We don't allow the setup to fail. But then we execute each step whether the previous ran or not
# and consolidate the error codes at the end
set +e

#### PYLINT
pylint_start=`date +%s`
ret_code=0
set -x
`pylint -j 2 --output-format=parseable --rcfile=.pylintrc ${APPS_NO_TESTS[@]} >> "${REPORTS}/pylint.txt" 2>&1`
cmd_ret_pylint=$?
set +x
if [ $cmd_ret_pylint -ne 0 ]; then
  printf "\x1b[31m[ERROR]\x1b[0m Pylint failed\n"
fi
pylint_end=`date +%s`
ret_code=`expr $ret_code + $cmd_ret_pylint`

#### FLAKE8
flake8_start=`date +%s`
set -x
flake8 --config=setup.cfg ${APPS[@]} > ${REPORTS}/flake8.txt 2>&1
cmd_ret_flake8=$?
set +x
if [ $cmd_ret_flake8 -ne 0 ]; then
  printf "\x1b[31m[ERROR]\x1b[0m Flake8 failed\n"
fi
flake8_end=`date +%s`
ret_code=`expr $ret_code + $cmd_ret_flake8`

#### MYPY
mypy_start=`date +%s`
set -x
mypy --config-file=setup.cfg ${APPS_NO_TESTS[@]} > ${REPORTS}/mypy.txt 2>&1
cmd_ret_mypy=$?
set +x
if [ $cmd_ret_mypy -ne 0 ]; then
  printf "\x1b[31m[ERROR]\x1b[0m Mypy failed\n"
fi
mypy_end=`date +%s`
ret_code=`expr $ret_code + $cmd_ret_mypy`

#### TEST
test_start=`date +%s`
set -x
coverage run -m pytest > ${REPORTS}/test.txt 2>&1
cmd_ret_test=$?
set +x
if [ $cmd_ret_test -ne 0 ]; then
  printf "\x1b[31m[ERROR]\x1b[0m Test failed\n"
fi
test_end=`date +%s`
ret_code=`expr $ret_code + $cmd_ret_test`

cov_start=`date +%s`
set -x
coverage html --rcfile=${REPORTS}/../setup.cfg
cmd_ret_cov=$?
set +x
if [ $cmd_ret_cov -ne 0 ]; then
  printf "\x1b[31m[ERROR]\x1b[0m Coverage failed\n"
fi
cov_end=`date +%s`


set +x
end=`date +%s`

echo ""
echo ""
echo "================== SUMMARY =================="
if [ $cmd_ret_pylint -ne 0 ]; then
  printf "* PYLINT:       \x1b[31m[ERROR]\x1b[0m         %s s\n"  $((pylint_end-pylint_start))
else
  printf "* PYLINT:       \x1b[32m[SUCCESS]\x1b[0m       %s s\n"  $((pylint_end-pylint_start))
fi
if [ $cmd_ret_flake8 -ne 0 ]; then
  printf "* FLAKE8:       \x1b[31m[ERROR]\x1b[0m         %s s\n"  $((flake8_end-flake8_start))
else
  printf "* FLAKE8:       \x1b[32m[SUCCESS]\x1b[0m       %s s\n"  $((flake8_end-flake8_start))
fi
if [ $cmd_ret_mypy -ne 0 ]; then
  printf "* MYPY:         \x1b[31m[ERROR]\x1b[0m         %s s\n"  $((mypy_end-mypy_start))
else
  printf "* MYPY:         \x1b[32m[SUCCESS]\x1b[0m       %s s\n"  $((mypy_end-mypy_start))
fi
if [ $cmd_ret_test -ne 0 ]; then
  printf "* TEST:         \x1b[31m[ERROR]\x1b[0m         %s s\n"  $((test_end-test_start))
else
  printf "* TEST:         \x1b[32m[SUCCESS]\x1b[0m       %s s\n"  $((test_end-test_start))
fi
if [ $cmd_ret_cov -ne 0 ]; then
  printf "* COVERAGE:     \x1b[31m[ERROR]\x1b[0m         %s s\n"  $((cov_end-cov_start))
else
  printf "* COVERAGE:     \x1b[32m[SUCCESS]\x1b[0m       %s s\n"  $((cov_end-cov_start))
fi

echo "============================================="
echo " Execution time:" $((end-start)) "sec"
echo ""
echo "Note that E2E tests were not run. You can run them with"
echo "    python -m unittest test_processing.test"

set -x
exit $ret_code
