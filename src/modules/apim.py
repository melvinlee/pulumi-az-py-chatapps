import pulumi
from pulumi_azure import apimanagement


class ApiManagement:
    """Create Azure API Management Service"""

    apimanagement = None

    def __init__(self, name, resource_group_name, apim_config, tags):
        
        apim = apimanagement.Service(name,
                                     resource_group_name=resource_group_name,
                                     publisher_name=apim_config.get(
                                         "publisher_name"),
                                     publisher_email=apim_config.get(
                                         "publisher_email"),
                                     sku_name="Developer_1",
                                     tags=tags)

        # TODO : configure product, api endpoint , and etc

        self.apimanagement = apim
