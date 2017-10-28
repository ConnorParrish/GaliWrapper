from flask import Flask, render_template, request, session
import sqlite3
import hashlib
import testing
import time
#import control

def hashpassword(password_to_hash):
	return hash(password_to_hash)

app = Flask(__name__)

##_________________________
## SIGN UP PAGE
##__________________________

@app.route('/sign_up')
def sign_up():
	return render_template('sign_up.html')

@app.route('/submitted_form', methods=['POST'])
def submitted_form(): 
	first_name = request.form['firstname']
	last_name = request.form['lastname']
	username = request.form['username']
	password = request.form['password1']
	galileo_id = testing.CreateAccount({'firstName':first_name,'lastName':last_name}, True)
	new_user_to_db(galileo_id, first_name,last_name,username, hashpassword(password))
	return render_template("submitted_form.html", galileo_id = galileo_id, first_name = first_name, last_name = last_name, username = username, password=password)

@app.route('/')
def home():
	return render_template("index.html")


###________________
### DASHBOARD
###________________

@app.route('/user_dashboard', methods=['POST'])
def user_dashboard():
	user_name = request.form['username']
	elements = pull_query_from_db(user_name) #Pull elements from db in order: Id, firstname, lastname
	print(elements[0])
	galileo_id = elements[0]
	firstname = elements[1]
	lastname = elements[2]

	print(elements)

	children_ids = testing.GetRelatedAccounts(galileo_id)

	#childrenTransactions = {}
	#childrenTransactions = testing.GetChildrenTransactionHistory(children_ids)

	# testing.CreateAccountTransfer(galileo_id, children_ids[0], 100)
	# testing.CreateAccountTransfer(galileo_id, children_ids[1], 120)
	# testing.CreateAccountTransfer(galileo_id, children_ids[2], 20)

	childrenNames = {}
	childrenBalances = {}

	for child in children_ids:
		childrenNames[child] = testing.GetAccountHolderName(child)
		childrenBalances[child] = testing.GetAccountBalance(child)


	# session['test'] = firstname
	time.sleep(4)

	return render_template('dashboard.html', firstname = firstname, child1 = childrenNames[children_ids[0]] + " - $" + childrenBalances[children_ids[0]], child2 = childrenNames[children_ids[1]] + " - $" + childrenBalances[children_ids[1]], child3 = childrenNames[children_ids[2]] + " - $" + childrenBalances[children_ids[2]])


###_______________
### Sign In 
###_______________

@app.route('/sign_in')
def sign_in():
	return render_template('sign_in.html')




def new_user_to_db(galileo_id, first_name, last_name, username, password):
	database = sqlite3.connect('data.db')
	cursor = database.cursor()
	cursor.execute('''INSERT INTO userinfo(Id, firstname, lastname, username, password) VALUES(?, ?, ?, ?, ?)''', (galileo_id, first_name, last_name, username, password))
	database.commit()

def pull_query_from_db(username):
	print ("Just hit PULL QUERY")
	database = sqlite3.connect('data.db')
	cursor = database.cursor()
	cursor.execute('''SELECT Id, firstname, lastname FROM userinfo WHERE username=?''', (username,))
	row = cursor.fetchone()
	print ("PULL QUERY FROM DB returning elements pulled from query: " + str(row))
	return row
	#query_results = []
	# for element in cursor:
	# 	query_results.append(element)
	# print ("PULL QUERY FROM DB returning elements pulled from query: " + str(query_results)
	# return query_results


app.run(debug=True)

database.close()