import json
import datetime
import dateutil.relativedelta
import boto3
import time
import os

def awsglaciervaultcheck(event, context):

    #Overall check is always okay (should be changed!)

    checkIsOkay = True

    #Read vault name from event

    try:
        vaultName = event['multiValueQueryStringParameters']['vaultName'][0]
    except:
        print("ERROR: The parameter vaultName was not provided.")
        response = {
            "statusCode": 500,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "An error occurred. The parameter vaultName was not provided."
        }
        return response

    #check if Vault exists

    print("Checking vault name "+ vaultName)
    client = boto3.client('glacier')
    response = client.list_vaults(
        limit='1000'
    )

    vaultList = response['VaultList']
    vaultIsPresent = False
    for availableVault in vaultList:
      availableVaultName = availableVault['VaultName']
      if availableVaultName == vaultName:
          vaultIsPresent = True
          break

    if vaultIsPresent is False:
        checkIsOkay = False
        print("A Glacier vault with the name " + vaultName + " is not available!")
        response = {
            "statusCode": 200,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "A Glacier vault with the name " + vaultName + " is not available."
        }
        return response

    print('The vault with the name ' + vaultName + ' is available!')

    #check if access policy matches the provided

    vaultAccessPolicyTemplate = os.environ['vaultAccessPolicy']
    vaultAccessPolicy = vaultAccessPolicyTemplate.replace('<<VAULTNAME>>', vaultName)

    try:
        response = client.get_vault_access_policy(
            vaultName=vaultName
        )
        accessPolicy = response['policy']['Policy']
    except:
        checkIsOkay = False
        print('WARNING: The program was not able to retrieve an access policy. Is a access policy set?')
        accessPolicy=""

    print('Access policy from vault is: ' + accessPolicy)

    if vaultAccessPolicy == accessPolicy:
        print("Access policy matched!")
    else:
        checkIsOkay = False
        print("Access policy does not match!")

    #check if lock policy matches the provided

    vaultLockPolicyTemplate = os.environ['vaultLockPolicy']
    vaultLockPolicy = vaultLockPolicyTemplate.replace('<<VAULTNAME>>', vaultName)

    try:
        response = client.get_vault_lock(
            vaultName=vaultName
        )
        print(response)
        lockPolicy = response['Policy']
        state = response['State']
        print("Lock status is currently: " + state)
        expirationDate = response['ExpirationDate']
        print("The lock on this vault will end at: " + expirationDate)
    except:
        checkIsOkay = False
        print('WARNING: The program was not able to retrieve the lock policy. Is a lock policy set?')
        lockPolicy=""

    print('Lock policy from vault is: ' + lockPolicy)

    if vaultLockPolicy == lockPolicy:
        print("Lock policy matched!")
    else:
        checkIsOkay = False
        print("Lock policy does not match!")

    #Process overall check

    if checkIsOkay is True:
        response = {
            "statusCode": 200,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "The check of the Glacier vault " + vaultName + " was successful."
        }
        return response
    if checkIsOkay is False:
        response = {
            "statusCode": 200,
            "headers": {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Credentials': True,
            },
            "body": "The check of the Glacier vault " + vaultName + " was not successful."
        }
        return response

    print("You should never reach this part...")
