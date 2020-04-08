#!/usr/bin/env bash
# Alternative for sourcing?
# https://stackoverflow.com/questions/7120426/how-to-invoke-bash-run-commands-inside-the-new-shell-and-then-give-control-bac


# Allow for this script to be only sources
# https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
# man bash | less -p BASH_SOURCE
[[ "${BASH_SOURCE[0]}" == "${0}" ]] && echo >&2 "ERROR: This script '${BASH_SOURCE[0]}' can only be sourced!" && exit 1

# Since this file is sourced we must avoid using 'exit' and instead use 'return'
# https://stackoverflow.com/questions/3666846/how-do-you-return-to-a-sourced-bash-script


######################################
### Cleanup on script exit

# Preserve old bash options
# https://unix.stackexchange.com/questions/310957/how-to-undo-a-set-x/310963
# Add add leading space to each command
# to prevent adding them to bash history
# https://serverfault.com/questions/72744/command-to-prepend-string-to-each-line
#oldstate="$(shopt -po xtrace | while read line; do echo " $line"; done)"
# Alternative with sed: "$(shopt -po | sed 's/^/    /')"

# FINISHED_ONCE=1
#
# function finish {
#   # finish will be called first time when this common.sh script finishes
#   # ignore it
#   if [[ ! $FINISHED_ONCE -eq 0 ]]; then
#     FINISHED_ONCE=0
#     return
#   fi
#
#   # Cleanup code here
#
#   # Restore to recorded state of bash options
#   # Use 'set +vx' to avoid the printing of a long list of options
#   set +vx
#   eval "$oldstate"
#   set +vx #
# }

# http://redsymbol.net/articles/bash-exit-traps/
# """
# There is a simple, useful idiom to make your bash scripts more
# robust - ensuring they always perform necessary cleanup operations,
# even when something unexpected goes wrong. The secret sauce is a
# pseudo-signal provided by bash, called EXIT, that you can trap;
# commands or functions trapped on it will execute when the script
# exits for any reason.
# """
#
# Also, why trapping on RETURN does not trap on functions (at least by deafult)
# https://unix.stackexchange.com/questions/419017/return-trap-in-bash-not-executing-for-function
# """
# If a sigspec is RETURN, the command arg is executed each time a
# shell function or a script executed with the . or source builtins finishes executing.
#"""
#"""
# All other aspects of the shell execution environment are identical between
# a function and its caller with these exceptions: the DEBUG and RETURN traps
# (see the description of the trap builtin under SHELL BUILTIN COMMANDS below)
# are not inherited unless the function has been given the trace attribute
# (see the description of the declare builtin below) or the -o functrace shell
# option has been enabled with the set builtin (in which case all functions
# inherit the DEBUG and RETURN traps), and the ERR trap is not inherited unless
# the -o errtrace shell option has been enabled.
# """
# set -o functrace

#  trap finish RETURN


######################################
### Bash debug/error opts setup

# This will cause the shell to exit immediately if a simple command exits with a nonzero exit value.
# A simple command is any command not part of an if, while, or until test, or part of an && or || list.
#
# Abort script at first error, when a command exits with non-zero status (except in until or while loops, if-tests, list constructs)
# set -e
# Causes a pipeline to return the exit status of the last command in the pipe that returned a non-zero return value.
# set -o pipefail

# -u Treats references to unset variables as errors.
# We cannot set this because this script fails with:
#   bash: VIRTUALENVWRAPPER_HOOK_DIR: unbound variable
# set -u

# set -v or set -o verbose  Print shell input lines as they are read.
# set -x or set -o xtrace   Print commands and their arguments as they are executed.
# set -xv

######################################
### Python tools setup

function CheckAndSetupBasicPythonEnvironment {
    # https://stackoverflow.com/questions/592620/how-to-check-if-a-program-exists-from-a-bash-script
    # If pip is not installed
    # then exit
    if ! command -v pip >/dev/null 2>&1; then
        echo >&2 "ERROR: pip not found but required!"; return 1
    fi

    # If virtualenvwrapper is not installed
    # then install it
    # TODO unless we are in an virtual environment already!!
    list_of_pip_packages=$(pip list --format=columns)
    if ! echo "$list_of_pip_packages" | grep  virtualenv --silent; then
    # TODO piping seems to be broken when we are already in a virtual env
    # if ! pip list --format=columns | grep  virtualenv --silent; then
        pip install virtualenvwrapper
    fi
    echo "aaaaaaaaaaaa"
    # Env variables used by virtualenvwrapper
    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$(pwd)

#    if [ -f ~/.local/bin/virtualenvwrapper.sh ]; then
#        export PATH=$PATH:~/.local/bin
#        . ~/.local/bin/virtualenvwrapper.sh
#    elif [ -f /usr/bin/virtualenvwrapper.sh ]; then
#        . /usr/bin/virtualenvwrapper.sh
#    else
#        return 1
#    fi
     . virtualenvwrapper.sh


}

function ShowVirtualEnvHelpMessage {
set -v
# Helpful virtualenvwrapper commands:
#
# https://virtualenvwrapper.readthedocs.io/en/stable/command_ref.html
#
# Managing Environments
#     mkvirtualenv
#     mktmpenv
#     lsvirtualenv
#     showvirtualenv
#     rmvirtualenv
#     cpvirtualenv
#     allvirtualenv
#
# Controlling the Active Environment
#     workon
#     deactivate
set +v
}

function EnterOrCreateVirtualEnv {
    CheckAndSetupBasicPythonEnvironment || return

    if [[ $# -ne 2 ]]; then
        echo >&2 "Illegal number of parameters"
        return 1
    fi

    local VIRTUALENV_NAME="$1"
    local PYTHON="$2"

    echo "ALA123 ${PYTHON}"

    # If particular env has not been created
    # then create it
    if ! lsvirtualenv -b | grep --silent "$VIRTUALENV_NAME"; then # lsvirtualenv -b Brief mode, disables verbose output.
        mkvirtualenv -p $(which "$PYTHON") "$VIRTUALENV_NAME"
    fi

    # Print available virtualenvs
    workon
    # Switch to selelcted virtualenv
    workon "$VIRTUALENV_NAME"

    pip install -r requirements.txt

    ShowVirtualEnvHelpMessage
}


# TODO
# make the shell interacive: https://unix.stackexchange.com/questions/291541/can-i-use-a-shebang-to-have-a-file-source-itself-into-current-bash-environment
# that would fix problems with automated exiting
# just do exec bash -i
