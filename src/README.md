# Introduction 

This repo contains code of using Pulumi to build and deploy cloud applications and infrastructure based on the proposed option 2 as described [here](../PROPOSAL.md) 

## Quick Start

1. Initialiase stack
```sh
pulumi stack init dev
```

2. Create Python venv and install dependencies:
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Setting Variables

```sh
pulumi config set resource-group-name chatapps-rg
pulumi config set zone-name app.com
pulumi config set pip-name chatapps-pip
pulumi config set --path 'vnet.name' chatapp-vnet
pulumi config set --path 'vnet.cidr' 10.0.0.0/16
pulumi config set --path 'vnet.subnet_frontend_cidr' 10.0.0.0/27
pulumi config set --path 'vnet.subnet_backend_cidr' 10.0.1.0/27
pulumi config set waf-name chatapps-waf
pulumi config set signalr-name chatapps-signalr
pulumi config set la-name chatapps-la
```

4. Let’s go ahead and deploy the stack
```sh
pulumi up
```

5. Cleanup
```sh
pulumi destroy
pulumi stack rm dev
```