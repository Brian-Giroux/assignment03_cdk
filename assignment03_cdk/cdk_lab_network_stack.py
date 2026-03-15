from aws_cdk import (Stack, aws_ec2 as ec2)

from constructs import Construct

class CdkLabNetworkStack(Stack):

    @property
    def vpc(self):
        return self.cdk_lab_vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with one public and one private subnet in each of two AZs.
        # CDK automatically creates and attaches an Internet Gateway for the public subnets
        # and a NAT Gateway so instances in private subnets can reach the internet.
        self.cdk_lab_vpc = ec2.Vpc(self, "cdk_lab_vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
            ]
        )
