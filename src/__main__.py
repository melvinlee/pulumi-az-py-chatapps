"""An Azure Python Pulumi program"""

import pulumi
import base
import storage
import vnet
import waf
import signalr
import zone
import pip
import monitoring
import apim
import tags

# Read local config settings
config = pulumi.Config()
resource_group_name = config.require("resource-group-name")
website_name = config.require("website-name")
waf_name = config.require("waf-name")
signalr_name = config.require("signalr-name")
pip_name = config.require("pip-name")
zone_name = config.require("zone-name")
la_name = config.require("la-name")

# VNET config object
vnet_config = config.require_object("vnet")
vnet_name = vnet_config.get("name")

# APIM config object
apim_config = config.require_object("apim")
apim_name = apim_config.get("name")

# Create an tags object
my_tags = tags.Tags({"purpose": "demo"})

# Create an Azure Resource Group
my_rg = base.ResourceGroup(name=resource_group_name,
                            tags=my_tags.get_tags())

# Create an Azure Loganalytics Workspace
my_laworkspace = monitoring.AnalyticsWorkspace(name=la_name,
                                               resource_group_name=my_rg.name,
                                               retention_in_days=35,
                                               tags=my_tags.get_tags())

# Create a VirtualNetwork
my_vnet = vnet.VirtualNetwork(vnet_name, my_rg.name, vnet_config, my_tags.get_tags())

# Create Azure Blob Static Website
my_website = storage.StaticWebsite(name=website_name,
                                   resource_group_name=my_rg.name,
                                   index_html="wwwroot/index.html",
                                   network_rules={
                                       "default_action": "Allow",
                                       "virtual_network_subnet_ids": [my_vnet.frontend_subnet.id]
                                   },
                                   tags=my_tags.get_tags({"network_rules": "yes"}))

# Create an Azure Standard Public IP
my_pip = pip.StandrdPublicIP(pip_name, my_rg.name, my_tags.get_tags())

# Create a Public Zone
my_zone = zone.PublicDNS(
    zone_name, my_rg.name, my_pip.public_ip_id, my_tags.get_tags())

# Create Azure Application Gateway
my_waf = waf.ApplicationGateway(waf_name, my_rg.name, my_pip.public_ip_id, my_vnet.frontend_subnet.id, my_vnet.backend_subnet.id, my_website.account.primary_web_host, my_laworkspace.AnalyticsWorkspace.id, my_tags.get_tags())

# Create Azure SignalR Services
my_signalr = signalr.Service(signalr_name, my_rg.name, my_laworkspace.AnalyticsWorkspace.id, my_tags.get_tags())

# Create Azure APIM
my_apim = apim.ApiManagement(apim_name, my_rg.name, apim_config, my_tags.get_tags())

# Export Variables
pulumi.export('website_url', "http://www." + zone_name)
pulumi.export("signalr_connection_string", my_signalr.service.primary_connection_string)
pulumi.export("signalr_public_port", my_signalr.service.public_port)
pulumi.export("apim_url", my_apim.apimanagement.gateway_url)
pulumi.export("static_website_url", my_website.account.primary_web_endpoint)