from pulumi_azure import storage
import pulumi


class StaticWebsite:
    """
    Create Azure Blob Static Website

    ## Example Usage

    ```python
    import storage

    website = storage.StaticWebsite(name=website_name, 
                                    resource_group_name=rg.name,
                                    network_rules={
                                        "default_action": "Allow",
                                        "ip_rules": ["100.0.0.1"],
                                        "virtual_network_subnet_ids": [example_subnet.id],
                                    },
                                    tags=tags)
    ```
    """

    account = None

    def __init__(self, name: str, resource_group_name: str, index_html: str = None, network_rules=None, tags: dict = None, opts: pulumi.ResourceOptions = None):
        """
        :param resource_name: The name of the resource.
        :param resource_group_name: The name of resource group 
        :param index_html: The name of the index.html upload to $web container.
        :param network_rules: A `network_rules` block as documented below.
        :param tags: A mapping of tags to assign to the resource.
        :param opts: Options for the resource.

        The **network_rules** object supports the following:

          * `bypasses` (`pulumi.Input[list]`) - Specifies whether traffic is bypassed for Logging/Metrics/AzureServices. Valid options are
            any combination of `Logging`, `Metrics`, `AzureServices`, or `None`.
          * `default_action` (`pulumi.Input[str]`) - Specifies the default action of allow or deny when no other rules match. Valid options are `Deny` or `Allow`.
          * `ip_rules` (`pulumi.Input[list]`) - List of public IP or IP ranges in CIDR Format. Only IPV4 addresses are allowed. Private IP address ranges (as defined in [RFC 1918](https://tools.ietf.org/html/rfc1918#section-3)) are not allowed.
          * `virtual_network_subnet_ids` (`pulumi.Input[list]`) - A list of resource ids for subnets.
        """

        __account = storage.Account(name,
                                  resource_group_name=resource_group_name,
                                  account_tier="Standard",
                                  account_kind="StorageV2",
                                  account_replication_type="LRS",
                                  static_website={
                                      "indexDocument": "index.html",
                                      "error404Document": "error.html"
                                  },
                                  network_rules=network_rules,
                                  enable_https_traffic_only=True,
                                  tags=self.__get_tags(tags),
                                  opts=opts)

        if index_html is not None:
            storage.Blob("index.html",
                         name="index.html",
                         content_type="text/html",
                         storage_account_name=__account.name,
                         storage_container_name="$web",
                         type="Block",
                         source=pulumi.FileAsset(index_html),
                         opts=opts)

        # Export account
        self.account = __account

    def __get_tags(self, tags):
        if tags is not None:
            __tags = dict(tags)
        else: 
            __tags = dict()

        __tags["moduleName"] = __name__

        return __tags