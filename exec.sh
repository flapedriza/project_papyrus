#!/usr/bin/env sh

set -ue

DIR=$(dirname $(readlink -f ${0}))
ENV_DIR="${DIR}/envs"

ENV=""
CMD=""


usage () {
    cat <<EOF
Executes a command from the host loading the specified environment.

Usage: ${0} [--env ENV] COMMAND

Options:
  --env       Specifies the environment to load (default: dev)

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
    h[ea]lp)
      usage
      exit 0
    ;;
    *)
      CMD="${CMD} ${1}"
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

# Run
export $(grep -vE "^\s*#" ${ENV_FILE} 2>/dev/null | xargs)
echo "Exec:${CMD}"
eval "${CMD}"