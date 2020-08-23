# Proposed Solution

## Assumption
- Node.js app will be performing authentication and authorisation
- The proposed solution must be cost effective
- The proposed solution required minimun effort to setup and maintained
- The proposed solution need to support web socket for real time communication and keep alive
- The proposed solution should be Highly Available
- The proposed solution should be Scalable
- The proposed solution should be Highly Fault Tolerant

## Option 1: Replatform
- minor code modification, example modify the way the app interacts with the database 
- cost-efficient solution, start small and scale up as needed
- new features can be added during replatforming to enable better scaling

![](/Images/option1-replatform.png)

### Resources
1. `Azure Public DNS` for app.com
2. `Azure WAF`
- path-based routing and Layer 7 firewall OWASP
- redirect https://app.com/ to Azure Blob 
- redirect https://app.com/api/ to APIM
3. `Azure Blob Static Website` serving static contents "index.html", js and CSS
4. `Azure APIM`
- redirect https://app.com/api/ to Azure WeApp
- request throttling
- endpoint protection
4. `Azure WebApp for Container` hosting node.js backend processing in container
5. `Azure Container Registry` hosting node.js container image
6. `Azure Redis Cache` keeps clients connectivity state
7. `Azuere MySQL` keeps user accounts
8. `Azure Monitor` for Azure resources and application monitoring


## Option 2: Refactoring
- Loosely coupled and using cloud native framework
- complex to refactor and required major code modification to better take advantage of cloud-based features 
- serverless architecture, consumed less and scale up as needed

![](/Images/option1-refactoring.png)

### Resources
1. `Azure Public DNS` for app.com
2. `Azure WAF`
- path-based routing and Layer 7 firewall OWASP
- redirect https://app.com/ to Azure Blob 
- redirect https://app.com/api/ and https://app.com/negotiate/ to APIM
3. `Azure Blob Static Website` serving static contents "index.html", js and CSS
4. `Azure APIM`
- redirect https://app.com/negotiate/ to Azure Function A
- redirect https://app.com/api/ to Azure Function B
- request throttling
- endpoint protection
5. Azure Function
- Azure Function A to authenticate user to SignalR services
- Azure Function B to send messages to connected client
6. `Azure SignalR Services`
7. `Azure Monitor` for Azure resources and application monitoring