#!/bin/bash

if [[ -z "${BRIEF_PERIOD}" ]]; then
  DAY="1"
else
  DAY="${BRIEF_PERIOD}"
fi

if [ $(expr $(date +%s) / 86400 % $DAY) -eq 0 ]; then
       exec /code/main.py
fi

