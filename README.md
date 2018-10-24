# AWS Glacier Vault check

With this code snippet, you can check if a specific Glacier Vault exists. If the Vault exists, we will check if predefined access and lock policy are configured at the bucket. This monitoring makes sense if you create new Vaults automatically on a regular basis for backup purposes and want to make sure, that everything works fine. The code snippet is invoked via HTTP endpoint.

## Requirements

* Python 3 (tested with version 3.7.0)
* Node.js (tested with version 8.12.0)
* Serverless (tested with version 1.32.0)
* serverless plugin tracing (install via ```npm install serverless-plugin-tracing```)

## How to install

1. Clone this repository
2. Please edit the variables ```vaultAccessPolicy``` and ```vaultLockPolicy```in the serverless.yml. You can use <<<VAULTNAME>> as a placeholder for the vault name
3. Deploy the solution to AWS with ```sls deploy```. Please note the API-ID and the X-API-Key in the output
4. Test the endpoint via ```curl -X GET 'https://<<gateway id>>.execute-api.<<region>>.amazonaws.com/dev/?vaultName=<<vault-name>>' --header "X-Api-Key:<<<API-Key>>>"```
