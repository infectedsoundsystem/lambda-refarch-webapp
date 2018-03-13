#!/bin/bash -xe
# Prepare swagger definition by entering region and account id in API Gateway integration

replacements=(
    "\"s#<<region>>#$AWS_REGION#g\""
    "\"s#<<accountId>>#$AWS_ACCOUNT_ID#g\""
)

for exp in "${replacements[@]}"; do
    eval "sed -i -r -e $exp templates/swagger.yaml"
done;
