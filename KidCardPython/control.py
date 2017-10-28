import testing


#The login process
def Login(username, password)
	#Get primary accountNo from database
	#If not found: return to index
	
	parentbalance = GetAccountBalance(accountNo)
	
	for account in GetRelatedAccounts(accountNo)
		name = GetAccountHolderName(account)
		balance = GetAccountBalance(account)

#Create a new child card for the given parent account, with the given first and last name.		
def MakeNewCard(originPRN, firstName, lastName)
	fields{'firstName': firstName, 'lastName': lastName}
	accountNo = CreateSecondaryAccount(originPRN, fields)
	ActivateAccount(accountNo)

#Simulate adding money to the primary account
def AddPrimaryFunds(accountNo, amount)
	CreateAdjustment(accountNo, amount)

#Add money to the child account.
def AddChildFunds(originPRN, targetPRN, amount)
	CreateAccountTransfer(originPRN, targetPRN, amount)

#Returns true if card is frozen, false otherwise
def GetFrozenStatus(accountNo)
	#Get status from custom field, using API getUserDefinedAccountFields

#Switch the status of the account between frozen and unfrozen.
def switchFrozenStatus(accountNo)
	if GetFrozenStatus(accountNo):
		UnfreezeAccount(accountNo)
	else:
		FreezeAccount(accountNo)

		
	
	