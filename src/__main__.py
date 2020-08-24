"""An Azure Python Pulumi program"""

import pulumi
import base
import storage
import vnet 

# Read local config settings
config = pulumi.Config()
resource_group_name = config.require("resource-group-name")

vnet_config = config.require_object("vnet")
vnet_name = vnet_config.get("name")
vnet_cidr = vnet_config.get("cidr")
vnet_subnet_frontend_cidr= vnet_config.get("subnet_frontend_cidr")
vnet_subnet_backend_cidr= vnet_config.get("subnet_backend_cidr")

tags = {
    "project" : "chatapps",
    "costCenter" : "test1234"
}

# Create an Azure Resource Group
rg = base.ResourceGroup(resource_group_name, tags)

# Create a VirtualNetwork
my_vnet = vnet.VirtualNetwork(vnet_name, rg.name, vnet_cidr, vnet_subnet_frontend_cidr, vnet_subnet_backend_cidr, tags)

# Create Azure Blob Static Website
my_website = storage.StaticWebsite('website',rg.name, tags)

# Export Variables
pulumi.export('website_url', my_website.url)
