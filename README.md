# Vaccine Tracker

## Create key for EC2
`aws ec2 create-key-pair --key-name KeyAlert --query 'KeyMaterial' --output text > key-alert.pem`

## Create EC2 Instance with Cloudformation
`aws cloudformation create-stack --stack-name alertStack --template-body file://template.json --parameters ParameterKey=KeyAlert,ParameterValue=KeyAlert`

## Remove EC2 Instance
`aws cloudformation delete-stack --stack-name alertStack`

## Copy files to EC2 Instance
```
chmod 400 key-alert.pem
scp -i key-alert.pem crawler.py ec2-user@public_ip:~/
scp -i key-alert.pem cron_job ec2-user@public_ip:~/
```

## Login to EC2 Instance or Run Cron Job Remotely
```
ssh -i key-alert.pem ec2-user@public_ip
ssh -i key-alert.pem ec2-user@public_ip "crontab ~/cron_job"
```
