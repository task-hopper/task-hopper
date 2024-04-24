#!/bin/bash


export HOP_REPO="${HOME}/.hop/repo"
export HOP_VENV="${HOME}/.hop/venv"


# Main hop function
hop() {
  case "$1" in
    init)
      if [ "$?" -eq 0 ]; then
        $HOP_REPO/bin/init.sh $2
      fi
      ;;
    healthcheck)
      $HOP_$REPO/bin/healthcheck.sh
      ;;
    *)
      $HOP_REPO/bin/healthcheck.sh -s
      if [ "$?" -eq 0 ]; then
        # Read the python composition into an array
        lines=()
        while IFS= read -r line; do
          lines+=("$line")
        done < <(${HOP_VENV}/bin/python ${HOP_REPO}/hop "$@")

        local COLOR_YELLOW='\033[0;33m'
        local COLOR_RED='\033[0;31m'
        local COLOR_RESET='\033[0m'

        local directive=''
        for line in "${lines[@]}"; do
          if [[ "$line" =~ ^_{2}hop_{1}[A-Za-z]*_{2}$ ]]; then
            directive="$line"
          else
            if [[ "$directive" == '__hop_eval__' ]]; then
              eval "$line" <&1
            elif [[ "$directive" == '__hop_bash__' ]]; then
              $line
            elif [[ "$directive" == '__hop_python__' ]]; then
              ${HOP_VENV}/bin/python ${HOP_REPO}/hop "th_callback" "$line"
            elif [[ "$directive" == '__hop_info__' ]]; then
              echo -e "$line"
            elif [[ "$directive" == '__hop_warn__' ]]; then
              echo -e "${COLOR_YELLOW}${line}${COLOR_RESET}"
            elif [[ "$directive" == '__hop_error__' ]]; then
              echo -e "${COLOR_RED}${line}${COLOR_RESET}"
            else
              echo $directive
              echo $line
              echo -e 'Invalid command directive'
            fi
          fi
        done
      fi
      ;;
  esac
}


hopd() {
  ${HOP_VENV}/bin/python ${HOP_REPO}/hop $@
}


_hop()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [[ ${COMP_CWORD} -eq 1 ]]; then
      hopcommands=$(hop -h | awk '/positional arguments:/{flag=1;next}/^$/{flag=0}flag' | cut -d ' ' -f 5)
      COMPREPLY=($(compgen -W "${hopcommands}" -- ${cur}))
      return 0
    fi
}

if [[ $(ps -p$$ -ocmd=) = "zsh" ]]; then
  autoload bashcompinit
  bashcompinit
fi

complete -F _hop hop
