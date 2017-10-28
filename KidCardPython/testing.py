import requests
from xml.dom.minidom import parseString
import string
import random
import time
import datetime

commonPayload = {'apiLogin':'Dlm5Fn-9999','apiTransKey':'QwQTu3mHXK','providerId':'488'}

def main():
    prn = 999900032825 #(for Ned Stark) CreateAccount({'firstName':'Ned','lastName':'Stark'}) #creating cards?
    #ActivateAccount(prn)

    #GetAccountCards(prn)
    #print("Creating child account")

    kidprn1 = 999900032833 #(for Sansa Stark) CreateSecondaryAccount(prn, {'firstName':'Sansa', 'lastName':'Stark'})
    #ActivateAccount(kidprn1)
    kidprn2 = 999900032841 #(for Arya Stark) CreateSecondaryAccount(prn, {'firstName':'Arya', 'lastName':'Stark'})
    #ActivateAccount(kidprn2)
    kidprn3 = 999900032866 #(for Bran Stark) CreateSecondaryAccount(prn, {'firstName':'Bran', 'lastName':'Stark'})
    #ActivateAccount(kidprn3)
    kidprn4 = 999900033864 #(for Jon Snow) CreateSecondaryAccount(prn, {'firstName':'Jon', 'lastName':'Snow'})

    #CreateAdjustment(prn, 100)
    #CreateAccountTransfer(prn, kidprn3, 30)

    accounts = {}
    relatedAccounts = GetRelatedAccounts(prn)

    GetTransactionHistory(kidprn4, "2017-01-01", datetime.datetime.now().strftime("%Y-%m-%d"), True)
    
    for accountNo in relatedAccounts:
        transactionHistory = GetTransactionHistory(accountNo, "2017-01-01", datetime.datetime.now().strftime("%Y-%m-%d"))
        #print(transactionHistory.getElementsByTagName('transactions')[0].firstChild.toprettyxml())

        accounts[accountNo] = []
        transactions = transactionHistory.getElementsByTagName('transactions')
        #print(str(transactions))

        #if transactionHistory.getElementsByTagName('transactions').__len__() != 0:
        for transaction in transactionHistory.getElementsByTagName('transactions'):
            if transaction.getElementsByTagName('pmt_ref_no').__len__() != 0:
                timestamp = transaction.getElementsByTagName('post_ts')[0].firstChild.nodeValue
                amount = transaction.getElementsByTagName('amt')[0].firstChild.nodeValue
                details = transaction.getElementsByTagName('details')[0].firstChild.nodeValue
                date = timestamp[:10]

                if (transaction.getElementsByTagName('formatted_merchant_desc')[0].firstChild != None):
                    merchantdesc = "Transfer from " + transaction.getElementsByTagName('formatted_merchant_desc')[0].firstChild.nodeValue
                else:
                    merchantdesc = ""

                accounts[accountNo].append(TransactionModelObject(amount, details, merchantdesc, date))

    FreezeAccount(kidprn1)
    print(GetFrozenStatus(kidprn1))
    UnfreezeAccount(kidprn1)
    print(GetFrozenStatus(kidprn1))
#    GetTransactionHistory(kidprn1, 1)

    #authId = CreateSimulatedCardAuth(kidprn2, 10, "visa", "Maester's Library", True)
    #CreateSimulatedCardSettle(kidprn2, authId, "visa", True)

    print("\n\n")
    #time.sleep(5)
    #accounts = {kidprn1:{'balance':GetBalance(kidprn1), 'transactions':{'transId':}}}

    GetTransactionHistory(kidprn2, '2016-01-01', '2017-12-12')

#region Account Creation

#Creates parent card
def CreateAccount(additionalUserInformation, displayXML=False):
    payload = AppendPayload(
        {
            'prodId':'5094'
        }, GatherInput())

    dom = GalileoPOST('createAccount', payload, displayXML)
    return dom.getElementsByTagName('pmt_ref_no')[0].firstChild.nodeValue

#Creates child cards
def CreateSecondaryAccount(originPRN, additionalUserInformation, displayXML=False):
    payload = AppendPayload(
        {
            'prodId':'5094',
            'primaryAccount':originPRN,
            'sharedBalance':0
        }, additionalUserInformation)

    dom = GalileoPOST('createAccount', payload, displayXML)
    return dom.getElementsByTagName('pmt_ref_no')[0].firstChild.nodeValue

# Get accounts up and activates both the account AND card at once
def ActivateAccount(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'type':1
        })

    dom = GalileoPOST('modifyStatus', payload, displayXML)
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'type':7
        })

    dom = GalileoPOST('modifyStatus', payload, displayXML)

#Deactivates card
def DeactivateAccount(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'type':'2'
        })

    dom = GalileoPOST('modifyStatus', payload, displayXML)

# Sets a new field with a given value
def SetUserDefinedAccountField(accountNo, fieldName, fieldValue, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'fieldId':fieldName,
            'fieldValue':fieldValue
        })

    dom = GalileoPOST('setUserDefinedAccountField', payload, displayXML)

# Gets all user defined fields on an account
def GetUserDefinedAccountFields(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo
        })

    return GalileoPOST('getUserDefinedAccountFields', payload, displayXML)

#endregion

#region Account Information

#Gets all transaction information on account
def GetAccountOverview(accountNo, startDate, endDate, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo, 
            'startDate':startDate, 
            'endDate':endDate
        })

    dom = GalileoPOST('getAccountOverview', payload, displayXML)
    return dom

