class connection :
    def __init__(self, name, codePin):
        self.name = name
        self.codePin = codePin

    def Connect(self):
        import sqlite3

        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        # c.execute("""CREATE TABLE users (
        #           name TEXT,
        #           pinCode INTEGER
        #   )""")

        # c.execute("INSERT INTO users VALUES ('user', 1234)")
        checkUser = self.name
        checkCodePin = self.codePin

        sql = "SELECT * FROM users WHERE name = ? AND pinCode = ?"
        c.execute(sql, (checkUser, checkCodePin))
        results = c.fetchall()
        if results:
            print("Connection établie !")
            return True