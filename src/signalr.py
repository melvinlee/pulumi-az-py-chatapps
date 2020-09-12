import pulumi
from pulumi_azure import signalr, monitoring


class Signalr:
    """
    Create Azure SignalR services

    ## Example Usage

    ```python
    import signalr

    my_signalr = signalr.Signalr(name=example_name,
                             resource_group_name=example_group_name,
                             sku={
                                "name": "Free_F1",
                                "capacity": 1,
                            },
                             log_analytics={
                                 "log_analytics_workspace_id":  example_id,
                             },
                             tags={
                                "environment": "Production",
                            })
    ```

    """

    def __init__(self, name: str, resource_group_name: str, sku: dict = None, log_analytics: dict = None, tags: dict = None, opts: pulumi.ResourceOptions = None):

        self.__tags = None
        self.__diag_logs = None
        self.__diag_metrics = None

        self.__service = signalr.Service(name,
                                         resource_group_name=resource_group_name,
                                         sku=sku,
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
                                         tags=tags,
                                         opts=opts)

        # TODO: to add service endpoint and allow connection from backend subnet only

        if log_analytics.get("logs") != None:
            self.__diag_logs = log_analytics["logs"]

        if log_analytics.get("metrics") != None:
            self.__diag_metrics = log_analytics["metrics"]

        # if la workspace id found, enabled diagnostic log
        if log_analytics.get("log_analytics_workspace_id") != None:
            self.__diagnostic_setting = monitoring.DiagnosticSetting("sig-diagsetting",
                                                                     target_resource_id=self.__service.id,
                                                                     log_analytics_workspace_id=log_analytics[
                                                                         "log_analytics_workspace_id"],
                                                                     logs=self.diag_logs,
                                                                     metrics=self.diag_metrics,
                                                                     opts=opts)

    @property
    def service(self):
        return self.__service

    @property
    def diag_logs(self) -> list:
        if self.__diag_logs is None:
            self.__diag_logs = [{
                "category": "AllLogs",
                "enabled": "true",
                "retention_policy": {
                    "days": 0,
                    "enabled": "false"
                }
            }]
        return self.__diag_logs

    @property
    def diag_metrics(self) -> list:
        if self.__diag_metrics is None:
            self.__diag_metrics = [{
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
            ]
        return self.__diag_metrics

    @property
    def diagnostic_setting(self):
        return self.diagnostic_setting

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value):
        if self.__tags is None:
            self.__tags = dict(value)
            self.__tags["moduleName"] = __name__
        else:
            self.__tags.update(value)
