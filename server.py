from socket import *
import random

# set server's port
serverPort = 1501

# create socket object
serverSocket = socket(AF_INET,SOCK_STREAM)

# k
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

# Status codes
STATUS_GAME_INITIALIZATION = 100
STATUS_INVALID_CHARACTER = 110
STATUS_ALREADY_GUESSED = 130
STATUS_CORRECT_ALPHABET = 150
STATUS_PLAYER_WIN = 200
STATUS_PLAYER_LOSE = 300


def generateTheme()->str:
    print("This round will be in theme...", end="")

    theme = random.choice(["School Life","Metaverse","Detective","Carnival and Fairs"])
    print(theme)
    return theme

def generateWord(theme:str)->str: 

    match theme:
        case "School Life":
            answer = random.choice(["pencil", "principal", "pen", "teacher", "professor", "locker", "prodigy", 
                                    "canteen", "friend", "classmate", "classroom", "basketball court"])
        case "Metaverse":
            answer = random.choice(["hemp", "cosmetic", "ingredient", "corn", "milk", "mixed reality", "server", 
                                    "bigbang theory", "database", "frontend", "backend"])
        case "Detective":
            answer = random.choice(["magnifying glass", "evidence", "fingerprint", "alibi", "suspicious", "sanity", 
                                    "decease", "suspect", "predict", "breakthrough", "suspect", "criminal"
                                    ,"examination", "forensic"])
        case "Carnival and Fairs":
            answer = random.choice(["rollercoaster", "carousel", "amusement park", "clown", 
                                    "balloon", "ferris wheel", "bumper car","festival", 
                                    "entertainment", "booth", "festivity", "merry-go-round"])


    print(f"The answer for this round is... {answer}")
    return answer.lower()

theme = ""
livesRemaining = 5
guessed_letters = []
alphabetPrompt = "a b c d e f g h i j k l m n\no p q r s t u v w x y z"
gameStart = False
gameEnd = False

while(not gameEnd):
    connectionSocket, addr = serverSocket.accept()
    # read data received from client
    receivedAlphabet = connectionSocket.recv(1024).decode().strip().lower()
    if(receivedAlphabet=="start" and not gameStart):
        gameStart = True
        theme = generateTheme()
        answer = generateWord(theme)
        reply = f"{STATUS_GAME_INITIALIZATION},Welcome to the hangman show!\n"\
        + f"This round will be in theme...{theme}\nThe game will begin... NOW!"
        
    elif(len(receivedAlphabet)!=1 or not receivedAlphabet.isalpha()):
        reply = f"{STATUS_INVALID_CHARACTER},Please... That's not what you should answer :)"

    elif(receivedAlphabet in guessed_letters):
        reply = f"{STATUS_ALREADY_GUESSED},You've already guessed that alphabet!"
    
    elif(receivedAlphabet in answer):
        reply = f"{livesRemaining},great choice! That alphabet is in the answer."
        guessed_letters.append(receivedAlphabet)
    
    else:
        livesRemaining -= 1
        guessed_letters.append(receivedAlphabet)
        if(livesRemaining>0):
            reply = f"{livesRemaining},bruh ¯\_(ツ)_/¯"
        else:
            reply = f"{STATUS_PLAYER_LOSE},You LOSE! (╯°□°）╯︵ ┻━┻\nThe correct word is {answer}!"
            gameEnd = True
    
    # generate word display
    displayWord = ""
    for letter in answer:
        if letter in guessed_letters:
            displayWord += letter
        elif (not str(letter).isalpha()):
            displayWord += letter
        else:
            displayWord += "_"

    if("_" not in displayWord):
        reply = f"{STATUS_PLAYER_WIN},Congratulations! ╰(*°▽°*)╯\nThe correct word is {answer}!"
        gameEnd = True
    
    reply += ",---------\n" + displayWord
    print(reply)
    print("guessed letters:",guessed_letters)

    for letter in guessed_letters:
        alphabetPrompt = alphabetPrompt.replace(letter, "-")
    reply += "\n" + alphabetPrompt
    
    connectionSocket.send(reply.encode())
    
    connectionSocket.close()