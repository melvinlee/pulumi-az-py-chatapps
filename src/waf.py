from pulumi_azure import network, monitoring


class ApplicationGateway:
    """Create Azure ApplicationGateway"""

    def __init__(self, name, resource_group_name, pip_id, subnet_frontend_id, subnet_backend_id, website_host, la_workspace_id, tags):

        web_backend_address_pool_name = name + "-web-beap"
        frontend_port_name = name + "feport"
        frontend_ip_configuration_name = name + "feip"
        web_backend_http_setting_name = name + "-web-be-htst"
        listener_name = name + "-httplstn"
        request_routing_rule_name = name + "-rqrt"
        redirect_configuration_name = name + "-rdrcfg"

        waf = network.ApplicationGateway(name,
                                         resource_group_name=resource_group_name,
                                         sku={
                                             "name": "WAF_v2",  # Using WAF_V2 for zone-redundant
                                             "tier": "WAF_v2",
                                             "capacity": 2,
                                         },

                                         gateway_ip_configurations=[{
                                             "name": "my-gateway-ip-configuration",
                                             "subnet_id": subnet_frontend_id,
                                         }],
                                         waf_configuration={
                                             "enabled": "true",
                                             "firewallMode": "Detection",
                                             "ruleSetVersion": "3.1"
                                         },
                                         frontend_ports=[{
                                             "name": frontend_port_name,
                                             "port": 80,
                                         }],
                                         frontend_ip_configurations=[{
                                             "name": frontend_ip_configuration_name,
                                             "public_ip_address_id": pip_id,
                                         }],
                                         backend_address_pools=[{
                                             "name": web_backend_address_pool_name,
                                             "fqdns": [website_host]
                                         }],
                                         #  probes = [{
                                         #      "name" : "probe",
                                         #      "interval": 30,
                                         #      "timeout": 30,
                                         #      "unhealthy_threshold": 3,
                                         #      "path": "/",
                                         #      "pickHostNameFromBackendHttpSettings": "true",
                                         #      "protocol": "https"
                                         #  }],
                                         backend_http_settings=[{
                                             "name": web_backend_http_setting_name,
                                             "cookieBasedAffinity": "Disabled",
                                             "path": "/",
                                             "port": 80,
                                             "protocol": "Http",
                                             "requestTimeout": 60,
                                         }],
                                         http_listeners=[{
                                             "name": listener_name,
                                             "frontend_ip_configuration_name": frontend_ip_configuration_name,
                                             "frontendPortName": frontend_port_name,
                                             "protocol": "Http",
                                         }],
                                         request_routing_rules=[{
                                             "name": request_routing_rule_name,
                                             "ruleType": "Basic",
                                             "httpListenerName": listener_name,
                                             "backendAddressPoolName": web_backend_address_pool_name,
                                             "backendHttpSettingsName": web_backend_http_setting_name,
                                         }],
                                         tags=tags)

        # Enabled diagnostic log and pipe it to la worksapce
        diagnostic_setting = monitoring.DiagnosticSetting("waf-diagsetting",
                                                          target_resource_id=waf.id,
                                                          log_analytics_workspace_id=la_workspace_id,
                                                          logs=[{
                                                              "category": "ApplicationGatewayFirewallLog",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              }
                                                          },
                                                              {
                                                              "category": "ApplicationGatewayAccessLog",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              }
                                                          },
                                                              {
                                                              "category": "ApplicationGatewayPerformanceLog",
                                                              "enabled": "true",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              },
                                                          }],
                                                          metrics=[{
                                                              "category": "AllMetrics",
                                                              "retention_policy": {
                                                                  "enabled": False,
                                                              },
                                                          }])
