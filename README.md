## Quick Start

Using Azure Blob for saving pulumi states

1. Install Pulumi https://www.pulumi.com/docs/get-started/install/

2. Install Azure CLI https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest


3. Updating your configuration such resource group and etc.
```sh
vim launch.config
source launch.config
```

4. Create a Azure Blob Container using launchpad

```sh
./launch.sh storage
```

5. Export Azure variables (Azure backend requires setting the environment variables AZURE_STORAGE_ACCOUNT and either AZURE_STORAGE_KEY)
```sh
az storage account keys list-g $RESOURCEGROUP -n $STORAGE_ACCOUNT

export AZURE_STORAGE_KEY=<storage key>
```

6. Login with Pulumi to Azure Storage
```sh 
pulumi login --cloud-url azblob://$AZURE_STORAGE_ACCOUNT
```