# Gets children accounts
def GetRelatedAccounts(accountNo, displayXML=False):
    relatedAccounts = []
    dom = GetAccountCards(accountNo, False)

    accounts = dom.getElementsByTagName("related_account")
    for account in accounts:
        relatedAccounts.append(account.getElementsByTagName('pmt_ref_no')[0].firstChild.nodeValue)

    return relatedAccounts

#Gets cards for primary account and secondaries (child cards)
def GetAccountCards(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'includeRelated':1
        })

    dom = GalileoPOST('getAccountCards', payload, displayXML)
    return dom

# Grabs the transactions between two dates
def GetTransactionHistory(accountNo, startDate, endDate, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'startDate':startDate,
            'endDate':endDate
            #'recordCnt':____
        })

    dom = GalileoPOST('getTransHistory', payload, displayXML)
    return dom

# Gets current balance of account
def GetAccountBalance(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo
        })
    return GalileoPOST('getBalance', payload, displayXML).getElementsByTagName("balance")[0].firstChild.nodeValue

# Grabs the name of the account holder
def GetAccountHolderName(accountNo):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    overview = GetAccountOverview(accountNo, now, now)
    return overview.getElementsByTagName("first_name")[0].firstChild.nodeValue + " " + overview.getElementsByTagName("last_name")[0].firstChild.nodeValue


#endregion

#region Account Administration

# Freezes account
def FreezeAccount(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'type':17
        })

    dom = GalileoPOST('modifyStatus', payload, displayXML)
    SetUserDefinedAccountField(accountNo, 'Frozen', '1', displayXML)

# Unfreezes account
def UnfreezeAccount(accountNo, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'type':18
        })

    dom = GalileoPOST('modifyStatus', payload, displayXML)
    SetUserDefinedAccountField(accountNo, 'Frozen', '0', displayXML)

#endregion

#region Money Movement
#Adjusts balance incase of error (adding money for testing)
def CreateAdjustment(accountNo, amount, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo, 
            'amount':amount, 
            'type':"F", 
            'debitCreditIndicator':"C",                                 #Give credit to account ("D" takes money)
            'description':input("Give description for adjustment: ")
        })

    dom = GalileoPOST('createAdjustment', payload, displayXML)

#Transfers money between parent and child cards
def CreateAccountTransfer(originPRN, targetPRN, amount, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':originPRN,
            'amount':amount,
            'transferToAccountNo':targetPRN, 
            'message':input("Enter message for transfer (optional): ")
        })

    dom = GalileoPOST('createAccountTransfer', payload, displayXML)


# Creates a simulated auth
def CreateSimulatedCardAuth(accountNo, amount, association, merchantName, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'amount':amount,
            'association':association,
            'merchantName':merchantName
        })

    return GalileoPOST('createSimulatedCardAuth', payload, displayXML).getElementsByTagName('auth_id')[0].firstChild.nodeValue

# Settles simulated auths
def CreateSimulatedCardSettle(accountNo, authId, association, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'authId':authId,
            'association':association
        })

    dom = GalileoPOST('createSimulatedCardSettle', payload, displayXML)

# Creates a payment (credits the account)
def CreatePayment(accountNo, amount, paymentType, description, displayXML=False):
    payload = AppendPayload(
        {
            'accountNo':accountNo,
            'amount':amount,
            'type':paymentType,
            'description':description
        })

    dom = GalileoPOST('createPayment', payload, displayXML)


#endregion



#region Helper Functions

#Generates a post call by given method name and unique payload
def GalileoPOST(methodName, payload, debugDisplay):
    r = requests.post('https://sandbox-api.gpsrv.com/intserv/4.0/' + methodName, data=payload, cert="galileo65.pem")
    dom = parseString(r.text)

    DebugDisplay(methodName, dom, debugDisplay)
    return dom

#Adds common parameter to the unique 
def AppendPayload(payload, stuffToAdd={}):
    payload.update(commonPayload)
    payload.update({'transactionId':randomTransID(7)})
    payload.update(stuffToAdd)
    return payload

# Displays the XML of request responses
def DebugDisplay(methodName, dom, displayXML):
    statusCode = dom.getElementsByTagName('status_code')
    if (displayXML):
        print(dom.toprettyxml())
    
    print(methodName + ' response code=' + statusCode[0].firstChild.nodeValue + " | " + dom.getElementsByTagName('status')[0].firstChild.nodeValue)

#Collects input for account creation from user
def GatherInput():
    return {'firstName': input("Enter first name: "), 'lastName':input("Enter last name: ")} #, 'dateOfBirth':input("Enter your DOB (YYYY-MM-DD)"), 'primaryPhone':input("Enter your phone number for security reasons")}

#Generates a random transaction ID
def randomTransID(length):
    numbers = string.digits
    letters = string.ascii_lowercase
    return ''.join(random.choice(numbers) for i in range (length))

def GetFrozenStatus(accountNo):
    return GetUserDefinedAccountFields(accountNo).getElementsByTagName('field_value')[0].firstChild.nodeValue

#endregion

class TransactionModelObject:
    def __init__(self, amount, details, merchant_description, date):
        self.Amount = amount
        self.Details = details
        self.MerchantDescription = merchant_description
        self.Date = date

if __name__ == "__main__":
    main()