#!/bin/bash -xe

PIP3=/usr/bin/pip3.4
cwd=$(dirname "$(readlink -f "$0")")

TARGET_DIR=$cwd/lambda-packages
TEMPLATE_DIR=$cwd/templates

# Remove everything in target dir
rm -rf $TARGET_DIR/*

# Install dependencies for functions
for functiondir in */ ; do

    # Copy function directory to target dir
    cp -r $functiondir $TARGET_DIR

    # Switch to target Lambda function directory
    pushd $TARGET_DIR/$functiondir

        if [ -f requirements.txt ]; then
            # Need to install additional packages
            $PIP3 install -r requirements.txt -t .
        fi

    popd

done

# Packages the Lambda functions and swagger file to S3 ready for deployment, and updates the SAM template
aws cloudformation package --template-file templates/serverless_application.yaml --s3-bucket $LAMBDA_BUCKET --output-template-file serverless-application-output.yaml
