#Imports
from tkinter import *
from PIL import ImageTk,Image

import wikipedia
import aiml
import time

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
#    chat.tag_configure("left", justify="left")
        chat.insert(END,"User: " +  question + "\n")
        chat.see("end")
#    chat.tag_add("left", "1.0", "end")
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
                    botAnswer("Sorry, I do not know that. Be more specific!")
            elif cmd == 99:
                botAnswer("I did not get that, please try again.")
        else:
            botAnswer(answer)
    
def botAnswer(answer):
    chat.config(state = NORMAL)
#    chat.tag_configure("right", justify="right", foreground="green")
    chat.insert(END, "Bot: " + answer + "\n")
    chat.see("end")
#    chat.tag_add("right", "1.0", "end")
    chat.config(state = DISABLED)

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

#Bot
kern = aiml.Kernel()
kern.setTextEncoding(None)

kern.bootstrap(learnFiles = "alcohol-wizard.xml")

greeting = "Greetings, I am the Alcohol Wizard, how can I help?"
botAnswer(greeting)

root.mainloop()
