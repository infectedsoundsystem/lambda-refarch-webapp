#!/bin/bash -xe
# This is specifically for the Python 3 Amazon Linux docker container image used
# by CodeBuild. Will need alterations to run on other distros etc.

yum install -y yum-utils
yum-config-manager --enable epel

yum install -y python34-pip zip

/usr/bin/pip-3.4 install --upgrade awscli
