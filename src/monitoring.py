from pulumi_azure import operationalinsights

class AnalyticsWorkspace:
    """Create Azure LogAnalytics"""

    AnalyticsWorkspace = None

    def __init__(self, name, resource_group_name, tags):
        self.AnalyticsWorkspace = operationalinsights.AnalyticsWorkspace(name,
                                                                         resource_group_name=resource_group_name,
                                                                         sku="PerGB2018",
                                                                         retention_in_days=30)
