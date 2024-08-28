#!/usr/bin/env -S just --justfile
# just reference  : https://just.systems/man/en/

set quiet := true

alias default := plot

plot:
    mise run --timings plot:fig1
    mise run --timings plot:fig2
    mise run --timings plot:fig3
    mise run --timings plot:fig4

[unix]
install-uv:
    mise run install-uv:unix

[windows]
install-uv:
    mise run install-uv:windows
    @echo "Please see https://docs.astral.sh/uv/getting-started/installation/ for installation instructions."
