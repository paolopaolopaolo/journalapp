import mysql.connector as mdb, getpass as gp, os,sys,pickle,re,datetime as dt,subprocess as sp,hashlib as hl
from random import randrange


def read_journal(db,username):
	cursor=db.cursor()
	cursor.execute("USE diary;")
	#try:
	sqlexec="SELECT * FROM entries WHERE user=%s ORDER BY day desc;" 
	cursor.execute(sqlexec,(username,))
	#except (mdb.ProgrammingError,mdb.OperationalError):
	#	print("Poops on doops!")
	continuer=""
	item=""
	while item is not None and continuer=="":
		item=cursor.fetchone()
		try:
			print ("\nDay: %s\tTime: %s" % (item[0],item[1]))
			print ("\n%s" % item[3])
		except TypeError:
			break
		continuer=input("")
		if re.search(r"[Pp][Rr][Ii][Nn][Tt]",continuer)!=None:
			print_entry(item[3])

		if re.search(r"[Dd][Ee][Ll][Ee][Tt][Ee]",continuer)!=None:
			confirm=input("Are you sure you wish to delete this entry (Y/N)? ").upper()
			if confirm=="Y":
				try:
					cursor.execute("DELETE from entries where entry=%s;", item[3])
				except mdb.ProgrammingError:
					print("\n\nSQL injection!! Oh no!!!")
					read_journal(db,username)
				db.commit()
			else:
			  print ("Entry not deleted!\n")

		if re.search(r"[Ee][Dd][Ii][Tt]",continuer)!=None:
			print ("Begin edits!\n")
			day=re.search(r"([\d]+-[\d]+-[\d]+) ([\d]+:[\d]+:[\d]+).",str(dt.datetime.today())).group(1)
			time=re.search(r"([\d]+-[\d]+-[\d]+) ([\d]+:[\d]+):[\d]+.",str(dt.datetime.today())).group(2)
			entry=item[3]+"\nEDIT (%s, %s):" % (day,time)
			while True:
				entryline=input("")
				entry+=entryline+"\n"
				if entryline=="END":
					print ("Ended edits!\n\n\n")
					break
			cursor.execute("UPDATE entries SET entry=%s where entry=%s ",(entry[0:-4],item[3]))
			db.commit()

	cursor.close()
	print ("End of Entries!\n")
	read_or_write(db,username)

def print_entry(entry):
	defaultMSG="EMPTY"
	x=open("temp.txt",'w')
	x.write(entry)
	x.close()
	sp.call([r'C:\Windows\System32\notepad.exe',"temp.txt"])
	x=open("temp.txt",'w')
	x.write(defaultMSG)
	x.close()

def write_journal(db,username):
	print("Begin writing!\n")
	this_moment=str(dt.datetime.today())
	this_indexed_moment=re.search(r"([\d]+-[\d]+-[\d]+) ([\d]+:[\d]+:[\d]+).",this_moment)
	day=this_indexed_moment.group(1)
	time=this_indexed_moment.group(2)
	cursor=db.cursor()
	entry=""
	while True:
		entryline=input("")
		entry+=entryline+"\n"
		if entryline=="END":
			break
	try:
		sqlexec="INSERT INTO entries VALUES(%s,%s,%s,%s)" 
		cursor.execute(sqlexec,(day,time,username,entry[0:-4]))
	except mdb.IntegrityError:
		this_moment=str(dt.datetime.today())
		this_indexed_moment=re.search(r"([\d]+-[\d]+-[\d]+) ([\d]+:[\d]+:[\d]+).",this_moment)
		day=this_indexed_moment.group(1)
		time=this_indexed_moment.group(2)
		sqlexec="INSERT INTO entries VALUES(%s,%s,%s,%s)" 
		cursor.execute(sqlexec,(day,time,username,entry[0:-4]))


	db.commit()
	cursor.close()
	print("Saved Entry!")
	read_or_write(db,username)



def read_or_write(db,username):
	#Read or Write Submenu
	r_or_w=input("Read or Write?")
	if re.search("[Rr][Ee][Aa][Dd]",r_or_w) != None:
		read_journal(db,username)
	elif re.search("[Ww][Rr][Ii][Tt][Ee]",r_or_w) != None:
		write_journal(db,username)
	elif re.search("[Ee][Xx][Ii][Tt]",r_or_w) != None:
		print ("Goodbye!")
		sys.exit(0)
	elif re.search("[Uu][Ss][Ee][Rr]",r_or_w) != None:
		menu(db)
	else:
		print ("Error! Try again!")
		read_or_write(db,username)


