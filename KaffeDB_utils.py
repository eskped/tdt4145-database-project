import sqlite3
from prettytable import PrettyTable

# Brukerhistorie 1
def validateLogIn(Epostadresse, Passord):
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Passord
        FROM Bruker
        WHERE Epostadresse = ?
    """, (Epostadresse,))
    row = cursor.fetchone()
    con.close()
    if row is None:
        return None
    if row[0] == Passord:
        return True
    return False

def addCoffeeToDataBase(BrenneriID, Epostadresse, Brennerinavn, Brenneristed, Kaffenavn, Poeng, Smaksnotat):
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    # Finner BrukerID
    cursor.execute("""
        SELECT BrukerID
        FROM Bruker
        WHERE Epostadresse = ?
    """, (Epostadresse,))
    row = cursor.fetchone()
    BrukerID = row[0]
    # Finner Dato
    cursor.execute("SELECT DATE('now')")
    row = cursor.fetchone()
    Dato = row[0]
    # Sjekker UNIQUE constraint
    cursor.execute("""
        SELECT BrukerID, Kaffenavn, BrenneriID
        FROM HarSmakt
        WHERE (BrukerID, Kaffenavn, BrenneriID) = (?, ?, ?)
    """, (BrukerID, Kaffenavn, BrenneriID,))
    row = cursor.fetchone()
    if (row is None):
        cursor.execute("INSERT INTO HarSmakt VALUES (?, ?, ?, ?, ?, ?)", (BrukerID, Kaffenavn, BrenneriID, Poeng, Smaksnotat, Dato))
        con.commit()
        con.close()
        return True
    else:
        cursor.execute("""
            UPDATE HarSmakt
            SET Poeng = (?),
                Notat = (?)
            WHERE (BrukerID, Kaffenavn, BrenneriID) = (?, ?, ?)
        """, (Poeng, Smaksnotat, BrukerID, Kaffenavn, BrenneriID,))
        con.commit()
        con.close()
        return False

def validateBrenneri(Brennerinavn, Brenneristed):
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    # Finner BrenneriID
    cursor.execute("""
        SELECT BrenneriID
        FROM Brenneri
        WHERE (Navn, Sted) = (?, ?)
    """, (Brennerinavn, Brenneristed))
    row = cursor.fetchone()
    if (row is None):
        return None
    BrenneriID = row[0]
    return BrenneriID

def validateKaffenavn(Kaffenavn, BrenneriID):
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
     # Finner Kaffenavn
    cursor.execute("""
        SELECT Navn
        FROM Kaffe
        WHERE (Navn, BrenneriID) = (?, ?)
    """, (Kaffenavn, BrenneriID))
    row = cursor.fetchone()
    if (row is None):
        return None
    Kaffenavn = row[0]
    return Kaffenavn

def validatePoeng(Poeng):
    try:
        Poeng = int(Poeng)
    except ValueError:
        return False
    if (Poeng < 1 or Poeng > 10):
        return None
    return int(Poeng)

def validateSmaksnotat(Smaksnotat):
    if len(Smaksnotat) > 280:
        return None
    return Smaksnotat

def printCoffeInfo():
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Kaffe.Navn AS Kaffenavn, Brenneri.Navn AS Brennerinavn, Sted AS Brenneristed
        FROM Kaffe INNER JOIN Brenneri USING (BrenneriID)
        """)
    rows = cursor.fetchall()
    x = PrettyTable()
    x.field_names = ["Kaffenavn", "Brennerinavn", "Brenneristed"]
    for row in rows:
        x.add_row([row[0], row[1], row[2]])
    print(x)
    con.close()

# Brukerhistorie 2
def getUserTastedCoffes():
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT FulltNavn, count(*) AS AntallUnikeKafferSmakt
        FROM Bruker
        INNER JOIN HarSmakt USING (BrukerID)
        INNER JOIN Kaffe ON KaffeNavn = Navn
        WHERE SUBSTR(HarSmakt.Dato, 1, 4) = SUBSTR(DATE('now'), 1, 4)
        GROUP BY BrukerID, FulltNavn
        ORDER BY AntallUnikeKafferSmakt DESC;
        """)    
    
    rows = cursor.fetchall()
    rowNum = 1
    x = PrettyTable()
    x.field_names = ["Rangering", "Navn", "Antall unike kaffer smakt"]
    for row in rows:
        x.add_row([rowNum, row[0], row[1]])
        rowNum += 1
    print(x)
    con.close()


# Brukerhistorie 3
def getBestValuedCoffes():
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Brenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn, KiloprisNOK, avg(Poeng) AS Gjennomsnittspoeng
        FROM Kaffe
            INNER JOIN HarSmakt ON (Kaffe.Navn = KaffeNavn) AND (HarSmakt.BrenneriID = HarSmakt.BrenneriID)
            INNER JOIN Brenneri USING (BrenneriID)
        GROUP BY Brenneri.BrenneriID, Brenneri.Navn, Kaffe.Navn, KiloprisNOK
        ORDER BY Gjennomsnittspoeng/KiloprisNOK DESC;
        """)
    rows = cursor.fetchall()
    rowNum = 1
    x = PrettyTable()
    x.field_names = ["Rangering", "Brenneri", "Kaffenavn", "Pris", "Gjennomsnittsscore"]
    for row in rows:
        x.add_row([rowNum, row[0], row[1], str(row[2]) + " NOK", str(row[3]) + "/10.0"])
        rowNum += 1
    print(x)
    con.close()

# Brukerhistorie 4
def getCoffesDescribedAsFloral():
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT DISTINCT Brenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn
        FROM Kaffe
            LEFT OUTER JOIN HarSmakt ON (Kaffe.Navn = KaffeNavn) AND (Kaffe.BrenneriID = HarSmakt.BrenneriID) 
            INNER JOIN Brenneri USING (BrenneriID)
        WHERE (HarSmakt.Notat LIKE '%floral%') OR (Kaffe.Notat LIKE '%floral%')
        """)
    rows = cursor.fetchall()
    x = PrettyTable()
    x.field_names = ["Brennerinavn", "Kaffenavn"]
    for row in rows:
        x.add_row([ row[0], row[1]])
    print(x)
    con.close()

# Brukerhistorie 5
def getNonWashedCoffesFromRwandaOrColombia():
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT Brenneri.Navn AS Brennerinavn, Kaffe.Navn AS Kaffenavn
        FROM Kaffe
            INNER JOIN Kaffeparti USING (KaffepartiID)
            INNER JOIN Brenneri USING (BrenneriID)
            INNER JOIN Gaard USING (GaardID)
            INNER JOIN Foredlingsmetode ON Foredlingsmetode.Navn = ForedlingsmetodeNavn
        WHERE ((Gaard.Land = 'Rwanda') OR (Gaard.Land = 'Colombia'))
            AND (Foredlingsmetode.Navn <> 'Vasket')
        """)
    rows = cursor.fetchall()
    rowNum = 1
    x = PrettyTable()
    x.field_names = ["Brennerinavn", "Kaffenavn"]
    for row in rows:
        x.add_row([ row[0], row[1]])
    print(x)
    con.close()
    
