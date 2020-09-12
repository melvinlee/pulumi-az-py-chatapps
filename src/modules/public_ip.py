from pulumi_azure import network
import pulumi

class StandrdPublicIP:
    """
    Create Azure Standard PublicIP
    ## Example Usage

    ```python
    import public_ip

    pip = public_ip.StandrdPublicIP(name="example_name",
                                    resource_group_name="example_group_name",
                                    domain_name_label="example_domain"
                                    tags={
                                        "environment": "Production",
                                    })
    ```
    """

    __allocation_method = "Static"

    def __init__(self, name: str, resource_group_name: str, domain_name_label: str = None, tags: dict = None, opts: pulumi.ResourceOptions = None):
        """
        :param name: The name of the resource.
        :param resource_group_name: The name of resource group 
        :param str domain_name_label: Label for the Domain Name. Will be used to make up the FQDN.  If a domain name label is specified, an A DNS record is created for the public IP in the Microsoft Azure DNS system.
        :param tags: A mapping of tags to assign to the resource.
        :param opts: Options for the resource.
        """

        __public_ip = network.PublicIp(name,
                                       resource_group_name=resource_group_name,
                                       sku="Standard",
                                       allocation_method=self.__allocation_method,
                                       domain_name_label=domain_name_label,
                                       tags=self.__get_tags(tags),
                                       opts=opts)

        self.public_ip = __public_ip

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else:
            __tags = dict()

        __tags["moduleName"] = __name__
        __tags["allocationMethod"] = self.__allocation_method

        return __tags
