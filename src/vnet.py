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

        frontend = network.Subnet("frontend",
                                  name="frontend",
                                  resource_group_name=resource_group_name,
                                  virtual_network_name=vnet.name,
                                  address_prefixes=[subnet_frontend_cidr])

        backend = network.Subnet("backend",
                                  name="backend",
                                  resource_group_name=resource_group_name,
                                  virtual_network_name=vnet.name,
                                  address_prefixes=[subnet_backend_cidr])

        # Export Subnets Id
        self.frontend_subnet_id = frontend.id
        self.backend_subnet_id = backend.id
