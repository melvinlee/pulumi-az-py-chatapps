import pulumi
from pulumi_azure import core

class ResourceGroup:
    """Create Resource group with tags"""

    def __init__(self, name: str, tags: dict = None):

        resource_group = core.ResourceGroup(name,
                                            tags=self.__get_tags(tags))
        self.name = resource_group.name

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else: 
            __tags = dict()

        __tags["moduleName"] = __name__

        return __tags