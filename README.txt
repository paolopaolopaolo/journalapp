README: journalapp.py

Hello, you've reached my journal app! You will need the following programs on your
computer before you use this app:

-Python Interpreter (e.g. python.exe)
 -- MySQLdb Python module
-MySQL Server (at least v5.1)

The prompts on this program are pretty self explanatory, however you can type EXIT at any prompt except the journal writing prompt to exit the program. During the "Read or Write?" prompt, you can also type in USER to change users or create a new user.

Also, if you have multiple computers all attached to one MySQL server, a person can only use the computer they created their account on to access the diary database. I made a very simple password encryption object that saves as a Pickle file on the computer hard drive and that file corresponds with the username that is put in when making a new account.One potential fix will be to go from using Pickle files to JSON files, and then storing the JSON files corresponding to each user on the database as well. There's one thread on Stack Overflow concerning storing Pickle
files on a MySQL database, but there is not much resolution on it. Otherwise, I would have definitely opted to storing the Pickle files, since they aren't as human readable as JSON.  

You'll also need to know which MySQL Server you plan on saving the diary to, as well as the password of that Server. One big caveat is that if you happen to have a db named "diary", it will
(or should) wipe that out and replace it with another one named "diary" with its own standard tables. Rename your current "diary" db to something else if you have too much vital information.

When the app asks for MySQL host and MySQL user at the very beginning, pressing Enter without inputting any data will default to "localhost" and "root" respectively. 

If you're looking at this program, thank you!
If you have any questions, my email is dpaolomercado@gmail.com.

-Dean