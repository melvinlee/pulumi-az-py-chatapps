from pulumi_azure import storage


class StaticWebsite:
    """Create Azure Blob Static Website"""

    url = None
    
    def __init__(self, name, resource_group_name, tags):
        
        account = storage.Account(name,
                                  resource_group_name=resource_group_name,
                                  account_tier='Standard',
                                  account_kind='StorageV2',
                                  account_replication_type='LRS',
                                  static_website={
                                      "indexDocument": "index.html",
                                      "error404Document": "error.html"
                                  },
                                  tags=tags)
        
        # TODO: add function to upload static files to storage container
        # TODO: create network_rules to block all traffic and only allow connection from waf to static website

        # Export Static-Web URL
        self.url = account.primary_web_endpoint

