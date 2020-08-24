from pulumi_azure import network


class StandrdPublicIP:
    """Create Azure Standard PublicIP"""

    public_ip_id = None

    def __init__(self, name, resource_group_name, tags):
        public_ip = network.PublicIp(name,
                                     resource_group_name=resource_group_name,
                                     sku="Standard",  # Standard SKU to support standard tier Application Gateways
                                     allocation_method="Static")

        self.public_ip_id = public_ip.id
