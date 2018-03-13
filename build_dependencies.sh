#!/bin/bash -xe
# This is specifically for the Python 3 Amazon Linux docker container image used
# by CodeBuild. Will need alterations to run on other distros etc.

yum install -y yum-utils
yum-config-manager --enable epel

yum install -y python34-pip zip

$PIP3 install --upgrade setuptools
$PIP3 install --upgrade awscli
