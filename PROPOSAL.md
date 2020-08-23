# Proposed Options

1. Replatform
2. Refactoring


## Replatform

### PaaS Resources

![](/Images/option1-replatform.png)

1. `Azure Public DNS` for app.com
2. `Azure WAF`
- Path-based routing and Layer 7 firewall
- redirect https://app.com/ to Azure Blob 
- redirect https://app.com/api/ to APIM
3. `Azure Blob Static Website` serving static contents "index.html", js and CSS
4. `Azure APIM`
- redirect https://app.com/api/ to Azure WeApp
- request throttling
4. `Azure WebApp for Container` hosting node.js backend processing in container
5. `Azure Container Registry` hosting node.js container image
6. `Azure Redis Cache` keeps clients connectivity state
7. `Azuere MySQL` keeps user accounts