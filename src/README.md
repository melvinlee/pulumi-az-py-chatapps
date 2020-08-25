# Introduction 

This repo contains code of using Pulumi to build and deploy cloud applications and infrastructure based on the proposed option 2 as described [here](../doc/PROPOSAL.md) 

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

3. Setting Azure Location
```sh
pulumi config set azure:environment public
pulumi config set azure:location SoutheastAsia
```

4. Setting Variables

```sh
pulumi config set resource-group-name chatapps-rg
pulumi config set website-name chatppswebsite
pulumi config set zone-name app.com
pulumi config set pip-name chatapps-pip
pulumi config set --path 'vnet.name' chatapp-vnet
pulumi config set --path 'vnet.cidr' 10.0.0.0/16
pulumi config set --path 'vnet.subnet_frontend_cidr' 10.0.0.0/27
pulumi config set --path 'vnet.subnet_backend_cidr' 10.0.1.0/27
pulumi config set waf-name chatapps-waf
pulumi config set signalr-name chatapps-signalr
pulumi config set la-name chatapps-la
pulumi config set --path 'apim.name' chatapps-apim
pulumi config set --path 'apim.publisher_name' app-developer
pulumi config set --path 'apim.publisher_email' chat@app.com
pulumi config set cost-center 882233
```

5. Let’s go ahead and deploy the stack
```sh
pulumi up
```

[![asciicast](https://asciinema.org/a/355386.svg)](https://asciinema.org/a/355386)

6. Cleanup
```sh
pulumi destroy
pulumi stack rm dev
```


## TODO
1. To create Azure Function
2. To deploy APIM inside VNET
3. To configure API endpoint, access policies, developer portal, and etc.
4. Landing Zone - Refactor module into multi-stack