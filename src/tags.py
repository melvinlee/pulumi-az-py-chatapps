import pulumi

class Tags:

    """
    Retrieve Resources Tags

    ## Example Usage

    ```python
    import tags

    my_tags = tags.Tags({"custom_tag": "custom_value"})
    my_tags.get_tags({"network_rules": "yes"})
    ```
    """
    
    def __init__(self, tags: dict = None):
        config = pulumi.Config()
        
        self.__tags = {
            'project': pulumi.get_project(),
            'stack': pulumi.get_stack(),
            'costCenter': config.require('cost-center')
        }

        if tags is not None:
            self.__tags.update(tags)

    def get_tags(self, tags: dict = None) -> dict:

        if tags is not None:
            tags.update(self.__tags)
            return tags
            
        return self.__tags