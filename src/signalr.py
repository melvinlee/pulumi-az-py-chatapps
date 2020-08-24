from pulumi_azure import signalr

class Service:
    """Create Azure SignalR services"""

    primary_connection_string = None
    public_port = None

    def __init__(self, name, resource_group_name, tags):

        service = signalr.Service(name,
            resource_group_name=resource_group_name,
            sku={
                "name": "Standard_S1",
                "capacity": 2,
            },
            features=[{
                "flag": "ServiceMode",
                "value": "Default",
            }],
            tags=tags)

        # TODO: to add service endpoint and allow connection from backend subnet only
        
        self.primary_connection_string = service.primary_connection_string
        self.public_port = service.public_port