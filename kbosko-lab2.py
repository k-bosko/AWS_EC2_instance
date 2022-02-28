'''
Author: Katerina Bosko
CS6620 Lab2: use the python AWS SDK to programmatically provision a virtual machine (VM) in a VPC,
             securely connect to it, and install a web server
'''

import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
CIDR_VPC = '10.0.0.0/16'
CIDR_PUBLIC_SUBNET = '10.0.0.0/24'
IP_FOR_SSHACESS = '23.118.50.228/32'

VPC_TAG_VALUE = 'cs6620-lab2-vpc'
INTERNET_GATEWAY_TAG_VALUE = 'cs6620-lab2-internet-gateway'
SUBNET_TAG_VALUE = 'cs6620-lab2-subnet'
ROUTE_TABLE_TAG_VALUE = 'cs6620-lab2-route-table'
SECURITY_GROUP_TAG_VALUE = 'cs6620-lab2-security-group'
INSTANCE_TAG_VALUE = 'cs6620-lab2-Linux-10GB-instance'
VOLUME_TAG_VALUE = 'cs6620-lab2-volume-10GB'

#Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
IMAGE_ID = 'ami-033b95fb8079dc481'
INSTANCE_TYPE = 't2.micro'

KEY_NAME = 'my-key-pair'
DEVICE = '/dev/xvda'

VOLUME_SIZE = 10


def get_custom_vpc_id(client):
    '''
    Searches for existing VPC based on its tag value and CIDR block
    If found, returns VPC id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_vpcs(
            Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            VPC_TAG_VALUE,
                        ]
                    },
                    {
                        'Name': 'cidr-block-association.cidr-block',
                        'Values': [
                            CIDR_VPC
                        ]
                    },
                ]
        )
        if response['Vpcs']:
            vpc_id = response['Vpcs'][0]['VpcId']
            print(f'Custom VPC exists. ID={vpc_id}')
            return vpc_id
    except ClientError:
        print('Failed while searching for existing VPC')
        raise
    else:
        return response['Vpcs']


def get_custom_subnet_id(client):
    '''
    Searches for existing subnet on a given VPC based on its tag value
    If found, returns subnet id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        SUBNET_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['Subnets']:
            subnet_id = response['Subnets'][0]['SubnetId']
            print(f'Custom subnet exists. ID={subnet_id}')
            return subnet_id
    except ClientError:
        print('Failed while searching for existing subnet')
        raise
    else:
        return response['Subnets']

