# Proposed Solution

## Assumption
- Node.js app will be performing authentication and authorisation
- The proposed solution must be cost effective
- The proposed solution required minimun effort to setup and maintained
- The proposed solution need to support web socket for real time communication and keep alive

## Options

1.Replatform
- minor code modification, example modify the way the app interacts with the database 
- cost-efficient solution, start small and scale up as needed
- new features can be added during replatforming to enable better scaling

2.Refactoring


## Replatform

![](/Images/option1-replatform.png)

### Resources
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
8. `Azure Monitor` for Azure resources and application monitoring