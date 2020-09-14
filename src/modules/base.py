import pulumi
from pulumi_azure import core

class ResourceGroup:
    """
    Create Resource group with tags

     ## Example Usage

    ```python
    import core

    my_resourcegroup = base.ResourceGroup(name=example_name,
                                tags={
                                    "environment": "Production",
                                })

    ```
     """   

    def __init__(self, name: str, tags: dict = None, opts: pulumi.ResourceOptions = None):
        """
        :param name: The name of the resource.
        :param tags: A mapping of tags to assign to the resource.
        :param opts: Options for the resource.
        """

        self.__resource_group = core.ResourceGroup(name,
                                            tags=self.__get_tags(tags),
                                            opts=opts)

    @property
    def resource_group(self):
        return self.__resource_group 

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else: 
            __tags = dict()

        __tags["moduleName"] = __name__

        return __tags