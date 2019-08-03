import getpass
import imaplib
import sys
import re
import hashlib

#Function that automatically detects the server to connect by anaysing the username
def autoDetect(usr):
    buffer = list()
    first = usr.find("@")
    last = usr.find(".")

    for i in range(first+1, last):
        buffer.append(usr[i])
    
    return "".join(buffer)


def getUsername():
    username = str(input("Username: "))

    """ Checks if the string is an email address """
    if re.match(r'[^@]+@[^@]+\.[^@]+', username) is None:
        print("Must be a valid email address...")
        sys.exit(0)
    
    return username

""" Looks for the password file and returns the password"""
def searchPasswd():
    try:
        with open("passwd.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

def savePasswd(password):
    with open("passwd.txt", "w") as f:
        f.write(password)

""" Gets the username and guesses the server """
username = getUsername()
server = autoDetect(username)

gmail = False
if server == "gmail":
    print("Oh, you seem to use Gmail... Then it is gonna be a bit different: please read \"GMAIL.txt\" before continuing otherwise it won't work...")
    gmail = True

""" Connects to the address """ 
try:
    print("Trying to reach the server...")
    imap = imaplib.IMAP4_SSL(f"imap.{server}.com", imaplib.IMAP4_SSL_PORT)

except:
    print("Failed to reach the server...")
    sys.exit(-1)

print("Successfully connected!")
if gmail == True:
    passwd = searchPasswd()
    if passwd == None:
        passwd = getpass.getpass()
        savePasswd(passwd)
else:
    passwd = getpass.getpass()

""" Logs in """
try:
    imap.login(username, passwd)

except:
    print("Invalid username or password...")
    sys.exit(-10)

print("You are logged in!")

imap.select()
typ, data = imap.search(None, "All")
data = data[0].split()
print(f"There are {len(data)} messages in your mailbox")
while True:
    sure = str(input("Are you sure you want to clean it? (Y/n) "))
    if sure == "Y":
        break
    elif sure == "n":
        print("Okay goodbye then...")
        imap.logout()
        sys.exit(0)

""" Writes the flag "Deleted" to the messages """
print("Cleaning...")
for id in data:
    imap.store(id, "+FLAGS", "\\Deleted")
imap.expunge()
print("Your email address is clean now!")

imap.close()

print("Logging out...")
imap.logout()
print("Logged out successfully!")
print("Goodbye!")