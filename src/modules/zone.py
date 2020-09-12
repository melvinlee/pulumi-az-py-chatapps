from pulumi_azure import dns
import pulumi


class PublicDNS:
    """Create Azure Public DNS Zone

    ## Example Usage

    ```python
    import zone

    my_zone = zone.PublicDNS(name=example_name,
                            resource_group_name=example_group_name,
                            recordsets=[{
                                "name": "www",
                                "record_type": "A",
                                "ttl" : 300,
                                "target_resource_id": "example_public_ip_id"
                            },
                            {
                                "name": "api",
                                "record_type": "CName",
                                "ttl" : 300,
                                "record": "contoso.com"
                            }],
                            tags={
                                "environment": "Production",
                            })
    ```
    """

    def __init__(self, name: str, resource_group_name: str, recordsets: list = None, tags: dict = None, opts: pulumi.ResourceOptions = None):

        self.__tags = None 
        
        self.tags = tags

        __zone = dns.Zone(
            name,
            name=name,
            resource_group_name=resource_group_name,
            tags=self.tags,
            opts=opts)

        for record in recordsets:

            if record["record_type"] == "A":

                __A_target_resource_id = None
                __A_record = None

                if record.get("target_resource_id") != None:
                    __A_target_resource_id = record["target_resource_id"]

                if record.get("records") != None:
                    __A_record = record["records"]

                dns.ARecord(record["name"],
                            name=record["name"],
                            zone_name=__zone.name,
                            resource_group_name=resource_group_name,
                            ttl=record["ttl"],
                            target_resource_id=__A_target_resource_id,
                            records=__A_record,
                            tags=self.tags)

            elif record["record_type"] == "CName":

                __target_resource_id = None
                __record = None

                if record.get("target_resource_id") != None:
                    __target_resource_id = record["target_resource_id"]

                if record.get("record") != None:
                    __record = record["record"]

                dns.CNameRecord(record["name"],
                                name=record["name"],
                                zone_name=__zone.name,
                                resource_group_name=resource_group_name,
                                ttl=record["ttl"],
                                target_resource_id=__target_resource_id,
                                record=__record,
                                tags=self.tags)

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