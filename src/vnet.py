from pulumi_azure import network


class VirtualNetwork:
    """Create Azure VirtualNetwork"""

    frontend_subnet_id = None
    backend_subnet_id = None

    def __init__(self, name, resource_group_name, cidr, subnet_frontend_cidr, subnet_backend_cidr, tags):
        vnet = network.VirtualNetwork(name,
                                      resource_group_name=resource_group_name,
                                      address_spaces=[
                                          cidr
                                      ],
                                      tags=tags)

        # Create frontend subnet
        frontend_nsg = network.NetworkSecurityGroup("frontend-nsg",
                                                    resource_group_name=resource_group_name,
                                                    security_rules=[
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
                                                        },
                                                        ],
                                                    tags=tags)

        frontend = network.Subnet("frontend",
                                  name="frontend",
                                  resource_group_name=resource_group_name,
                                  virtual_network_name=vnet.name,
                                  address_prefixes=[subnet_frontend_cidr],
                                  service_endpoints=["Microsoft.Storage"])

        # Associate subnet with nsg
        network.SubnetNetworkSecurityGroupAssociation("NetworkSecurityGroupAssociation",
                                                      subnet_id=frontend.id,
                                                      network_security_group_id=frontend_nsg.id)

        # Create backend subnet
        backend = network.Subnet("backend",
                                 name="backend",
                                 resource_group_name=resource_group_name,
                                 virtual_network_name=vnet.name,
                                 address_prefixes=[subnet_backend_cidr])

        # Export Subnets Id
        self.frontend_subnet_id = frontend.id
        self.backend_subnet_id = backend.id
