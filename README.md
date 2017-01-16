# Serverless Reference Architecture: Web Applications

---

Fork of the original version of [lambda-refarch-webapp](https://github.com/awslabs/lambda-refarch-webapp) as it was at [commit ceda53fc23](https://github.com/awslabs/lambda-refarch-webapp/tree/ceda53fc23f97df8acca5503140f128670a68890). This fork has the following changes: 

- uses voting via the web page rather than via SMS
- uses the Python runtime for all Lambda functions
- uses YAML for the CloudFormation templates
- uses the [AWS Serverless Application Model](https://github.com/awslabs/serverless-application-model)
- uses a Lambda-backed custom resource to create/configure the Cognito Identity Pool
- uses a Lambda-backed custom resource to automatically set appropriate values in refresh.js (AWS region, Cognito Identity Pool id, API Gateway endpoint, DynamoDB table name)
- includes a script to package the Lambda functions
- everything automated apart from uploading the required files to S3
- the voting topic has been changed to something much more likely to incite a flame war ;)

---

Serverless Reference Architecture illustrating how to build dynamic web applications using [AWS Lambda](http://aws.amazon.com/lambda/) and Amazon API Gateway to authenticate and process API requests.

By combining AWS Lambda with other AWS services, developers can build powerful web applications that automatically scale up and down and run in a highly available configuration across multiple data centers&mdash;with zero administrative effort required for scalability, backups, or multi–data center redundancy.

This example looks at using AWS Lambda and Amazon API Gateway to build a dynamic voting application, which receives votes via web requests, aggregates the totals into Amazon DynamoDB, and uses Amazon Simple Storage Service (Amazon S3) to display the results in real time.

A similar architecture to that described in this [diagram](https://s3.amazonaws.com/awslambda-reference-architectures/web-app/lambda-refarch-webapp.pdf) can be created with AWS CloudFormation templates, one of which uses the [AWS Serverless Application Model](https://github.com/awslabs/serverless-application-model).

[The base template](https://@TODO) does the following:

- Creates an S3 bucket to hold your web app's static files
- Creates a Route 53 resource record set to point your chosen subdomain to the S3 website endpoint
- Creates an S3 bucket to hold Lambda packages for deployment


[The serverless application template](https://@TODO) does the following:
:
- Creates a DynamoDB table to store votes
- Creates a DynamoDB table to aggregate vote totals
- Creates a Lambda function that allows your application to receive votes
- Creates an API Gateway endpoint for votes to be proxied to this Lambda function
- Creates a Lambda function that aggregates the votes from a DynamoDB Stream
- Creates a Lambda-backed custom resource that creates a Cognito Identity Pool and configures it with appropriate IAM Roles
- Creates a Lambda-backed custom resource that automatically sets appropriate values in refresh.js (AWS region, Cognito Identity Pool id, API Gateway endpoint, DynamoDB table name)

## Dynamic Dashboard

The services and resources configured by the AWS CloudFormation templates can be tested with the HTML page `index.html`, which relies on the HTML, JavaScript, and CSS files found in this repo.

## Instructions

This example demonstrates receiving votes a web page and displaying the vote totals.

Step 1 – Create an AWS CloudFormation stack using the base.yaml template in the templates/ directory. You'll need to enter:

- The name of an existing Route 53 hosted zone (e.g. example.com)
- The id of that hosted zone
- The subdomain that you want to use (e.g. for vote.example.com just enter the hostname: 'vote')

Step 2 - Upload the contents of the static/ directory to the S3 bucket created with the FQDN from the last step (e.g. a bucket called 'vote.example.com'). This is where your static files are served from.

Step 3 - Run package.sh to create the Lambda packages. Edit swagger.yaml in the lambda-packages/ directory so it has your AWS Region and Account Id in the marked places, then upload the contents of the lambda-packages/ directory (including swagger.yaml) to your Lambda packages S3 bucket (e.g. the bucket created called vote-lambda-packages.example.com)

Step 4 - Create an AWS CloudFormation change set for a new stack using the serverless_application.yaml template in the templates/ directory. (Note: edit this template first to correct the S3 URI values in each *CodeUri*)

Congratulations! You now should have a working example of the reference architecture. Now go to the site (e.g. at http://vote.example.com) to see it in action.

You are able to receive votes in real time, tune your DynamoDB table to handle various levels of incoming traffic, and watch your results change on your dashboard in real time!


## Cleanup

To remove all automatically created resources, delete the AWS CloudFormation stacks in reverse order.

Note: Deletion of the S3 buckets will fail unless all files in the bucket are removed before the stack is deleted.

## License

This reference architecture sample is licensed under Apache 2.0.
