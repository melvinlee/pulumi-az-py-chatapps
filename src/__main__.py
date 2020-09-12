"""An Azure Python Pulumi program"""

import pulumi
from modules import base
from modules import storage
from modules import vnet
from modules import signalr
from modules import zone
from modules import public_ip
from modules import monitoring
from modules import apim
from modules import tags
import waf

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
my_vnet = vnet.VirtualNetwork(name=vnet_name,
                              resource_group_name=my_rg.name,
                              cidr=[vnet_config.get("cidr")],
                              subnets={
                                  "subnets": [{
                                      "name": "frontend-sub",
                                      "address_prefixes": [vnet_config.get("subnet_frontend_cidr")],
                                      "service_endpoints": ["Microsoft.Storage"],
                                      "nsg_security_rules": [
                                          {
                                              "name": "AllowGWM",
                                              "priority": 100,
                                              "direction": "Inbound",
                                              "access": "Allow",
                                              "protocol": "Tcp",
                                              "source_port_range": "*",
                                              "destination_port_range": "65200-65535",
                                              "source_address_prefix": "GatewayManager",
                                              "destination_address_prefix": "*",
                                          },
                                          {
                                              "name": "AllowAzureLoadBalancer",
                                              "priority": 101,
                                              "direction": "Inbound",
                                              "access": "Allow",
                                              "protocol": "Tcp",
                                              "source_port_range": "*",
                                              "destination_port_range": "*",
                                              "source_address_prefix": "AzureLoadBalancer",
                                              "destination_address_prefix": "*",
                                          },
                                          {
                                              "name": "AllowHttp",
                                              "priority": 200,
                                              "direction": "Inbound",
                                              "access": "Allow",
                                              "protocol": "Tcp",
                                              "source_port_range": "*",
                                              "destination_port_range": "80",
                                              "source_address_prefix": "*",
                                              "destination_address_prefix": "*",
                                          },
                                          {
                                              "name": "AllowHttps",
                                              "priority": 201,
                                              "direction": "Inbound",
                                              "access": "Allow",
                                              "protocol": "Tcp",
                                              "source_port_range": "*",
                                              "destination_port_range": "443",
                                              "source_address_prefix": "*",
                                              "destination_address_prefix": "*",
                                          }
                                      ]
                                  },
                                      {
                                      "name": "backend-sub",
                                      "address_prefixes": [vnet_config.get("subnet_backend_cidr")],
                                  }]
                              },
                              tags=my_tags.get_tags())

# Create Azure Blob Static Website
my_website = storage.StaticWebsite(name=website_name,
                                   resource_group_name=my_rg.name,
                                   index_html="wwwroot/index.html",
                                   network_rules={
                                       "default_action": "Allow",
                                       "virtual_network_subnet_ids": [my_vnet.subnets["frontend-sub"].id]
                                   },
                                   tags=my_tags.get_tags({
                                       "network_rules": "yes",
                                       "network_subnet_id": my_vnet.subnets["frontend-sub"].id,
                                   }))

# Create an Azure Standard Public IP
my_pip = public_ip.StandrdPublicIP(name=pip_name,
                                   resource_group_name=my_rg.name,
                                   tags=my_tags.get_tags())

# Create a Public Zone
my_zone = zone.PublicDNS(name=zone_name,
                         resource_group_name=my_rg.name,
                         recordsets=[
                             {
                                 "name": "www",
                                 "record_type": "A",
                                 "ttl": 300,
                                 "target_resource_id": my_pip.public_ip.id
                             },
                             {
                                 "name": "api",
                                 "record_type": "CName",
                                 "ttl": 300,
                                 "record": "contoso.com"
                             }],
                         tags=my_tags.get_tags())

# Create Azure Application Gateway
my_waf = waf.ApplicationGateway(name=waf_name,
                                resource_group_name=my_rg.name,
                                pip_id=my_pip.public_ip.id,
                                subnet_frontend_id=my_vnet.subnets["frontend-sub"].id,
                                subnet_backend_id=my_vnet.subnets["backend-sub"].id,
                                website_host=my_website.account.primary_web_host,
                                la_workspace_id=my_laworkspace.AnalyticsWorkspace.id,
                                tags=my_tags.get_tags())

# Create Azure SignalR Services
my_signalr = signalr.Signalr(name=signalr_name,
                             resource_group_name=my_rg.name,
                             sku={
                                 "name": "Free_F1",
                                 "capacity": 1,
                             },
                             log_analytics={
                                 "log_analytics_workspace_id":  my_laworkspace.AnalyticsWorkspace.id,
                             },
                             tags=my_tags.get_tags())

# Create Azure APIM
my_apim = apim.ApiManagement(name=apim_name,
                             resource_group_name=my_rg.name,
                             apim_config=apim_config,
                             tags=my_tags.get_tags())

# Export Variables
pulumi.export('website_url', "http://www." + zone_name)
pulumi.export("signalr_connection_string",
              my_signalr.service.primary_connection_string)
pulumi.export("signalr_public_port", my_signalr.service.public_port)
pulumi.export("apim_url", my_apim.apimanagement.gateway_url)
pulumi.export("static_website_url", my_website.account.primary_web_endpoint)