def menu(db):
	print ('Welcome to Journal App 1.0!\n')
	ans=input('Are you a New (N) user or a Returning (R) user?\t')

	#New User: Set username and password
	#password is scrambled, username and scrambled password inserted into users table
	if ans.lower()=='n':
		print ('Excellent! We will need you to make a new password.\n')
		username=input('What will your username be?: ')
		pw1=gp.getpass('Password: ')
		pw2=gp.getpass('Confirm Password: ')
		if pw1==pw2:
			passhash=hl.sha1()
			passhash.update(pw1.encode("utf-8"))
			pw1=passhash.hexdigest()
			sqlexec="INSERT INTO users VALUES (%s;"
			cursor=db.cursor()
			try:
				cursor.execute(sqlexec,(username,pw1))
				db.commit()
				print ('Password confirmed! You are now in our system, %s!' % username)
			except mdb.IntegrityError:
				print ("There already exists a user with that handle. Please try again!")
				menu(db)
			cursor.close()
			read_or_write(db,username)

		else:
			print ('Password not confirmed: Try again!')
			menu(db)

	#Returning User: Enter username and password
	#For password, program will reopen Scramble object according to username

	elif ans.lower()=='r':
		print ('Excellent! Enter your username and password below!\n')
		username=input('Username: ')
		pw=gp.getpass('Password: ')
		passhash=hl.sha1()
		passhash.update(pw.encode("utf-8"))
		pw=passhash.hexdigest()
		compare=(username,pw)
		cursor=db.cursor()
		sqlexec=("SELECT * FROM users"
			" WHERE user=%s;")
		try:
		  cursor.execute("use diary;")
		  cursor.execute(sqlexec,(username,))
		  compare2=cursor.fetchall()
		  if compare2[0][0] == compare[0] and compare2[0][1]== compare[1]:
		    print("Success!")
		  cursor.close()
		except (mdb.ProgrammingError,mdb.OperationalError):
		  print("Bad Username or Password! Try Again!")
		  cursor.close()
		  menu(db)
		#print(compare2)
		read_or_write(db,username)
		
		
	elif ans.lower()=='exit':
		print ('Goodbye!')
		sys.exit(0)

	else:
		print ("Enter either 'N' or 'R' and then press enter!\nOr type in 'Exit' and then Enter to exit.\n")
		menu(db)

def set_db():
	host=input('MySQL Host?: ')
	if host=="":
		host="localhost"
	
	user=input('MySQL User?: ')
	if user=="":
		user="paolo"

	pw=gp.getpass('MySQL Password?: ')

	
	###Test connection to MySQL system
	#Test 1: Parameters Correct? If not, start again from beginning of main(). If so, continue.
	try:
		db=mdb.connect(host=host,user=user,password=pw)
		cursor=db.cursor()
	except (mdb.OperationalError,mdb.ProgrammingError):
		tryagain=input("Incorrect input. Could not connect!\nPress ENTER to try again or type in EXIT then press Enter\n")
		if tryagain.upper()=="EXIT":
			print ("Goodbye!")
			sys.exit(0)
		else:
			print ("Try again!")
			main()
	#Test 2: Diary exists on MySQL server? Will attempt to bring up Diary database, and open up tables.
	#IF diary does not exist or does not have the entries or users relations, it will create a new diary db with
	#those relations.
	try:
		cursor.execute('USE diary;')

	except (mdb.OperationalError, mdb.ProgrammingError):
		print ("You do not have a diary in your MySQL server or it does not have the proper tables.\nSetting up diary database with standard schema...")
		
		#Test 2a: Is there an existing diary DB on the server? If not, it will create one. If so, it will delete what
		#is there and create a new one. WARNING: If you happen to have a database called 'diary' on your server,
		#rename it before running this program.

		try:
			cursor.execute('CREATE DATABASE diary;')

		except mdb.ProgrammingError:
			cursor.execute('DROP DATABASE diary;')
			cursor.execute('CREATE DATABASE diary;')

		cursor.execute('USE diary;')
		cursor.execute('CREATE TABLE entries(day varchar(10), time varchar(8), user varchar(100), entry text, primary key(day,time,user))')
		cursor.execute('CREATE TABLE users(user varchar(100) primary key, password varchar(100))')
		db.commit()
		
		print ("Diary database created. You're welcome, booboo.")
	
	#Start menu!
	cursor.close()
	menu(db)


def main():
	###Set parameters for connecting to MySQL system
    set_db()

if __name__=='__main__':
	main()