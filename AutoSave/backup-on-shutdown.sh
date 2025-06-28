#!/bin/bash

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Use IMDSv2 token method to get instance ID
token=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
       -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

instance_id=$(curl -s -H "X-aws-ec2-metadata-token: $token" \
       http://169.254.169.254/latest/meta-data/instance-id)

filename="backup_${instance_id}_${timestamp}.zip"

# Zip the desired directories
zip -r /tmp/$filename /var/log /home/ubuntu

# Upload to S3
aws s3 cp /tmp/$filename s3://ec2-backup-bucket-b1/backups/

# Optional cleanup
rm /tmp/$filename
