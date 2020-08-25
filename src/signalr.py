from pulumi_azure import signalr, monitoring


class Service:
    """Create Azure SignalR services"""

    service = None

    def __init__(self, name, resource_group_name, la_workspace_id, tags):

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

        # Enabled diagnostic log and pipe it to la worksapce
        diagnostic_setting = monitoring.DiagnosticSetting("sig-diagsetting",
                                                          target_resource_id=service.id,
                                                          log_analytics_workspace_id=la_workspace_id,
                                                          logs=[{
                                                              "category": "AllLogs",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              }
                                                          }],
                                                          metrics=[{
                                                              "category": "Traffic",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              },
                                                          }])

        self.service = service
