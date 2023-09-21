from Connection import *
from BankAccount import *
import sqlite3

conn = sqlite3.connect('bank.db')
c = conn.cursor()

# c.execute("""CREATE TABLE users (
#           name TEXT,
#           pinCode INTEGER
#   )""")
#c.execute("INSERT INTO users VALUES ('aissam', 1234, 12000, null)")
#conn.commit()
# c.execute('''ALTER TABLE users
#             ADD COLUMN solde REAL''')
# c.execute('''ALTER TABLE users
#             ADD COLUMN dernier_retrait DATETIME''')
# c.execute("""CREATE TABLE retraits (
#           name TEXT,
#           amount INTEGER
#           date DATETIME
#   )""")
#c.execute("""CREATE TABLE retraits (
#            name TEXT,
#            pinCode INTEGER,
#            amount DECIMAL,
#            date DATETIME
#    )""")

user = input("Entrez votre nom")
codePin = int(input("Entrez votre codePin"))
max_trials = 2
trials = max_trials


while(trials > 0):

    tryConnect = connection(user, codePin)
    if tryConnect.Connect():
        compte = BankAccount()
        montant = 0
        compte.Retrait(user, codePin)

        conn.commit()
        break
    else :
        print("Nom ou code pin incorrect, il vous reste " + str(trials) + " essais.")
        user = input("Entrez votre nom")
        codePin = int(input("Entrez votre codePin"))
        trials -= 1




"""

max_trials = 3
trials = max_trials
solde = 1000


while trials > 0:
    tryUser = input("Entrez votre nom d'utilisateur: ")
    tryCodePin = int(input("Entrez votre code pin: "))

    if tryUser != user or tryCodePin != codePin:
        trials -= 1
        print("Nom d'utilisateur ou code pin incorrect, encore " + str(trials) + " essais.")

    else:
        print("Bienvenue, " + user + "!")
        print("Votre solde est de " + str(solde) + "€.")
        break

if trials == 0:
    print("Vous avez épuisé toutes vos tentatives.")
"""
