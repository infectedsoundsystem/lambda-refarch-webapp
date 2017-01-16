# Lambda-backed CloudFormation Custom Resource to create unauthenticated Cognito identity pools
from __future__ import print_function

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

        self.cognito = boto3.client('cognito-identity', AWS_REGION)
        self.iam = boto3.client('iam', AWS_REGION)

        self.roles = {}

        try:
            self.identity_pool_name = event['ResourceProperties']['IdentityPoolName']
            self.roles['authenticated'] = event['ResourceProperties']['IdentityAuthRoleArn']
            self.roles['unauthenticated'] = event['ResourceProperties']['IdentityUnauthRoleArn']
        except KeyError as e:
            logger.error('Missing IdentityPoolName resource property')
            logger.error(e)
            self.return_status(FAILED)
            return

    def create(self):
        try:
            response = self.cognito.create_identity_pool(
                IdentityPoolName=self.identity_pool_name,
                AllowUnauthenticatedIdentities=True,
            )
            self.physical_resource_id = response['IdentityPoolId']
            self.response_data = {'IdentityPoolId': response['IdentityPoolId']}

            self.cognito.set_identity_pool_roles(
                IdentityPoolId=self.physical_resource_id,
                Roles=self.roles,
            )
            # response = self.cognito.get_identity_pool_roles(
            #     IdentityPoolId=self.physical_resource_id,
            # )
            # unauthenticated_role = response['Roles']['unauthenticated']

            # self.iam.attach_role_policy(
            #     RoleName=unauthenticated_role,
            #     PolicyArn=self.identity_policy_arn,
            # )

            self.return_status(SUCCESS)

        except Exception as e:
            logger.error('Create identity pool failed')
            logger.error(e)
            self.return_status(FAILED)

    def delete(self):
        try:
            self.physical_resource_id = self.event['PhysicalResourceId']
            self.cognito.delete_identity_pool(
                IdentityPoolId=self.physical_resource_id,
            )
            self.return_status(SUCCESS)

        except Exception as e:
            logger.error('Delete identity pool ' + self.physical_resource_id + 'failed')
            logger.error(e)
            self.return_status(FAILED)

    def update(self):
        # Do nothing
        self.return_status(SUCCESS)

    def return_status(self, status):
        send(
            event=self.event,
            context=self.context,
            response_status=status,
            reason=self.reason,
            response_data=self.response_data,
            physical_resource_id=self.physical_resource_id,
        )


def lambda_handler(event, context):
    resource = CustomResource(event, context)
    try:
        getattr(resource, event['RequestType'].lower())()
    except Exception as e:
        send(event, context, FAILED, reason="Invalid RequestType " + event['RequestType'])
