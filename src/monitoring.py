from pulumi_azure import operationalinsights
import pulumi

class AnalyticsWorkspace:
    """
    Create Azure LogAnalytics

    ## Example Usage

    ```python
    import storage

    la_workspace = monitoring.AnalyticsWorkspace(name=la_name,
                                        resource_group_name=my_rg.name,
                                        retention_in_days=35,
                                        tags=my_tags.get_tags())

    ```
     """   

    AnalyticsWorkspace = None

    def __init__(self, name: str, resource_group_name: str, sku: str = "PerGB2018", retention_in_days: int = 30, tags: dict = None, opts: pulumi.ResourceOptions = None):
        """
        :param name: The name of the resource.
        :param resource_group_name: The name of resource group
        :param sku: The sku of the resource.
        :param retention_in_days:  The workspace data retention in days. Possible values are either 7 (Free Tier only) or range between 30 and 730.
        :param tags: A mapping of tags to assign to the resource.
        :param opts: Options for the resource.
        """

        self.AnalyticsWorkspace = operationalinsights.AnalyticsWorkspace(name,
                                                                         resource_group_name=resource_group_name,
                                                                         sku=sku,
                                                                         retention_in_days=retention_in_days,
                                                                         tags=self.__get_tags(tags),
                                                                         opts=opts)

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else: 
            __tags = dict()

        __tags["moduleName"] = __name__

        return __tags