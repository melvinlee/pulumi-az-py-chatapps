from pulumi_azure import dns


class PublicDNS:
    """Create Azure Public DNS Zone"""

    def __init__(self, name, resource_group_name, waf_pip_id, tags):

        zone = dns.Zone(
            name,
            name=name,
            resource_group_name=resource_group_name,
            tags=tags)

        dns.ARecord("www",
            name = "www",
            zone_name=zone.name,
            resource_group_name=resource_group_name,
            ttl=300,
            target_resource_id=waf_pip_id)