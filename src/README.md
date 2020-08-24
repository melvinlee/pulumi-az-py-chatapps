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