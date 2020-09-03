import pulumi
from pulumi_azure import network


class VirtualNetwork:
    """Create Azure VirtualNetwork
    ## Example Usage

    ```python
    import vnet

    vnet = network.VirtualNetwork(name="example_name",
                                    resource_group_name="example_group_name",
                                    cird = "10.0.0.0/16",
                                    "subnets": [{
                                      "name": "frontend-sub",
                                      "address_prefixes": ["10.0.0.0/27"],
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
                                          }
                                        ]
                                    },
                                        {
                                            "name": "backend-sub",
                                            "address_prefixes": ["10.0.1.0/27"],
                                        }]
                                    },
                                    tags={
                                        "environment": "Production",
                                    })
    ```
    """

    def __init__(self, name: str, resource_group_name: str, cidr: list, subnets: dict, tags: dict = None, opts: pulumi.ResourceOptions = None):
        """
        :param name: The name of the resource.
        :param resource_group_name: The name of resource group 
        :param subnets A mapping of subnets to assign to Virtual Network.
        :param tags: A mapping of tags to assign to the resource.
        :param opts: Options for the resource.
        """

        self.__subnets: dict = dict()

        __vnet = network.VirtualNetwork(name,
                                        resource_group_name=resource_group_name,
                                        address_spaces=cidr,
                                        tags=self.__get_tags(tags),
                                        opts=opts)

        __input_subnets = subnets["subnets"]

        for subnet in __input_subnets:

            __service_endpoints = None
            __subnet_name = subnet["name"]
            if subnet.get("service_endpoints") != None:
                __service_endpoints = subnet["service_endpoints"]

            __subnet = network.Subnet(__subnet_name,
                                      name=__subnet_name,
                                      resource_group_name=resource_group_name,
                                      virtual_network_name=__vnet.name,
                                      address_prefixes=subnet["address_prefixes"],
                                      service_endpoints=__service_endpoints)

            __security_rules = None
            if subnet.get("nsg_security_rules") != None:
                __security_rules = subnet["nsg_security_rules"]

            # Create nsg
            __nsg = network.NetworkSecurityGroup(__subnet_name + "-nsg",
                                                 resource_group_name=resource_group_name,
                                                 security_rules=__security_rules,
                                                 tags=self.__get_tags(tags))

            # Associate subnet with nsg
            network.SubnetNetworkSecurityGroupAssociation(__subnet_name + "nsg-as",
                                                          subnet_id=__subnet.id,
                                                          network_security_group_id=__nsg.id,)

            self.__subnets[subnet["name"]] = __subnet

    @property
    def subnets(self) -> dict:
        return self.__subnets 

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else:
            __tags = dict()

        __tags["moduleName"] = __name__

        return __tags
