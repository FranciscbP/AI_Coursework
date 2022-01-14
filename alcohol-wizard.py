#Imports
from tkinter import *
from PIL import ImageTk,Image
import string
import aiml
import wikipedia
import pandas as pd
import nltk
from nltk.corpus import stopwords

#Initialize Window
root = Tk()
root.geometry("800x300")
root.iconbitmap("Images/alcohol_icon.ico")
root.title("Alcohol Wizard Bot")
root.config(bg="#E0B953")
root.resizable(False, False) 

#Funtions
def askQuestion(event=None):
    question = questionTxt.get()

    if question != "":
        chat.config(state = NORMAL)
        chat.insert(END,"User: " +  question + "\n")
        chat.see("end")
        chat.config(state = DISABLED)

        questionTxt.delete(0, END)

        #pre-process user input and determine response agent (if needed)
        responseAgent = 'aiml'
        #activate selected response agent
        if responseAgent == 'aiml':
            answer = kern.respond(question)
        #post-process the answer for commands
        if answer[0] == '#':
            params = answer[1:].split('$')
            cmd = int(params[0])
            if cmd == 0:
                botAnswer(params[1])
            elif cmd == 1:
                try:
                    wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
                    botAnswer(wSummary)
                except:
                    botAnswer(getSimilarQuestion(question))
            elif cmd == 99:
                botAnswer(getSimilarQuestion(question))
        else:
            botAnswer(answer)
    
def botAnswer(answer):
    chat.config(state = NORMAL)
    chat.insert(END, "Bot: " + answer + "\n\n")
    chat.see("end")
    chat.config(state = DISABLED)

def similarQuestions(userQuestion,predefinedQuestion):    
    #Normalize
    lemmer = nltk.stem.WordNetLemmatizer()
    
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    
    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
    
    uQuestion_list = LemNormalize(userQuestion)
    preQuestion_list = LemNormalize(predefinedQuestion)
    
    #Get Stop Words
    stopWordsList = stopwords.words('english')
    #Remove Stop Words
    uQuestion_set = {w for w in uQuestion_list if not w in stopWordsList} 
    preQuestion_set = {w for w in preQuestion_list if not w in stopWordsList}
      
    #Create vector containing words of both strings
    l1 =[]
    l2 =[]   
    rvector = uQuestion_set.union(preQuestion_set) 
    for w in rvector:
        if w in uQuestion_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in preQuestion_set: l2.append(1)
        else: l2.append(0)
        
    #Cosine Formula 
    c = 0
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine
    
def getSimilarQuestion(userQuest):
    #Return Answer from Similar Question
    i = 0
    biggestSimilarity = 0
    similarQuestion = 0

    for cont in qaQuestions:
        if similarQuestions(userQuest,qaQuestions[i]) > biggestSimilarity:
            biggestSimilarity = similarQuestions(userQuest,qaQuestions[i])
            similarQuestion = i
            
        i = i + 1
    if biggestSimilarity > 0.7:
        return qaAnswers[similarQuestion]
    else:
        return "Sorry, I do not know that. Be more specific!"

#Widgets
chat = Text(root, height = 14, width = 70, bd = 2, state = DISABLED)
chat.place(x = 20, y = 20)

questionTxt = Entry(root, width = 75)
questionTxt.place(x = 20, y = 265)

questionBtn = Button(root, text = "Ask Question", width = 12, command = askQuestion)
questionBtn.place(x = 492, y = 262)

root.bind('<Return>', askQuestion) #When Return is Pressed, calls askQuestion Function

closeBtn = Button(root, text = "Close Bot", width = 12, command = root.destroy)
closeBtn.place(x = 645, y = 262)

#Image
image = Image.open("Images/alcohol_img.png")

resize_image = image.resize((100, 100))
img = ImageTk.PhotoImage(resize_image)

imageLbl = Label(image = img, bg = "#E0B953")
imageLbl.image = img
imageLbl.place(x = 640, y = 20)

#Kernel
kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles = "alcohol-wizard.xml")

#QA CSV
qa = pd.read_csv("qaAlcohol.csv")
qaQuestions = qa['Question'].tolist()
qaAnswers = qa['Answer'].tolist()

greeting = "Greetings, I am the Alcohol Wizard, how can I help?"
botAnswer(greeting)

root.mainloop()
