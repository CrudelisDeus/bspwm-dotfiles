#
# ~/.bashrc
#

# venv
export EDITOR=nvim
export VISUAL=nvim

# alias
alias ls='eza -lah --icons --group-directories-first --time-style=long-iso'
alias cat='bat'
alias top='btop'
alias grep='grep --color=auto'

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '
