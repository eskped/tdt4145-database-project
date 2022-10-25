# importerer funksjoner og biblitek som hjelper med grensesnittet
from KaffeDB_utils import *
from rich.console import Console
from rich.theme import Theme

# kommenter ut linjen under for å lage ny database med data fra KaffeDBfillData.sql
# import CreateDB

# lager innstillinger for eget tema
custom_theme = Theme({"success": "bold green", "error": "bold red"})
console = Console(theme=custom_theme)

def main():
    clear()
    printWelcome()
    printMenu()
    printNL() # printer ny linje
    
    try:
        userInput = int(console.input("[bold blue]Valg: [/]"))
    except ValueError:
        userInput = -2
    
    while userInput != -1:
        clear()
        if userInput == 0:
            clear()
        elif userInput == 1:
            addCoffeeToDataBaseInterface()
        elif userInput == 2:
            consolePrint("Brukere som har smakt flest unike kaffer så langt i år, sortert synkende:", "success")
            getUserTastedCoffes()
        elif userInput == 3:
            consolePrint("Kaffer som gir forbrukeren mest for pengene ifølge KaffeDBs brukere (høyeste gjenomsnittsscore kontra pris), sortert synkende:", "success")
            getBestValuedCoffes()
        elif userInput == 4:
            consolePrint("""Kaffer beskrevet som "floral", enten av brukere eller brennerier:""", "success")
            getCoffesDescribedAsFloral()
        elif userInput == 5:
            consolePrint("Kaffer fra Rwanda eller Colombia som ikke er vaskede:", "success")
            getNonWashedCoffesFromRwandaOrColombia()
        else:
            consolePrint("Ugyldig valg. Du må skrive inn -1, 0, 1, 2, 3, 4 eller 5.", "error")
        printMenu()
        
        try:
            userInput = int(console.input("[bold blue]Valg: [/]"))
        except ValueError:
            userInput = -2
            
    consolePrint("\nDu har avsluttet økten.", "success")
    print("Takk for besøket!")
    
    
##Denne funksjonen lager grensesnittet for brukerhistorie 1 og bruker hjelpefunksjoner til å validere input.
def addCoffeeToDataBaseInterface():
    print("For å legge inn en kaffe du har smakt må du logge inn med epost og passord.")
    
    validEpostadresse = login()
    while validEpostadresse == None:
        if goBackToMenu():
            return
        validEpostadresse = login()
    
    print("Her er en oversikt over alle registrerte kaffer med tilhørende brennerinavn og -sted:")
    printCoffeInfo()
    print("\nVennligst skriv inn nødvendige opplysninger nedenfor for å registrere en kaffe du har smakt. Merk at du kun kan ha lagret én kaffesmaking per unike kaffe.")
    
    brenneristedInput = console.input("[bold #59bfff]Brenneristed: [/]")
    validBrenneriID, validBrenneriNavn = getBrenneriIDAndName(brenneristedInput)
    while validBrenneriID == None or validBrenneriNavn == None:
        if goBackToMenu():
            return
        brenneristedInput = console.input("[bold #59bfff]Brenneristed: [/]")
        validBrenneriID, validBrenneriNavn = getBrenneriIDAndName(brenneristedInput)
    
    kaffenavn = getKaffenavn(validBrenneriID)
    while kaffenavn == None:
        if goBackToMenu():
            return
        kaffenavn = getKaffenavn(validBrenneriID)    
    
    poeng = getPoeng()
    while poeng == None:
        if goBackToMenu():
            return
        poeng = getPoeng()
    
    smaksnotat = getSmaksnotat()
    while smaksnotat == None:
        if goBackToMenu():
            return
        smaksnotat = getSmaksnotat()

    if addCoffeeToDataBase(validBrenneriID,validEpostadresse, validBrenneriNavn, brenneristedInput, kaffenavn, poeng, smaksnotat):
        consolePrint("Kaffen har blitt lagt til databasen.", "success")
    else:
        consolePrint("Kaffesmakingen har blitt oppdatert", "success")
        

    print("Du blir nå logget ut og tatt tilbake til menyen.\n")
    clear()

""" Ulike hjelpefunksjoner som validerer login og finner og validerer kaffe og brenneri,
 ved hjelp av valideringsmetoder i KaffeDB_utils.py """
def login():
    Epostadresse = console.input("[bold #59bfff]Epostadresse: [/]")
    Passord = console.input("[bold #59bfff]Passord: [/]")
    correctLogin = validateLogIn(Epostadresse, Passord)
    if correctLogin == True:
        consolePrint("Riktig epostadresse og passord.\n", "success")
        return Epostadresse
    consolePrint("Feil epostadresse eller passord.", "error")
    return None

def getBrenneriIDAndName(brenneristedInput):
    BrennerinavnInput = console.input("[bold #59bfff]Brennerinavn: [/]")
    if validateBrenneri(BrennerinavnInput, brenneristedInput) != None:
        return validateBrenneri(BrennerinavnInput, brenneristedInput), BrennerinavnInput
    consolePrint("Du må skrive inn et gyldig brennerinavn og sted som eksisterer i databasen. Prøv igjen.", "error")
    return None, None
 
def getKaffenavn(BrenneriID):
    KaffenavnInput = console.input("[bold #59bfff]\nKaffenavn: [/]")
    if validateKaffenavn(KaffenavnInput, BrenneriID) != None:
        return validateKaffenavn(KaffenavnInput, BrenneriID)
    consolePrint("\nDu må skrive inn et gyldig kaffenavn som eksisterer i databasen fra det oppgitte brenneriet. Prøv igjen.", "error")
    return None

def getPoeng():
    PoengInput = console.input("[bold #59bfff]\nPoeng: [/]")
    if validatePoeng(PoengInput) != None:
        return validatePoeng(PoengInput)
    consolePrint("\nDu må skrive inn en en gyldig poengsum som er minst 1 og maks 10. Prøv igjen.", "error")
    return None

def getSmaksnotat():
    Smaksnotat = console.input("[bold #59bfff]\nSmaksnotat: [/]")
    if validateSmaksnotat(Smaksnotat) != None:
        return Smaksnotat
    consolePrint("\nDu må skrive inn en et gyldig notat på maks 280 tegn. Prøv igjen.", "error")
    return None


##Ved ugyldig input sendes brukeren til denne menyen. Lar brukeren gå tilbake til hovedmenyen eller prøve på nytt.
def goBackToMenu():
    userInput = -1
    while(userInput == -1):
        print("\nØnsker du å gå tilbake til menyen [1] eller prøve igjen [2]?")
        try:
            userInput = int(console.input("[bold blue]Valg: [/]"))
        except ValueError:
            userInput = -1
        if (userInput == 1):
            clear()
            return True
        elif (userInput == 2):
            return False
        else:
            console.print("Ugyldig valg. Du må skrive inn 1 eller 2.\n", style="error")  
            userInput = -1

##Funksjon som printer ut menyen til terminalen
def printMenu():
    printNL()
    console.print("""[default][underline bold]Meny[/]:
[bold][-1][/] for å avslutte økten.
[bold][0][/]  for å få opp denne menyen igjen.
[bold][1][/]  for å regisrere en kaffesmaking. 
[bold][2][/]  for en liste over brukere som har smakt flest unike kaffer så langt i år, sortert synkende.
[bold][3][/]  for en liste over kaffer som gir forbrukeren mest verdi for pengene ifølge KaffeDBs brukere (høyeste gjenomsnittsscore kontra pris), sortert synkende.
[bold][4][/]  for en liste over kaffer som er beskrevet som "floral", enten av brukere eller brennerier.
[bold][5][/]  for en liste over kaffer fra Rwanda eller Colombia som ikke er vaskede.[/]""")
    printNL()

##Rydder terminalen
def clear():
    print(chr(27) + "[2J")
    print(chr(27) + "[2J")
    print(chr(27) + "[2J")
    
def printNL():
    print("\n")
    
def consolePrint(text, textStyle):
    console.print(text, style=textStyle)

##Funksjon som kalles når applikasjonen starter.
def printWelcome():
    console.print("[bold] Velkommen til KaffeDB!")
    console.print("[bold] Her kan du registrere kaffesmakinger og finne informasjon om andre kaffer.")
    console.print("""[default bold]
            
                        )     (
                 ___...(-------)-....___
             .-""       )    (          ""-.
       .-'``'|-._       (     )         _.-|
      /  .--.|   `""---...........---""`   |
     /  /    |                             |
     |  |    |                             |
      \  \   |                             |
       `\ `\ |                             |
         `\ `|                             |        KaffeDB ☕🗄️
         _/ /\                             /
        (__/  \                           /
     _..---""` \                         /`""---.._
  .-'           \                       /          '-.
 :               `-.__             __.-'              :
 :                  ) ""---...---"" (                 :
  '._               `"--...___...--"`              _.'
    \""--..__                              __..--""
     '._     \"""----.....______.....----\"""     _.'
        `""--..,,_____            _____,,..--""`
                      `\"""----\"""`                                                        
    [/]""")

main()