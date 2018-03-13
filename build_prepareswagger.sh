#!/bin/bash -xe
# Prepare swagger definition by entering region and account id in API Gateway integration

replacements=(
    "\"s#<<region>>#$AWS_REGION#g\""
    "\"s#<<accountId>>#$AWS_ACCOUNT_ID#g\""
    "\"s#<<timestamp>>#$(date +%s)#g\""
)

for exp in "${replacements[@]}"; do
    eval "sed -i -r -e $exp templates/swagger.yaml"
    eval "sed -i -r -e $exp templates/serverless_application.yaml"
done;
