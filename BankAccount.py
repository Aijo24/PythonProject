import sqlite3
from datetime import datetime, timedelta
from math import floor
class bankAccount:
    def __init__(self):
        self.dateDeRetrait = None
        self.montantRetirerAujd = 0
        self.solde = 0

    def Retrait(self, montant, user, codePin):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()

        c.execute("SELECT solde, dernier_retrait FROM users WHERE name = ? AND pinCode = ?", (user, codePin))
        row = c.fetchone()
        if row is not None:
            self.solde = row[0]
            date_de_retrait_str = row[1]  # Récupérer la date de retrait sous forme de chaîne
            if date_de_retrait_str is not None:
                self.dateDeRetrait = datetime.strptime(date_de_retrait_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                self.dateDeRetrait = datetime.now()
            print("Votre solde est de :", self.solde)
        else:
            print("Aucun utilisateur correspondant trouvé dans la base de données.")

        montant = int(input("Combien voulez-vous retirer ?"))
        while montant < 20 :
            montant = int(input("Combien voulez-vous retirer ?"))

        un_jour_avant = datetime.now() - timedelta(hours=24)
        c.execute("SELECT SUM(amount) FROM retraits WHERE name = ? AND date >= ?", (user, un_jour_avant))
        total_retraits_24h = c.fetchone()[0] or 0

        if total_retraits_24h + montant > 2000:
            print("La somme des retraits des dernières 24 heures dépasse 200. Retrait impossible.")
        elif montant <= self.solde:
            self.solde -= montant
            c.execute("UPDATE users SET dernier_retrait = ?, solde = ? WHERE name = ? AND pinCode = ?",
                      (self.dateDeRetrait.strftime("%Y-%m-%d %H:%M:%S.%f"), self.solde, user, codePin))
            conn.commit()
            c.execute("INSERT INTO retraits (name, pinCode, amount, date) VALUES (?, ?, ?, ?)",
                      (user, codePin, montant, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
            conn.commit()

            if montant >= 100:
                petit_ou_gros = ""

                while petit_ou_gros != "p" and petit_ou_gros != "g":
                    try:
                        petit_ou_gros = input("Voulez-vous retirer des petits ou des gros billets ? Entrez p ou g : ").lower()
                    except:
                        print("Veuillez entrer un caractère valide.")
                        print("Veuillez répondre par 'p' ou 'g'.")

                if(petit_ou_gros == "p"):
                    nb_billet_20 = floor(montant / 20)
                    reste = montant - nb_billet_20 * 20
                    nb_billet_10 = int(reste / 10)
                    if nb_billet_10 < 1 and nb_billet_20 == 1:
                        print("Vous avez retiré : un billet de 20 ")
                    elif nb_billet_10 < 1 :
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 ")
                    elif nb_billet_10 == 1 :
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 " + "un billets de 10.")
                    else:
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 " + str(nb_billet_10) +
                              " billets de 10.")

                if (petit_ou_gros == "g"):
                    nb_billet_100 = floor(montant / 100)
                    reste = montant - nb_billet_100 * 100

                    while reste % 100 == 0:
                        nb_billet_100 = floor(montant / 100)
                        reste = montant - nb_billet_100 * 100

                    while reste % 50 == 0:
                        nb_billet_50 = floor(montant / 50)
                        reste = montant - nb_billet_50 * 50

                    nb_billet_20 = floor(montant / 20)
                    reste = montant - nb_billet_20 * 20
                    nb_billet_10 = int(reste / 10)
                    if nb_billet_10 < 1 and nb_billet_20 == 1:
                        print("Vous avez retiré : un billet de 20 ")
                    elif nb_billet_10 < 1:
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 ")
                    elif nb_billet_10 == 1:
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 " + "un billets de 10.")
                    else:
                        print("Vous avez retiré : " + str(nb_billet_20) + " billets de 20 " + str(nb_billet_10) +
                              " billets de 10.")

            print("Soit : " + str(montant) + " €")
            print("Il vous reste :", str(self.solde) + " €")
        else:
            print("Solde insuffisant sur le compte ou montant quotidien maximum atteint.")
        """
        montant = int(input("Combien voulez-vous retirer ?"))

        if montant < self.solde and self.montantRetirerAujd + montant <= 200:
            self.solde -= montant
            self.montantRetirerAujd += montant
            self.dateDeRetrait = datetime.now()
            c.execute("UPDATE users SET dernier_retrait = ?, solde = ? WHERE name = ? AND pinCode = ?",
                      (self.dateDeRetrait.strftime("%Y-%m-%d %H:%M:%S.%f"), self.solde, user, codePin))
            conn.commit()
            c.execute("INSERT INTO retraits (name, pinCode, amount, date) VALUES (?, ?, ?, ?)",
                      (user, codePin, montant, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
            conn.commit()
            print("Vous avez retiré :", montant)
            print("Il vous reste :", self.solde)
        else:
            print("Solde insuffisant sur le compte ou montant quotidien maximum atteint.")
        """