#!/bin/bash
# Packages the Lambda functions ready for deployment to S3

# Python 2's pip
PIP2=/usr/bin/pip2

TARGET_DIR=$PWD/lambda-packages
TEMPLATE_DIR=$PWD/templates
TMP_DIR=$PWD/lambda-packages/tmp

# Remove previous packages
find $TARGET_DIR -type f -name '*.zip' -delete

mkdir -p $TMP_DIR

pushd lambda-functions

for functiondir in */ ; do

    # Copy function directory to temp dir
    cp -r $functiondir $TMP_DIR

    # Switch to temp Lambda function directory
    pushd $TMP_DIR/$functiondir

        if [ -f requirements.txt ]; then
            # Need to install additional packages
            $PIP2 install -r requirements.txt -t .
        fi
        
        # Zip everything apart from egg-info directories
        zip -r $TARGET_DIR/${functiondir%?}.zip . -x \*.egg-info\*

        # Clean up
        rm -rf $TMP_DIR/*

    popd
done

rmdir $TMP_DIR

popd

# Copy swagger file to the package directory so it can be uploaded easily at same time
# @todo - replace region and account id automatically
cp $TEMPLATE_DIR/swagger.yaml $TARGET_DIR

echo "Done! Packages are in $TARGET_DIR ready to be uploaded to S3"
