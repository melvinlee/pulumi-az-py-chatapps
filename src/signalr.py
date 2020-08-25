from pulumi_azure import signalr, monitoring


class Service:
    """Create Azure SignalR services"""

    service = None

    def __init__(self, name, resource_group_name, la_workspace_id, tags):

        service = signalr.Service(name,
                                  resource_group_name=resource_group_name,
                                  sku={
                                      "name": "Free_F1",
                                      "capacity": 1,
                                  },
                                  features=[{
                                      "flag": "ServiceMode",
                                      "value": "Default",
                                  },
                                      {
                                      "flag": "EnableConnectivityLogs",
                                      "value": "False"
                                  },
                                      {
                                      "flag": "EnableMessagingLogs",
                                      "value": "False"
                                  }
                                  ],
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
                                                                  "days": 0,
                                                                  "enabled": "false"
                                                              }
                                                          }],
                                                          metrics=[{
                                                              "category": "Errors",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "days": 0,
                                                                  "enabled": "false"
                                                              }
                                                          },
                                                              {
                                                              "category": "Traffic",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "days": 0,
                                                                  "enabled": "false"
                                                              }
                                                          }
                                                          ])

        self.service = service
