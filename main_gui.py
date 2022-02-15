'''

    Main -  Run File


'''



import random
import json

import torch
from model import NeuralCode
import pyglet
import time
from tkinter import *
from bot_utils import *
import time


# bot variables
idk = "I do not understand"
bot_name = "Globot"

json_file = 'F:\GLOBOT\GLOBOT\data_file.json'

quit_txt =["quit", "OK go to sleep",
            "okay go to sleep", "sleep", "OK goto sleep"]
fun_txt = ["activate fun mode", "change mode"]


# FUN MODE SECTION 
'''
IGNORE THIS PART

def fun_mode():
    end_fun_mode = ["end fun mode", "return to normal mode", "activate normal mode",
                    "normal mode", "switch to normal mode", "quit"]
    fun_mode_run = True
    
    while(fun_mode_run):
        sentence , key, sender = recognizer()
        if sentence in end_fun_mode :
            Application._insert_message("Fun Mode Terminated, starting normal mode", bot_name)
            print(f'{bot_name}: Fun Mode Terminated, starting normal mode')
            talk('Fun Mode Terminated, starting normal mode')
            fun_mode_run = False
            
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if(key == 1):
            break
        elif(key == 2):
            pass
        elif(key == 0):
            if prob.item() > 0.75:
                for intent in intents["customs"]:
                    if tag == intent["tag"]:
                        a = random.randint(0, (len(intent["responses"])-1))
                        print(f'{bot_name}: {(intent["responses"][a])}')
                        talk(intent["responses"][a])
                        mp3_file = intent["link"][0]
                        music = pyglet.resource.media(mp3_file)
                        music.play()
                        time.sleep(intent["time"])
                        print(f'{bot_name} :Sir,what can I do for you next') 
                        talk("Sir,what can I do for you next")
                        
        else:
            print(f'{bot_name}: I do not Understand...')
            talk("I do not Understand...")
'''
# NORMAL MODE SECTION
def normal_mode(sentence):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open(json_file, 'r') as data_file:
        intents = json.load(data_file)

    File = 'data.pth'
    data = torch.load(File)

    input_size = data["input_size"]
    output_size = data["output_size"]
    hidden_size = data["hidden_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralCode(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    #if(key == 1):
     #   return
    #elif(key == 2):
    #    pass
    #elif(key == 0):
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                a = random.randint(0, (len(intent["responses"])-1))
                #print(f'{bot_name}: {(intent["responses"][a])}')
                return intent["responses"][a]
           
    else:
        return idk
        #print(f'{bot_name}: I do not Understand...')
        #talk("I do not Understand...")


# GUI SECTION

#variables
PASSWORD = "a"
WIDTH = 1200
HEIGHT = 700
BG_COLOR = "#34568B" #"#00758fr" 
TEXT_COLOR = "#EAECEE"
FONT = "Arial 14"
FONT_BOLD = "Calibri 19 bold"
PROCESSING_COLOR = "#1e81b0"
RUN_COLOR = "#00FF00" 
ERR_COLOR = "#FF0000"
#SETTING_ICO = "F:\\GLOBOT\\assets\\setting.png"
SETTING_BG = "#eab676"


class Application: 

    def __init__(self):
        self.window = Tk()
        self._main_window()
    
    def run(self):
        self.window.mainloop()
        

    def _main_window(self):
        self.window.title("GLOBOT")
        #self.window.iconbitmap("assets/icon.ico")
        #self.window.resizable(width = False, height = False)
        self.window.configure(width = WIDTH , height = HEIGHT, bg = BG_COLOR )

        # head title
        self.head_title = Label(self.window, bg = BG_COLOR, fg = "#FF0000",
                        text  ="Welcome To Global College", font = FONT_BOLD, pady = 10)
        self.head_title.place(relwidth=1)
        
        # divider
        divider = Label(self.window, width = 690, bg = TEXT_COLOR)
        divider.place(relwidth=1, rely= 0.07, relheight=0.006)    
        
        #text widget
        self.text_widget = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.text_widget.place(relheight=0.92, relwidth=1,rely=0.08 )  
        self.text_widget.configure(cursor = "arrow", state = DISABLED)
        
        # scroll bar
        sb = Scrollbar(self.text_widget)
        sb.place(relheight=1, relx = 0.989)
        sb.configure(command=self.text_widget.yview)

        # self._insert_message("Hello Sir, You can ask me whatever you want, Please say QUIT to exit",0, "GLOBOT")

        # button
        self.start_button = Button(text = "Start", font=FONT_BOLD, width = 20, bg = "#FFFFFF",
                              command = lambda: self._on_enter_pressed(NONE))
        self.start_button.place(relx=0.87, rely= 0.008 , relheight=0.06, relwidth= 0.12)


        # listening status indicator:
        self.indic = Label(self.window, text="Stopped", width =50, bg = BG_COLOR, 
                     fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.indic.place(relheight= 0.05, relwidth=0.1, rely=0.01, relx=0.01)
        
        
        # indicator blip 
        self.blip = Label(self.window, text = "",  width = 8, height = 8, bg = "#FF0000", font = FONT, padx = 5, pady = 5)
        self.blip.place(relheight=0.02, relwidth=0.015, rely=0.025, relx=0.011)
        
        # settings button
        self.settings_button = Button(self.window, text= "#",font=FONT_BOLD, command= lambda: self._password_page(NONE), borderwidth=0)
        self.settings_button.place(relx=0.82, rely=0.008, relheight=0.06, relwidth=0.04)
    
    
    def _password_page(self,event):
      
        def back_to_main_window_from_pass():
            self.pass_enter_button.destroy()
            self.pass_enter_text.destroy()
            self.pass_label.destroy()
            self.window.update()
            self._main_window()
        
        def pass_check():
            try:
                password = self.pass_enter_text.get(1.0, "end-1c")
            except TclError :
                self.pass_label.configure(text="Incorrect Password", fg="#FF0000")
                self.window.update()
                talk("Access Denied")
                self.pass_label.configure(text="Enter Password", fg = "#000000")
                    
                self.window.update()
            
            if password == PASSWORD:
                self.pass_label.configure(text="Correct Password", fg="#00FF00")
                self.window.update()
                talk("Access Granted")
                  
                self.pass_label.destroy()
                self.pass_enter_button.destroy()
                self.pass_enter_text.destroy()
                
                self._settings_(NONE)
            else:
                self.pass_enter_text.delete(1.0, "end-1c")
                self.pass_label.configure(text="Incorrect Password", fg="#FF0000")
                self.window.update()
                talk("Access Denied")
                self.pass_label.configure(text="Enter Password", fg = "#000000")
                self.pass_enter_text.focus()
                self.window.update()        
              
        
        self.settings_button.destroy()
        self.start_button.destroy()
        self.text_widget.destroy()
        self.blip.destroy()
        self.indic.destroy()
        
        
        
        
        
        self.pass_label = Label(self.window, text="Enter Passsword", font= "Calibri 18 bold")
        self.pass_label.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.3)
        
        # password input box
        self.pass_enter_text = Text(self.window,width = 20, bg = "#FFFFFF",
                                fg = "#000000", font = "Calibri 20 bold", padx = 5, pady = 5 )
        self.pass_enter_text.place(relheight=0.06, relwidth=0.2, relx=0.4, rely=0.4)
        
        # login button    
        self.pass_enter_button = Button(self.window, text="Login", bg="#FFFFFF", fg = "#000000",
                                        font=FONT,command= lambda:pass_check())
        self.pass_enter_button.place(relheight=0.06, relwidth=0.1, relx=0.45, rely=0.5)
        self.pass_enter_text.focus()
        
        
        self.back_button = Button(self.window, text= "<<",font= "Calibri 20", command= lambda: back_to_main_window_from_pass(), borderwidth=0)
        self.back_button.place(relx=0.001, rely=0.007, relheight=0.055, relwidth=0.04)
    
    
    
    
    # setting page:
    def _settings_(self,event):
        
        def _get_tag_list():
            tags_list = []
            with open(json_file) as f:
                temp = json.load(f)
            for intent in temp["intents"]:
                tag = intent["tag"]
                tags_list.append(tag)
            return tags_list
        
        
        
        def reset():
            self.check_tag_button.configure(bg = TEXT_COLOR, text="Check Tag", state="normal")
            self.add_tag_text.configure(state="normal")
            self.add_tag_text.delete(1.0, "end-1c")
            self.add_pattern_button.configure(state="disabled")
            self.add_patterns_text.delete(1.0,"end-1c")
            self.add_patterns_text.configure(state="disabled")
            self.add_response_button.configure(state="disabled")
            self.add_response_text.delete(1.0, "end-1c")
            self.add_response_text.configure(state="disabled")
            self.save_data_button.configure(state="disabled", fg="#000000")
            self.table_.configure(state="normal")
            self.table_.delete(1.0, "end-1c")
            tmp["responses"] = []
            tmp["patterns"] = []
            self.table_.configure(state="disabled")
            self.window.update()
            
            
            
        def add_response():
            temp_response = self.add_response_text.get(1.0, "end-1c")
            if len(temp_response) != 0 and temp_response not in tmp["responses"]:
                
                tmp["responses"].append(temp_response)
                self.add_response_text.delete(1.0, "end-1c")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Response : \"{temp_response}\"\n")
                self.table_.configure(state="disabled")
                self.save_data_button.configure(state="normal", fg = "#00FF00")

            else:
                self.add_response_button.configure(text="Invalid", fg = "#FF0000")
                self.window.update()
                talk("Invalid Response")
                self.add_response_button.configure(text="Add", fg = "#000000")


            
        def add_pattern():
            temp_pattern = self.add_patterns_text.get(1.0, "end-1c")
            if len(temp_pattern) != 0 and temp_pattern not in tmp["patterns"]:
                
                tmp["patterns"].append(temp_pattern)
                self.add_patterns_text.delete(1.0, "end-1c")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Pattern : \"{temp_pattern}\"\n")
                self.table_.configure(state="disabled")
            else:
                self.add_pattern_button.configure(text="Invalid", fg = "#FF0000")
                self.window.update()
                talk("Invalid Pattern")
                self.add_pattern_button.configure(text="Add", fg = "#000000")
        
     
        
        
        def check_tag():
            
            
            tag = self.add_tag_text.get(1.0, "end-1c")
            tags_list = _get_tag_list()
            
            if tag not in tags_list and len(tag) != 0:
                self.add_tag_text.configure(state="disabled")
                self.check_tag_button.configure(state="disabled", text="Valid Tag", bg = "#00FF00")
                self.add_pattern_button.configure(state="normal")
                self.add_patterns_text.configure(state="normal")
                self.add_response_button.configure(state="normal")
                self.add_response_text.configure(state="normal")
                self.table_.configure(state="normal")
                self.table_.insert("end", f"Tag : \"{tag}\"\n")
                self.table_.configure(state="disabled")
                self.window.update()
                

            else:
                self.check_tag_button.configure(text="Invalid Tag",fg="#FF0000")
                self.window.update()
                talk("invalid tag")
                self.check_tag_button.configure(text ="Check Tag", fg = "#000000")
        
        def training():
            pass
        
        def view_data():
            #self.view_data_button.destroy()
            #self.add_data_button.destroy()
            #self.delete_data_button.destroy()
            #self.train_button.destroy()
            self.view_data_button.configure(state="disabled")
            self.back_button.configure(command= lambda: back_to_setting_page())
            self.head_title.configure(text="Data")  
            self.data_table.place(relheight=0.9, relwidth=0.8, relx= 0.17, rely=0.09)
            
            self.data_table.config(state="normal")
          
            with open(json_file, "r") as f:
                file = json.load(f)
                j = 0
                for intent in file["intents"]:
                    tag = intent["tag"]
                    pattern = intent["patterns"]
                    responses = intent["responses"]
                    
                    self.data_table.insert("end", f"\n({j}) Tag : {tag}\n")
                    
                    self.data_table.insert("end", "\nPatterns : \n")
                    
                    i = 0
                    for p in pattern:
                        self.data_table.insert("end", f"{i} : {p}\n")
                        #print(f"{i} : {p}")
                        i+=1
                    
                    self.data_table.insert("end", "\nResponses : \n")
                    
                    i = 0
                    for r in responses:
                        self.data_table.insert("end", f"{i} : {r}\n")
                        #print(f"{i} : {r}")
                        i+=1    
                    self.data_table.insert("end", "\n\n")
                    j +=1
            
            # always see end
            self.data_table.see(END)
            self.data_table.config(state="disabled")
            
            self.window.update()       
               
        def view_tags():
            
            tags_list2 = _get_tag_list()
            
            
            self.tags_table.place(relheight=0.9, relwidth=0.25, relx=0.745, rely=0.09)
            self.tags_table.config(state="normal")
            self.tags_table.delete('1.0',END)
            self.window.update()
            i = 0
            for tag in tags_list2:
                self.tags_table.insert("end", f"{i} : {tag}\n")
                i+=1
            self.tags_table.config(state="disabled")
            self.window.update()
        
        def add_data():
            self.view_data_button.destroy()
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.train_button.destroy()
            self.data_table.destroy()
            self.back_button.configure(command= lambda: back_to_setting_page())
            self.window.update()
            
            self.add_tag_label.place(relwidth=0.2, relheight=0.06,relx=0.05, rely=0.1)
            self.add_tag_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.2)
            self.add_tag_text.focus()
            self.view_tags_button.place(relheight=0.06, relwidth=0.1, relx=0.05, rely=0.3)
            self.check_tag_button.place(relwidth=0.1, relheight=0.06,relx=0.15 ,rely=0.3)
            
            self.add_pattern_label.place(relwidth=0.2, relheight=0.06, relx=0.05,rely=0.4)
            self.add_patterns_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.5)
            self.add_pattern_button.place(relwidth=0.1, relheight=0.06, relx=0.25, rely=0.5)
            
            self.add_response_label.place(relwidth=0.2, relheight=0.06, relx=0.05,rely=0.6)
            self.add_response_text.place(relwidth=0.2, relheight=0.06, relx=0.05, rely=0.7)
            self.add_response_button.place(relwidth=0.1, relheight=0.06, relx=0.25, rely=0.7)
            
            self.save_data_button.place(relwidth=0.1, relheight=0.06, relx=0.15, rely=0.8)
            self.reset_button.place(relwidth=0.1, relheight=0.06, relx=0.05, rely=0.8)
            
            self.table_label.place(relwidth=0.2,relheight=0.06, relx=0.45 , rely=0.1)
            self.table_.place(relheight=0.7, relwidth=0.35, relx=0.38, rely=0.2)
            
            self.window.update()
            
            
        # data entry
        
        def save_data():
            
            save = {}
            with open(json_file,"r") as f:
                temp = json.load(f)
                
            
            save["tag"] = self.add_tag_text.get(1.0, "end-1c")
            save["responses"] = tmp["responses"]
            save["patterns"] = tmp["patterns"]
            
            
            
            temp["intents"].append(save)
            with open(json_file, "w") as f:
                json.dump(temp, f, indent = 4)

            tmp["patterns"]  = []
            tmp["responses"] = []        
        
            self.add_tag_text.configure(state="normal")
            self.add_tag_text.delete(1.0, "end-1c")
            self.add_tag_text.focus()
            
            self.add_patterns_text.delete(1.0, "end-1c")
            self.add_patterns_text.configure(state="disabled")
            self.add_pattern_button.configure(state= "disabled")
            
            self.add_response_text.delete(1.0, "end-1c")
            self.add_response_text.configure(state="disabled")
            self.add_response_button.configure(state= "disabled")
            
            self.check_tag_button.configure(state="normal", fg = "#000000", bg = TEXT_COLOR, text="Check Tag")
            self.save_data_button.configure(state="disabled")
            
            self.table_.configure(state="normal")
            self.table_.delete(1.0, "end-1c")
            self.table_.configure(state="disabled")
            
            view_tags()

            
            self.tags_table.update()
            self.window.update()
            
            
            
        tmp = {}
        
        tmp["responses"] = []
        tmp["patterns"] = []
        
        
            
            
            
            
            
            
            
                      
        def delete_data():
            pass
        
        def back_to_main_page():
            self.add_data_button.destroy()
            self.delete_data_button.destroy()
            self.view_data_button.destroy()
            self.train_button.destroy()
            self.pass_enter_text.destroy()
            self.pass_enter_button.destroy()
            self.pass_label.destroy()
            self.back_button.destroy()
            self.data_table.destroy()
            self.tags_table.destroy()
            
            self.window.update()
            
            self._main_window()
        
        def back_to_setting_page():
            self.add_tag_text.destroy()
            self.add_tag_label.destroy()
            self.add_pattern_label.destroy()
            self.add_pattern_button.destroy()
            self.add_patterns_text.destroy()
            self.add_response_label.destroy()
            self.add_response_button.destroy()
            self.add_response_text.destroy()
            self.check_tag_button.destroy()
            self.reset_button.destroy()
            self.save_data_button.destroy()
            self.view_tags_button.destroy()
            self.data_table.destroy()
            self.tags_table.destroy()
            self.table_.destroy()
            self.table_label.destroy()
            self.view_data_button.destroy()
            self.delete_data_button.destroy()
            self.add_data_button.destroy
            self.train_button.destroy()
           
            self._settings_(NONE)

         # view data vars
        self.data_table = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        self.tags_table = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5 )
        
        self.table_label = Label(self.window, text="Live Preview", font= FONT)
        self.table_ = Text(self.window,width = 20, bg = BG_COLOR,
                                fg = TEXT_COLOR, font = FONT, padx = 5, pady = 5, state="disabled")
        
        
        # add data vars
        self.add_tag_label = Label(self.window, text="Enter Tag", font= FONT_BOLD)
        self.add_tag_text = Text(self.window, bg = BG_COLOR, fg=TEXT_COLOR, 
                                font= FONT, padx=5,pady=5)
        self.view_tags_button = Button(self.window, text = "View Tags", font=FONT, command= lambda : view_tags())
        self.check_tag_button = Button(self.window, text="Check Tag", font=FONT, command=lambda:check_tag())
        
        
        self.add_pattern_label = Label(self.window, text="Enter Pattern", font= FONT_BOLD)        
        self.add_patterns_text = Text(self.window, bg=BG_COLOR, fg = TEXT_COLOR, font="Calibri 20", 
                                      padx=5, pady=5, state="disabled")
        self.add_pattern_button = Button(self.window, text = "Add", font= FONT, command=lambda:add_pattern(), state="disabled")
        
        self.add_response_label = Label(self.window, text="Enter Response", font= FONT_BOLD)        
        self.add_response_button = Button(self.window, text = "Add", font= FONT, command=lambda:add_response(), state="disabled")
        self.add_response_text = Text(self.window, bg=BG_COLOR, fg = TEXT_COLOR, font="Calibri 20", 
                                      padx=5, pady=5, state="disabled")
        
        
        # reset button
        self.reset_button = Button(self.window, text= "Reset", font=FONT, command=lambda: reset())
        # save button
        self.save_data_button = Button(self.window, text= "Save", font=FONT, command=lambda: save_data(), state="disabled")
    
        
        # setup            
        self.start_button.destroy()
        self.blip.destroy()
        self.indic.destroy()
        self.text_widget.destroy()
        self.settings_button.destroy()
        self.head_title.configure(text="Settings")
        self.window.configure(bg = SETTING_BG)
        
        # button declration
        self.delete_data_button = Button(self.window, text = "Delete Data", font=FONT_BOLD , command= lambda : delete_data())
        self.add_data_button = Button(self.window, text = "Add Data", font=FONT_BOLD , command= lambda : add_data())
        self.view_data_button = Button(self.window, text = "View Data", font=FONT_BOLD , command= lambda : view_data())
         
        self.train_button = Button(self.window, text="Train Bot", font=FONT_BOLD, command= lambda: training())
        
       
        
        self.delete_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.1)            
        self.add_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.2)
        self.view_data_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.3)
        self.train_button.place(relwidth=0.15, relheight=0.05, relx=0.01, rely=0.4)
        
        
      
        
        # back button
        self.back_button = Button(self.window, text= "<<",font= "Calibri 20", command= lambda: back_to_main_page(), borderwidth=0)
        self.back_button.place(relx=0.001, rely=0.007, relheight=0.055, relwidth=0.04)
        self.window.update()

        
        
    def running_state(self):
        run = True
        # stop automatically if user daid nothing two times
        err_count = 0
        
        while run and err_count < 2:
            
            self.indic.configure(text="  Listening..")
            self.blip.configure(bg = "#00FF00")
            self.window.update()
            
            msg , key, sender = recognizer()
            
            self.indic.configure(text="     Processing")
            self.blip.configure(bg = "#0000FF")
            self.window.update()
            
            
            if key == 'm':
                self.text_widget.config(fg= ERR_COLOR)
                self._insert_message("MICROPHONE ERROR :(", sender)
                self.text_widget.update()
                self.text_widget.config(fg=TEXT_COLOR)
                
                talk(msg)
                run = False
            elif key == 'e':
                self._insert_message("SERVER ERROR/NO INTERNET CONNECTION :(", sender)
                self.text_widget.update()
                talk(msg)
                run = False
            elif key == 'a':
                self._insert_message("Could not understand :(", sender)
                self.text_widget.update()
                err_count+=1
                talk(msg)
                continue
            else:
                self._insert_message(msg, sender)
                self.text_widget.update()
            
                err_count = 0 # error count reset
                if msg in quit_txt:
                    self._insert_message("See ya later :)",bot_name)
                    self.text_widget.update()
                    talk("see ya later")
                    self.text_widget.config(state="normal")
                    self.text_widget.delete('1.0',END)
                    self.text_widget.update()
                    self.text_widget.config(state="disabled")
                    run = False
                elif msg in fun_txt:
                    fun_mode()
                    self._insert_message(reply,bot_name)
                    self.text_widget.update()
                    talk(reply)
                else:
                    reply = normal_mode(msg)
                    self._insert_message(reply,bot_name)
                    self.text_widget.update()
                    talk(reply)    
         
         

        self.settings_button.configure(state="normal")  
        self.indic.configure(text="Stopped")
        self.blip.configure(bg = "#FF0000")
        self.window.update()
        
        return
    
    
    def _on_enter_pressed(self,event):
        
        self.settings_button.configure(state= "disabled")
        
        self.start_button.configure(text= "Running", state = "disabled")
        
        self.indic.configure(text="Running")
        self.blip.configure(bg = "#00FF00")
        
        self._insert_message("Hello, Welcome to The Global College, How may I help you ?", bot_name)
        self.window.update()

        talk("Hello, Welcome to The Global College, How may I help you")
        
        self.running_state()
        
        self.start_button.config(text="Start", state = "normal")
        self.window.update()
        
        return
        
        
    # insert message
    def _insert_message(self, msg,sender):
        if not msg :
            return
        msg = f"{sender}: {msg}\n\n"
        
        # change text widget state to normal for a moment
        # this may have nothing to do as we are not using mouse so will refractor it
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", msg)
        self.text_widget.config(state="disabled")

        # always see end
        self.text_widget.see(END)
  
         
if __name__ == "__main__":
    app = Application()
    app.window.mainloop()

