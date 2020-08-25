from pulumi_azure import storage
import pulumi

class StaticWebsite:
    """Create Azure Blob Static Website"""

    account = None

    def __init__(self, name, resource_group_name, tags):

        account = storage.Account(name,
                                  resource_group_name=resource_group_name,
                                  account_tier="Standard",
                                  account_kind="StorageV2",
                                  account_replication_type="LRS",
                                  static_website={
                                      "indexDocument": "index.html",
                                      "error404Document": "error.html"
                                  },
                                  enable_https_traffic_only=False,
                                  tags=tags)

        storage.Blob("index.html",
                     name="index.html",
                     content_type="text/html",
                     storage_account_name=account.name,
                     storage_container_name="$web",
                     type="Block",
                     source=pulumi.FileAsset("wwwroot/index.html"))

        # TODO: create network_rules to block all traffic and only allow connection from waf to static website

        # Export account
        self.account = account