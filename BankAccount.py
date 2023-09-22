import sqlite3
from datetime import datetime, timedelta
from math import floor

class BankAccount:
    def __init__(self):
        self.dateDeRetrait = None
        self.solde = 0

    def Retrait(self, user, codePin):
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

        montant = int(input("Combien voulez-vous retirer ? :"))

        while montant < 20 or montant % 10 != 0:
            montant = int(input("Entrez un multiple de 10 entier, le retrait minimum est de 20€ :"))

        un_jour_avant = datetime.now() - timedelta(hours=24)
        c.execute("SELECT SUM(amount) FROM retraits WHERE name = ? AND date >= ?", (user, un_jour_avant))
        total_retraits_24h = c.fetchone()[0] or 0

        if total_retraits_24h + montant > 20000:
            print("La somme des retraits des dernières 24 heures dépasse 200.00 €. Retrait impossible.")
        elif montant <= self.solde:
            self.solde -= montant
            c.execute("UPDATE users SET dernier_retrait = ?, solde = ? WHERE name = ? AND pinCode = ?",
                      (self.dateDeRetrait.strftime("%Y-%m-%d %H:%M:%S.%f"), self.solde, user, codePin))
            conn.commit()
            c.execute("INSERT INTO retraits (name, pinCode, amount, date) VALUES (?, ?, ?, ?)",
                      (user, codePin, montant, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
            conn.commit()

            if montant >= 30:
                petit_ou_gros = ""

                while petit_ou_gros != "p" and petit_ou_gros != "g":
                    try:
                        petit_ou_gros = input(
                            "Voulez-vous retirer des petits ou des gros billets ? Entrez 'p' ou 'g' : ").lower()
                        if petit_ou_gros == "p":
                            nb_billet_20 = floor(montant / 20)
                            reste = montant - nb_billet_20 * 20
                            nb_billet_10 = int(reste / 10)

                            message = "Vous avez retiré :"
                            if nb_billet_20 > 0:
                                message += " " + str(nb_billet_20) + " billet(s) de 20 €"
                            if nb_billet_10 >= 1:
                                message += " " + str(int(nb_billet_10)) + " billet(s) de 10 €"
                            if nb_billet_10 > int(nb_billet_10):
                                message += " et " + str(int((nb_billet_10 - int(nb_billet_10)) * 10)) + " pièce(s) de 10 €"
                            print(message)

                        if petit_ou_gros == "g":
                            nb_billet_50 = 0
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

                            message = "Vous avez retiré :"
                            if nb_billet_100 > 0:
                                message += " " + str(nb_billet_100) + " billet(s) de 100 €"
                            if nb_billet_50 > 0:
                                message += " " + str(nb_billet_50) + " billet(s) de 50 €"
                            if nb_billet_20 > 0:
                                message += " " + str(nb_billet_20) + " billet(s) de 20 €"
                            if nb_billet_10 >= 1:
                                message += " " + str(int(nb_billet_10)) + " billet(s) de 10 €"
                            if nb_billet_10 > int(nb_billet_10):
                                message += " et " + str(int((nb_billet_10 - int(nb_billet_10)) * 10)) + " pièce(s) de 10 €"
                            print(message)
                        else:
                            print("Veuillez répondre par 'p' ou 'g'.")
                    except:
                        print("Veuillez entrer un caractère valide.")
                        print("Veuillez répondre par 'p' ou 'g'.")

            print(str(montant) + " € retiré")
            print("Il vous reste :", str(self.solde) + " €")
        else:
            print("Solde insuffisant sur le compte ou montant quotidien maximum atteint.")

    def History(self):
        affiche_historique = ""
        while affiche_historique != "o" and affiche_historique != "n":
            try:
                affiche_historique = input("Voulez-vous un historique de vos retraits ? o/n : ").lower()
                if affiche_historique == "o":
                    # Affiche l'historique des retraits ici en interrogeant la base de données
                    pass
                elif affiche_historique == "n":
                    pass  # Vous pouvez ajouter ici le code pour gérer le cas où l'utilisateur ne veut pas d'historique
                else:
                    print("Veuillez répondre par 'o' ou 'n'.")
            except:
                print("Veuillez entrer un caractère valide.")
                print("Veuillez répondre par 'o' ou 'n'.")


# Vous devrez instancier la classe BankAccount et appeler la méthode Retrait pour effectuer des retraits.
