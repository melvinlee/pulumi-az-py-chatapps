import pulumi

def get_tags():

    config = pulumi.Config()
    
    tags = {
        'Project': pulumi.get_project(),
        'Stack': pulumi.get_stack(),
        'CostCenter': config.require('cost-center')
    }

    return tags