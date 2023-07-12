#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.iac_stack import IacStack


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")
github_ref_name = os.environ.get("GITHUB_REF_NAME")
project_name = os.environ.get("PROJECT_NAME")


tags = {
    'project': project_name,
    'stage': "TEST",
    'stack': 'BACK',
    'owner': 'DevCommunity'
}

IacStack(app, stack_name, env=cdk.Environment(account=aws_account_id, region=aws_region), tags=tags)

app.synth()
