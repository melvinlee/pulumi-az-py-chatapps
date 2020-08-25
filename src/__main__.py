"""An Azure Python Pulumi program"""

import pulumi
import base, storage, vnet, waf, signalr, zone, pip, monitoring

# Read local config settings
config = pulumi.Config()
resource_group_name = config.require("resource-group-name")

vnet_config = config.require_object("vnet")
vnet_name = vnet_config.get("name")
vnet_cidr = vnet_config.get("cidr")
vnet_subnet_frontend_cidr= vnet_config.get("subnet_frontend_cidr")
vnet_subnet_backend_cidr= vnet_config.get("subnet_backend_cidr")

waf_name = config.require("waf-name")
signalr_name = config.require("signalr-name")
pip_name = config.require("pip-name")
zone_name =  config.require("zone-name")
la_name = config.require("la-name")

tags = {
    "project" : "chatapps",
    "costCenter" : "test1234"
}

# Create an Azure Resource Group
rg = base.ResourceGroup(resource_group_name, tags)

# Create an Azure Loganalytics Workspace
my_laworkspace = monitoring.AnalyticsWorkspace(la_name, rg.name, tags)

# Create a VirtualNetwork
my_vnet = vnet.VirtualNetwork(vnet_name, rg.name, vnet_cidr, vnet_subnet_frontend_cidr, vnet_subnet_backend_cidr, tags)

# Create Azure Blob Static Website
my_website = storage.StaticWebsite('website',rg.name, tags)

# Create an Azure Standard Public IP
my_pip = pip.StandrdPublicIP(pip_name, rg.name, tags)

# Create a Public Zone
my_zone = zone.PublicDNS(zone_name, rg.name, my_pip.public_ip_id ,tags)

# Create Azure Application Gateway
my_waf = waf.ApplicationGateway(waf_name, rg.name, my_pip.public_ip_id, my_vnet.frontend_subnet.id, my_vnet.backend_subnet.id, my_website.account.primary_web_host, tags)

# Create SignalR Services
my_signalr = signalr.Service( signalr_name, rg.name, tags)

# Export Variables
pulumi.export('website_url', "http://www." + zone_name)
pulumi.export("signalr_connection_string", my_signalr.primary_connection_string)
pulumi.export("signalr_public_port", my_signalr.public_port)