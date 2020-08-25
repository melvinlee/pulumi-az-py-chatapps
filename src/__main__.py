"""An Azure Python Pulumi program"""

import pulumi
import base, storage, vnet, waf, signalr, zone, pip, monitoring, apim, tags

# Read local config settings
config = pulumi.Config()
resource_group_name = config.require("resource-group-name")
website_name = config.require("website-name")
waf_name = config.require("waf-name")
signalr_name = config.require("signalr-name")
pip_name = config.require("pip-name")
zone_name =  config.require("zone-name")
la_name = config.require("la-name")

# VNET config object
vnet_config = config.require_object("vnet")
vnet_name = vnet_config.get("name")

# APIM config object
apim_config = config.require_object("apim")
apim_name = apim_config.get("name")

# Create an Azure Resource Group
rg = base.ResourceGroup(resource_group_name, tags.get_tags())

# Create an Azure Loganalytics Workspace
my_laworkspace = monitoring.AnalyticsWorkspace(la_name, rg.name, tags.get_tags())

# Create a VirtualNetwork
my_vnet = vnet.VirtualNetwork(vnet_name, rg.name, vnet_config, tags.get_tags())

# Create Azure Blob Static Website
my_website = storage.StaticWebsite(website_name,rg.name, tags.get_tags())

# Create an Azure Standard Public IP
my_pip = pip.StandrdPublicIP(pip_name, rg.name, tags.get_tags())

# Create a Public Zone
my_zone = zone.PublicDNS(zone_name, rg.name, my_pip.public_ip_id ,tags.get_tags())

# Create Azure Application Gateway
my_waf = waf.ApplicationGateway(waf_name, rg.name, my_pip.public_ip_id, my_vnet.frontend_subnet.id, my_vnet.backend_subnet.id, my_website.account.primary_web_host, my_laworkspace.AnalyticsWorkspace.id, tags.get_tags())

# Create Azure SignalR Services
my_signalr = signalr.Service(signalr_name, rg.name, my_laworkspace.AnalyticsWorkspace.id, tags.get_tags())

# Create Azure APIM
# my_apim = apim.ApiManagement(apim_name, rg.name, apim_config, tags.get_tags())

# Export Variables
pulumi.export('website_url', "http://www." + zone_name)
pulumi.export("signalr_connection_string", my_signalr.service.primary_connection_string)
pulumi.export("signalr_public_port", my_signalr.service.public_port)
# pulumi.export("apim_url", my_apim.apimanagement.gateway_url)
pulumi.export("static_website_url", my_website.account.primary_web_endpoint)