from __future__ import print_function

import boto3
import json
import logging
import os

AWS_REGION = os.environ['AWS_REGION']
TABLE_NAME = os.environ['TABLE_NAME']
VOTE_CHOICES = (
    'LOLWUT',
    'PCMR',
    'PEASANT',
)

dynamodb = boto3.client('dynamodb', AWS_REGION)
logger = logging.getLogger()


def lambda_handler(event, context):

    logger.setLevel(logging.INFO if context.invoked_function_arn.endswith('prd') else logging.DEBUG)

    logger.debug(json.dumps(event, indent=4, separators=(',', ': ')))

    totals = {choice: 0 for choice in VOTE_CHOICES}

    records = event.get('Records', [])

    for record in records:

        if 'NewImage' not in record['dynamodb']:
            continue

        voted_for_hash = record['dynamodb']['NewImage']['VotedFor']['S']
        num_votes = record['dynamodb']['NewImage']['Votes']['N']

        # Determine which choice the vote was for & add the votes
        try:
            voted_for = voted_for_hash.split('.')[0]
        except IndexError:
            logger.error('Invalid vote: ' + voted_for_hash)
        else:
            if voted_for in VOTE_CHOICES:
                totals[voted_for] += int(num_votes)
            else:
                logger.error('Invalid vote: ' + voted_for)

    # Update the aggregation table with the votes received for each choice
    for choice, total in totals.iteritems():
        if total < 1:
            continue

        try:
            dynamodb.updateItem(
                TableName=TABLE_NAME,
                Key={
                    'VotedFor': {
                        'S': voted_for,
                    }
                },
                UpdateExpression='add #vote :x',
                ExpressionAttributeNames={
                    '#vote': 'Vote',
                },
                ExpressionAttributeValues={
                    ':x': {
                        'N': str(total),
                    },
                },
            )
        except Exception as e:
            logger.error('Error recording vote in ' + TABLE_NAME)
            logger.error(e)
        else:
            logger.info('Votes received for ' + voted_for)
