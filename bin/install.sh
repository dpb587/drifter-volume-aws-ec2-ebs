#!/bin/bash

set -e

echo $PWD

apt-get update

if ! (which python 1>/dev/null 2>&1) ; then
  apt-get -y install python
fi

if ! (which pip 1>/dev/null 2>&1) ; then
  apt-get -y install python-pip
fi

pip install --upgrade -r requirements.txt
