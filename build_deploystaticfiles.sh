#!/bin/bash -xe 

aws s3 sync --delete --exclude "*" --include "*.css" --include "*.html" --include "*.js" static/ s3://${WEBSITE_BUCKET}/
