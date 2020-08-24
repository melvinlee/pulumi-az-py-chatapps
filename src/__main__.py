"""An Azure Python Pulumi program"""

import pulumi
import base
import storage

# Read local config settings
config = pulumi.Config()
resource_group_name = config.require("resource-group-name")
tags = {
    "project" : "chatapps",
    "costCenter" : "test1234"
}

# Create an Azure Resource Group
rg = base.ResourceGroup(resource_group_name, tags)

# Create Azure Blob Static Website
website = storage.StaticWebsite('website',rg.name, tags)

# Export Variables
pulumi.export('website_url', website.url)