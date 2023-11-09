# Amazon Lightsail instance public network IP inspection 

* 🚀 Initialize an Amazon Lightsail instance. 
* 😎 Procure a static IP and link it with the corresponding instance. 
* 🎯 Register a distinct domain name and delegate subdomains to direct traffic towards your Lightsail assets. 
* 🎉 You are now able to access your assets via the registered domain name.

🔍 This application consistently conducts active surveillance on the specified port of the instance. 🚫If access is obstructed, it will renew the static IP of the instance ⚡ and update the domain name record 🔄.

## Environment

Create .env file in the root directory of the project, and add the following content:

```bash
AWS_ACCESS_KEY_ID=<your aws access key id>
AWS_SECRET_ACCESS_KEY=<your aws secret access key>
REGION_NAME=<region of instance>
LIGHTSAIL_INSTANCE_NAME=<instance name>
LIGHTSAIL_INSTANCE_PORT=<port for inspection>
DOMAIN_ENTRY_NAME=<your domain>
```

## Usage

```bash
python main.py
```

# Reference
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html