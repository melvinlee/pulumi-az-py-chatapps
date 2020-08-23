#/bin/sh

set -e
source launch.config

instuction()
{
    echo ""
    echo "Welcome to pulumi backend launchpad"
    echo "Usage: launch.sh storage"
    echo
}

if [ $# -lt 1 ]; then
    instuction
    exit 1
fi


if [ "$1" = "storage" ];then

    echo "Launching resources..."
    echo
    echo "Creating resources group ..." 
    az group create -l $AZURE_LOCATION \
                    -n $AZURE_RESOURCEGROUP --output json
    echo 
    echo "Creating backend storage ..." 
    az storage account create \
    --name $AZURE_STORAGE_ACCOUNT \
    --resource-group $AZURE_RESOURCEGROUP \
    --location $AZURE_LOCATION \
    --sku Standard_ZRS \
    --kind StorageV2 --output json
fi