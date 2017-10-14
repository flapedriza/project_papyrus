#!/usr/bin/env sh

set -u
set -e


DIR=$(dirname $(readlink -f ${0}))
ENV_DIR="${DIR}/envs"

ENV=""
BUILD=0


usage () {
    cat <<EOF
Runs and build docker-compose loading the specified environment.

Usage: ${0} [--env ENV] [--build]

Options:
  --env       Specifies the environment to load (default: dev)
  --build     Execute build before run

Environments:
  dev
  pre
  pro

Help
  help        This fine usage message.
  halp        Alias for help.

EOF
}


while test "${#}" -gt 0
do
  case ${1} in
    --env)
      shift
      ENV=${1}
    ;;
    --build)
      BUILD=1
    ;;
    h[ea]lp)
      usage
      exit 0
    ;;
  esac
  shift
done


# Environment
ENV="${ENV:-dev}"
ENV_FILE="${ENV_DIR}/${ENV}.env"

if [ "${ENV}" = "" ] || [ ! -e "${ENV_FILE}" ]
then
  usage
  exit 1
fi

export DOCKER_COMPOSE_ENV="${ENV}"

# Build
test ${BUILD} -eq 0 || docker-compose build

# Run
docker-compose up