#!/usr/bin/env bash

# Allow for this script to be only sources
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
[[ "${BASH_SOURCE[0]}" == "${0}" ]] && echo >&2 "ERROR: This script '${BASH_SOURCE[0]}' can only be sourced!" && exit 1

. common.sh

EnterOrCreateVirtualEnv voting-rules-approval-tmp "$(which python3)"