def get_custom_internet_gateway(client):
    '''
    Searches for existing internet gateway on a given VPC based on its tag value
     If found, returns internet gateway id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_internet_gateways(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        INTERNET_GATEWAY_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['InternetGateways']:
            internet_gateway_id = response['InternetGateways'][0]['InternetGatewayId']
            print(f'Custom internet gateway exists. ID={internet_gateway_id}')
            return internet_gateway_id
    except ClientError:
        print('Failed while searching for existing internet gateway')
        raise
    else:
        return response['InternetGateways']

def get_custom_route_table(client):
    '''
    Searches for existing route table on a given VPC based on its tag value
    If found, returns route table id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_route_tables(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        ROUTE_TABLE_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['RouteTables']:
            route_table_id = response['RouteTables'][0]['RouteTableId']
            print(f'Custom route table exists. ID={route_table_id}')
            return route_table_id
    except ClientError:
        print('Failed while searching for existing route table')
        raise
    else:
        return response['RouteTables']

def get_custom_security_group(client):
    '''
    Searches for existing security group on a given VPC based on its tag value
    If found, returns security group id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_security_groups(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        SECURITY_GROUP_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['SecurityGroups']:
            security_group_id = response['SecurityGroups'][0]['GroupId']
            print(f'Custom security group exists. ID={security_group_id}')
            return security_group_id
    except ClientError:
        print('Failed while searching for existing security group')
        raise
    else:
        return response['SecurityGroups']


def create_custom_vpc(client):
    '''
    Creates a custom VPC with specified configuration
    Returns VPC id
    '''
    try:
        vpc = client.create_vpc(CidrBlock=CIDR_VPC,
                        InstanceTenancy='default',
                        TagSpecifications=[
                            {
                                'ResourceType': 'vpc',
                                'Tags': [
                                    {
                                        'Key': 'Name',
                                        'Value': VPC_TAG_VALUE
                                    },
                                ]
                            },
                        ]
        )
        print(f'Created VPC with id={vpc.id}')
    except ClientError:
        print('Failed to create custom VPC')
        raise
    else:
        return vpc.id

def create_custom_subnet(client, vpc_id):
    '''
    Creates a subnet in the specified VPC
    Returns subnet id
    '''
    try:
        subnet = client.create_subnet(
            CidrBlock = CIDR_PUBLIC_SUBNET,
            VpcId = vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': SUBNET_TAG_VALUE
                        },
                    ]
                },
            ],
        )
        subnet_id = subnet['Subnet']['SubnetId']
        print(f'Created subnet={subnet_id} on VPC={vpc_id}')
    except ClientError:
        print('Failed to create subnet on specified VPC')
        raise
    else:
        return subnet_id


def create_and_attach_internet_gateway(client, vpc_id):
    '''
    Creates and attaches internet gateway to a specified VPC
    Return internet gateway id
    '''
    try:
        internet_gateway = client.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': INTERNET_GATEWAY_TAG_VALUE
                        },
                    ]
                },
            ],
        )
        internet_gateway_id = internet_gateway['InternetGateway']['InternetGatewayId']
        print(f'Created internet gateway with id={ internet_gateway_id }')
    except ClientError:
        print('Failed to create internet gateway')
        raise

    try:
        client.attach_internet_gateway(
            InternetGatewayId=internet_gateway_id,
            VpcId=vpc_id,
        )
        print(f'Successfully attached internet gateway to VPC')
    except ClientError:
        print('Failed to attach internet gateway')
        raise
    else:
        return internet_gateway_id

def associate_route_table_with_subnet(client, vpc_id, internet_gateway_id, subnet_id):
    '''
    Retrieves a main route table for the specified VPC,
    Creates a route in the main route table that points all traffic (0.0.0.0/0) to the internet gateway,
    Associates it with the specified subnet
    '''
    try:
        response = client.describe_route_tables(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ],
        )
        route_table_id = response['RouteTables'][0]['Associations'][0]['RouteTableId']
        print(f'Retrieved route table id={route_table_id}')
    except ClientError:
        print('Failed to retrieve route table')
        raise

    try:
        route = client.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=internet_gateway_id,
            RouteTableId=route_table_id,
        )
        print(f'Route 0.0.0.0/0 created')
    except ClientError:
        print('Failed to create route 0.0.0.0/0')

    try:
        response = client.associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id,
        )
        print(f'Subnet with id={subnet_id} is associated with custom route table id={route_table_id}')
    except ClientError:
        print('Failed to associate route table with given subnet')

def create_security_group(client, vpc_id):
    '''
    Creates security group on a given VPC,
    Authorizes SSH access for a specified IP address
    Authorizes HTTP access
    '''
    try:
        response = client.create_security_group(
            Description='Security group for SSH and HTTP access',
            GroupName='HTTPandSSHAccess',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': SECURITY_GROUP_TAG_VALUE
                        },
                    ]
                },
            ],
        )
        security_group_id = response['GroupId']
        print(f'Created security group with ID={security_group_id}')
    except ClientError:
        print('Failed to create security group')

    return security_group_id

def authorize_for_SSH_and_HTTP_access(client, security_group_id):
    '''

    '''
    try:
        client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [
                        {
                            'CidrIp': IP_FOR_SSHACESS,
                            'Description': 'SSH access from my IP address',
                        },
                    ],
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0'
                        }
                    ],
                }
            ],
        )
        print('Authorized SSH and HTTP access')
    except ClientError:
        print('Failed to authorize')
        raise

def create_custom_instance(resource, security_group_id, subnet_id):
    '''
    Creates custom EC2 instance with specified configurations
    '''
    try:
        with open('apache-web-server.sh', 'r') as fp:
            script=fp.read()

        instance = resource.create_instances(
            BlockDeviceMappings=[
                        {
                            'DeviceName': DEVICE,
                            'Ebs': {
                                'DeleteOnTermination': False,
                                'VolumeSize': 10,
                                'VolumeType': 'gp2',
                                'Encrypted': False
                            },
                        },
                    ],
            ImageId = IMAGE_ID,
            MinCount = 1,
            MaxCount = 1,
            InstanceType = INSTANCE_TYPE,
            KeyName = KEY_NAME,
            UserData=script,
            NetworkInterfaces=[
                        {
                            'AssociatePublicIpAddress': True,
                            'DeleteOnTermination': True,
                            'DeviceIndex': 0,
                            'Groups': [
                                security_group_id,
                            ],
                            'SubnetId': subnet_id,
                        },
                    ],
            TagSpecifications=[
                    {
                        'ResourceType': 'volume',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': VOLUME_TAG_VALUE
                            },
                        ]
                    },
                                        {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': INSTANCE_TAG_VALUE
                            },
                        ]
                    },
                ],
        )
        print(f'Created instance with ID: {instance[0].id}')
    except ClientError:
        print('Failed to create custom EC2 instance')
        raise
    else:
        return instance


def main():
    # create EC2 client and VPC
    resource = boto3.resource('ec2', region_name=AWS_REGION)
    client = boto3.client('ec2', region_name=AWS_REGION)

    vpc_id = get_custom_vpc_id(client)
    if not vpc_id:
        vpc_id = create_custom_vpc(resource)

    # create public subnet within VPC
    subnet_id = get_custom_subnet_id(client)
    if not subnet_id:
        subnet_id = create_custom_subnet(client, vpc_id)

    # create internet gateway and attach to custom VPC
    internet_gateway_id = get_custom_internet_gateway(client)
    if not internet_gateway_id:
        internet_gateway_id = create_and_attach_internet_gateway(client, vpc_id)

    # create route table, route and associate it with subnet
    route_table_id = get_custom_route_table(client)
    if not route_table_id:
        associate_route_table_with_subnet(client, vpc_id, internet_gateway_id, subnet_id)

    security_group_id = get_custom_security_group(client)
    if not security_group_id:
        security_group_id = create_security_group(client, vpc_id)
        authorize_for_SSH_and_HTTP_access(client, security_group_id)

    # create EC2 instance
    ec2_instance = create_custom_instance(resource, security_group_id, subnet_id)



if __name__ == '__main__':
    main()



