import sqlite3
from datetime import datetime

class bankAccount:
    def __init__(self):
        self.dateDeRetrait = None
        self.montantRetirerAujd = 0

    def Retrait(self, montant, user, codePin):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()

        # Effectuez une requête SELECT pour récupérer le solde depuis la base de données
        c.execute("SELECT solde FROM users WHERE name = ? AND pinCode = ?", (user, codePin))
        row = c.fetchone()
        if row is not None:
            self.solde = row[0]
            print("Solde initial:", self.solde)
        else:
            print("Aucun utilisateur correspondant trouvé dans la base de données.")
            return

        if self.dateDeRetrait is None:
            self.dateDeRetrait = datetime.now()

        diff = datetime.now() - self.dateDeRetrait
        hours = diff.total_seconds() / 3600

        if hours > 24:
            self.montantRetirerAujd = 0

        if montant < self.solde and self.montantRetirerAujd < 200:
            self.solde -= montant
            self.montantRetirerAujd += montant
            self.dateDeRetrait = datetime.now()
            c.execute("UPDATE users SET dernier_retrait = ? WHERE name = ? AND pinCode = ?",
                      (self.dateDeRetrait, user, codePin))
            conn.commit()
            print("Vous avez retiré :", montant)
            print("Il vous reste :", self.solde)
        else:
            print("Solde insuffisant sur le compte.")
