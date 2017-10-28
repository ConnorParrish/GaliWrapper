import testing


#Create a new primary account, returns the Galileo ID
def CreatePrimaryAccount(firstName, lastName):
	fields{'firstName': firstName, 'lastName': lastName}
	accountNo = CreateAccount(fields)
	ActivateAccount(accountNo)
	return accountNo

#Get Children and Balance
def GetChildren(accountNo):
	
	children = {}
	
	for account in GetRelatedAccounts(accountNo)
		name = GetAccountHolderName(account)
		balance = GetAccountBalance(account)
		children[name] = balance

return children
		
#Create a new child card for the given parent account. Returns the Galileo ID.		
def MakeNewCard(originPRN, firstName, lastName):
	fields = {'firstName': firstName, 'lastName': lastName}
	accountNo = CreateSecondaryAccount(originPRN, fields)
	ActivateAccount(accountNo)
	return accountNo

#Simulate adding money to the primary account
def AddPrimaryFunds(accountNo, amount):
	CreateAdjustment(accountNo, amount)

#Add money to the child account.
def AddChildFunds(originPRN, targetPRN, amount):
	CreateAccountTransfer(originPRN, targetPRN, amount)

#Returns true if card is frozen, false otherwise
def GetFrozenStatusOfCard(accountNo):
	return GetFrozenStatus(accountNo) == "1"
	

#Switch the status of the account between frozen and unfrozen.
def switchFrozenStatus(accountNo):
	if GetFrozenStatus(accountNo) == "1":
		UnfreezeAccount(accountNo)
	else:
		FreezeAccount(accountNo)

		
	
	