# AWS Lightsail instance public network IP inspection 

Detect and automatically switch static IPs for instances.

## Environment

Create .env file in the root directory of the project, and add the following content:

```bash
AWS_ACCESS_KEY_ID=<your aws access key id>
AWS_SECRET_ACCESS_KEY=<your aws secret access key>
REGION_NAME=<region of instance>
LIGHTSAIL_INSTANCE_NAME=<instance name>
```

## Usage

```bash
python main.py
```

# Reference
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html