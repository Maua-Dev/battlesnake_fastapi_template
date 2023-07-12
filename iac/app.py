#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.iac_stack import IacStack


app = cdk.App()
IacStack(app, "IacStack")

app.synth()
