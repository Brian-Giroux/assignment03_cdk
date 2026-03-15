#!/usr/bin/env python3
import aws_cdk as cdk

from assignment03_cdk.cdk_lab_network_stack import CdkLabNetworkStack
from assignment03_cdk.cdk_lab_server_stack import CdkLabServerStack

app = cdk.App()
network_stack = CdkLabNetworkStack(app, "CdkLabNetworkStack")

CdkLabServerStack(app, "CdkLabServerStack", cdk_lab_vpc=network_stack.vpc)

app.synth()