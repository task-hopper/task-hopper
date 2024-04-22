#!/bin/bash


export HOP_REPO="${HOME}/repos/personal/task-hopper-two"
export HOP_VENV="${HOME}/.hop2/venv"


# Main hop function
hop3() {
  case "$1" in
    init)
      if [ "$?" -eq 0 ]; then
        ~/repos/personal/task-hopper-two/bin/init.sh $2
      fi
      ;;
    healthcheck)
      ~/repos/personal/task-hopper-two/bin/healthcheck.sh
      ;;
    *)
      ~/repos/personal/task-hopper-two/bin/healthcheck.sh -s
      if [ "$?" -eq 0 ]; then
        local directive=''
        while IFS= read -r line ; do
          if [[ "$line" =~ ^_{2}hop_{1}[A-Za-z]*_{2}$ ]]; then
            directive="$line"
          else
            if [[ "$directive" == '__hop_message__' ]]; then
              echo -e "$line"
            elif [[ "$directive" == '__hop_task__' ]]; then
              eval "$line" <&1
            elif [[ "$directive" == '__hop_warning__' ]]; then
              local FONT_YELLOW='\033[0;33m'
              local FONT_DEFAULT='\033[0m'
              echo -e "${FONT_YELLOW}${line}${FONT_DEFAULT}"
            elif [[ "$directive" == '__hop_error__' ]]; then
              local FONT_RED='\033[0;31m'
              local FONT_DEFAULT='\033[0m'
              echo -e "${FONT_RED}${line}${FONT_DEFAULT}"
            else
              echo -e 'Invalid command directive'
            fi
          fi
        done < <(${HOP_VENV}/bin/python ${HOP_REPO}/hop $@)
      fi
      ;;
  esac
}


hop3d() {
  ${HOP_VENV}/bin/python ${HOP_REPO}/hop $@
}


_hop3()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [[ ${COMP_CWORD} -eq 1 ]]; then
      hopcommands=$(hop3 -h | awk '/positional arguments:/{flag=1;next}/^$/{flag=0}flag' | cut -d ' ' -f 5)
      COMPREPLY=($(compgen -W "${hopcommands}" -- ${cur}))
      return 0
    fi
}

if [[ $(ps -p$$ -ocmd=) = "zsh" ]]; then
  autoload bashcompinit
  bashcompinit
fi

complete -F _hop3 hop3
