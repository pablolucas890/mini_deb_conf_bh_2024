#!/bin/sh -e

echo "Creating ${1%.data}.dict and ${1%.data}.index"

dictfmt -p \
        --allchars \
        --utf8 \
        --columns 0 \
        -u "http://www.chat.ru/~mueller_dic" \
        -s "Mueller English-Russian Dictionary$3" \
        --without-time \
        "${1%.data}" < "$1"
