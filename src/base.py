import pulumi
from pulumi_azure import core

# Define a class
class ResourceGroup:
    """Create Resource group with tags"""

    def __init__(self, name, tags):    
        resource_group = core.ResourceGroup(name,tags=tags)
        self.name = resource_group.name