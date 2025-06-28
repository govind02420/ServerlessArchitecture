import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop', 'Auto-Start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped']
            }
        ]
    )

    auto_stop_ids = []
    auto_start_ids = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            action = tags.get('Action')

            if action == 'Auto-Stop' and instance['State']['Name'] == 'running':
                auto_stop_ids.append(instance_id)
            elif action == 'Auto-Start' and instance['State']['Name'] == 'stopped':
                auto_start_ids.append(instance_id)

    if auto_stop_ids:
        ec2.stop_instances(InstanceIds=auto_stop_ids)
        print(f"Stopped instances: {auto_stop_ids}")

    if auto_start_ids:
        ec2.start_instances(InstanceIds=auto_start_ids)
        print(f"Started instances: {auto_start_ids}")
