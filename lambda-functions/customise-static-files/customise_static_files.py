# Lambda-backed CloudFormation Custom Resource to customise the Vote App static files
import boto3

from cfnresponse import FAILED, send, SUCCESS

import json
import logging
import os

AWS_REGION = os.environ['AWS_REGION']

logger = logging.getLogger()


class CustomResource(object):

    reason = None
    response_data = None
    physical_resource_id = None

    def __init__(self, event, context):
        self.event = event
        self.context = context

        logger.setLevel(logging.INFO if self.context.invoked_function_arn.endswith('prd') else logging.DEBUG)

        logger.debug(json.dumps(event, indent=4, separators=(',', ': ')))

        self.s3_resource = boto3.resource('s3', AWS_REGION)
        self.apigateway = boto3.client('apigateway', AWS_REGION)

        self.replacements = {
            '<your-region-here>': AWS_REGION,
        }

        try:
            self.replacements['<your-identity-pool-id-here>'] = event['ResourceProperties']['IdentityPoolId']
            self.replacements['<your-vote-aggregate-table-name-here>'] = event['ResourceProperties']['VoteAggregateTable']
            self.api_id = event['ResourceProperties']['ApiGatewayId']
            self.bucket = event['ResourceProperties']['S3Bucket']
            self.key = event['ResourceProperties']['S3Key']
        except KeyError as e:
            logger.error('Missing resource property')
            logger.error(e)
            self.return_status(FAILED)
            return

    def create(self):
        try:
            # Build API Gateway endpoint
            endpoint = 'https://' + self.api_id + '.execute-api.' + AWS_REGION + '.amazonaws.com/Prod/vote'
            self.replacements['<your-api-gateway-endpoint-here>'] = endpoint

            self.s3_resource.meta.client.download_file(
                self.bucket,
                self.key,
                '/tmp/' + self.key,
            )

            # Replace the placeholders with the provided values
            with open('/tmp/' + self.key) as input_file, open('/tmp/outputfile', 'w') as output_file:
                for line in input_file:
                    for find, replace_with in self.replacements.items():
                        line = line.replace(find, replace_with)
                    output_file.write(line)

            self.s3_resource.meta.client.upload_file(
                '/tmp/outputfile',
                self.bucket,
                self.key,
            )

            self.return_status(SUCCESS)

        except Exception as e:
            logger.error('Modifying the static files failed')
            logger.error(e)
            self.return_status(FAILED)

    def delete(self):
        # Do nothing
        self.return_status(SUCCESS)

    def update(self):
        # Do nothing
        self.return_status(SUCCESS)

    def return_status(self, status):
        send(
            event=self.event,
            context=self.context,
            responseStatus=status,
            responseData=self.response_data,
            physicalResourceId=self.physical_resource_id,
        )


def lambda_handler(event, context):
    resource = CustomResource(event, context)
    try:
        getattr(resource, event['RequestType'].lower())()
    except Exception as e:
        send(
            event=event,
            context=context,
            responseStatus=FAILED,
            responseData=None,
        )
