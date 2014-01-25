README: journalapp.py

Hello, you've reached my journal app! You will need the following programs on your
computer before you use this app:

-Python Interpreter (e.g. python.exe) AT LEAST 3.0
 -- mysql.connector module (comes with MySQL Server)
-MySQL Server (at least v5.1)

The prompts on this program are pretty self explanatory, however you can type EXIT at any prompt except the journal writing prompt to exit the program. During the "Read or Write?" prompt, you can also type in USER to change users or create a new user.

Passwords are encrypted with SHA1 and their hexdigest is saved on the database. This removes the need for any custom encryption scheme.

You'll also need to know which MySQL Server you plan on saving the diary to, as well as the password of that Server. One big caveat is that if you happen to have a db named "diary", it will
(or should) wipe that out and replace it with another one named "diary" with its own standard tables. Rename your current "diary" db to something else if you have too much vital information.

When the app asks for MySQL host and MySQL user at the very beginning, pressing Enter without inputting any data will default to "localhost" and "root" respectively. 

If you're looking at this program, thank you!
If you have any questions, my email is dpaolomercado@gmail.com.

-Dean