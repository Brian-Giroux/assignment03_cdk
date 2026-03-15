import os.path

from aws_cdk.aws_s3_assets import Asset as S3asset

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_rds as rds,
    RemovalPolicy,
)

from constructs import Construct

dirname = os.path.dirname(__file__)

class CdkLabServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_lab_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Security Groups
        web_sg = ec2.SecurityGroup(self, "WebServerSG", vpc=cdk_lab_vpc)
        web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))

        rds_sg = ec2.SecurityGroup(self, "RdsSG", vpc=cdk_lab_vpc)
        rds_sg.add_ingress_rule(web_sg, ec2.Port.tcp(3306))

        # IAM Role
        instance_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Asset script
        webinitscriptasset = S3asset(self, "Asset", path=os.path.join(dirname, "configure.sh"))

        # Web Server 1 (AZ 1)
        web_instance_1 = ec2.Instance(self, "WebServer1",
            vpc=cdk_lab_vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC, availability_zones=[cdk_lab_vpc.availability_zones[0]]),
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            role=instance_role,
            security_group=web_sg
        )
        asset_path_1 = web_instance_1.user_data.add_s3_download_command(bucket=webinitscriptasset.bucket, bucket_key=webinitscriptasset.s3_object_key)
        web_instance_1.user_data.add_execute_file_command(file_path=asset_path_1)
        webinitscriptasset.grant_read(web_instance_1.role)

        # Web Server 2 (AZ 2)
        web_instance_2 = ec2.Instance(self, "WebServer2",
            vpc=cdk_lab_vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC, availability_zones=[cdk_lab_vpc.availability_zones[1]]),
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            role=instance_role,
            security_group=web_sg
        )
        asset_path_2 = web_instance_2.user_data.add_s3_download_command(bucket=webinitscriptasset.bucket, bucket_key=webinitscriptasset.s3_object_key)
        web_instance_2.user_data.add_execute_file_command(file_path=asset_path_2)
        webinitscriptasset.grant_read(web_instance_2.role)

        # RDS MySQL
        rds.DatabaseInstance(self, "MySQLInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
            vpc=cdk_lab_vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups=[rds_sg],
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            removal_policy=RemovalPolicy.DESTROY,
            delete_automated_backups=True
        )