import boto3
import requests
import time
def createSG(sgName,sgDesc):
    ec2 = boto3.client('ec2')    #creating resources
    res = ec2.create_security_group (
        GroupName = sgName,
        Description = sgDesc
    )
    res2 = ec2.authorize_security_group_ingress(
        GroupId=res["GroupId"],
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/32',
                        'Description': 'SSH access from anywhere',
                    },
                ],
                'ToPort': 22,
            },
        ],
    )
def createKeyPair(name):
    ec2 = boto3.resource('ec2')
    res = ec2.create_key_pair(KeyName = name)
    with open("key_pair.pem", "w") as file:
        file.write(res.key_material)
def createEC2(amiId, keyName, sgName, instType = 't1.micro', minInst = 1, maxInst =
1):
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances (
        ImageId = amiId,
        MinCount = minInst,
        MaxCount = maxInst,
        InstanceType = instType,
        KeyName = keyName,
        SecurityGroups=[sgName]
    )
    host = instances[0]
    while host.state['Name'] == 'pending':
        print("Reload")
        time.sleep(1)
        host.load()
    print(instances[0].public_dns_name)
if __name__ == '__main__':
    sgName = 'securityGroupForDemo'
    sgDesc = 'This is a security group for demo'
    keyName = 'demo-key'
    amiId = 'ami-06b263d6ceff0b3dd'
    #createSG(sgName, sgDesc)
    #createKeyPair(keyName)
    createEC2(amiId, keyName, sgName)