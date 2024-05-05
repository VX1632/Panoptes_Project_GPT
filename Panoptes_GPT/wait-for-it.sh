#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available

TIMEOUT=15
QUIET=0
WAIT=0

echoerr() { if [[ "$QUIET" -ne 1 ]]; then echo "$@" 1>&2; fi }

usage() {
    exitcode="$1"
    cat << USAGE >&2
Usage:
    $cmdname host:port [-q] [-t timeout] [-- command args]
    -q | --quiet                        Do not output any status messages
    -t TIMEOUT | --timeout=timeout      Timeout in seconds, zero for no timeout
    -- COMMAND ARGS                     Execute command with args after the test finishes
USAGE
    exit "$exitcode"
}

wait_for() {
    for i in `seq $TIMEOUT` ; do
        nc -z "$HOST" "$PORT" > /dev/null 2>&1

        result=$?
        if [[ $result -eq 0 ]] ; then
            if [[ $WAIT -eq 1 ]]; then
                sleep 1
            else
                if [[ "$QUIET" -ne 1 ]]; then echo "$HOST:$PORT is available after $i seconds"; fi
                return 0
            fi
        fi
        sleep 1
    done
    echo "Operation timed out" >&2
    return 1
}

while [[ "$#" -gt 0 ]]
do
    case "$1" in
      *:* )
      HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
      PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
      shift 1
      ;;
      -q | --quiet)
      QUIET=1
      shift 1
      ;;
      -t)
      TIMEOUT="${2}"
      shift 2
      ;;
      --timeout=*)
      TIMEOUT="${1#*=}"
      shift 1
      ;;
      --)
      shift
      WAIT=1
      break
      ;;
      --help)
      usage 0
      ;;
      *)
      echoerr "Unknown argument: $1"
      usage 1
      ;;
    esac
done
