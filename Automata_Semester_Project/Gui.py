import tkinter as tk
from PIL import Image, ImageTk
import FA


# class to display main page of the program
class MainWindow(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        # creating a border to the frame
        border = tk.LabelFrame(self, bg="#D8CFF7", bd=20)
        border.pack(fill="both", expand="yes", padx=250, pady=250)

        # Label projectTitle
        projectTitle = tk.Label(self, text="Automata & Computability\nFinal project" ,font=("Helvetica Bold", 50))
        projectTitle.config(fg= "#877796")
        projectTitle.place(x=250, y=50)

        # text field entry to get regex from user
        EnterRegex_Label = tk.Label(border, text="Enter the Regular Expression to be Converted:",
                                  font=("Courier Bold", 18),
                                  bg="#D8CFF7", fg= "#877796")
        EnterRegex_Label.place(x=115, y=30)

        regex_textEntry = tk.Entry(border, width=20,  bd=5, font=("Courier", 18))
        regex_textEntry.place(x=210, y=90)

        def generateFA(clicked_button):
            if clicked_button == "NFA":
                NFA_Window.regex = regex_textEntry.get()
                controller.showFrame(NFA_Window)
            elif clicked_button == "DFA":
                DFA_Window.regex = regex_textEntry.get()
                controller.showFrame(DFA_Window)

        # Moving to REGEX 2 NFA window
        Convert2nfa_button = tk.Button(self, text="NFA Converter", font=("Helvetica", 18),
                            command=lambda: generateFA("NFA"), bg="#D8CFF7", bd=5)
        Convert2nfa_button.place(x=550, y=500)




class NFA_Window(tk.Frame):
    regex = ""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

################### title label#############################
        Title = tk.Label(self, text="Regex to NFA", font=("Arial Bold", 20))
        Title.config(fg= "#877796")
        Title.place(x=500, y=30)

#################Convert to NFA btn #######################
        Convert_btn = tk.Button(self, text="Convert to NFA", font=("Helvetica", 18), bg="#D8CFF7", bd=5,
                                command=lambda: self.display_regex_NFA())
        Convert_btn.place(x=400, y=80)

#################Convert to DFA btn #######################
        Convert_btn_DFA = tk.Button(self, text="Convert to DFA", font=("Helvetica", 18), bg="#D8CFF7", bd=5,
                                    command=lambda: self.display_regex_DFA())
        Convert_btn_DFA.place(x=600, y=80)

###################### Solving the Lag of Graphix##################################

        Clear_label = tk.Label(self, text="Clear Page, before Proceeding!", font=("Arial Bold", 15), bg="#D8CFF7")
        Clear_label.place(x=450, y=650)
        clear_btn = tk.Button(self, text="Clear page", font=("Helvetica", 18),
                              command=lambda: self.clear_window(), bg="#D8CFF7", bd=5)
        clear_btn.place(x=1075, y=10)

########################## Button leading to main window ###############################
        HomeWindow_Button = tk.Button(self, text="Home page", font = ("Helvetica", 18),
                               command=lambda: controller.showFrame(MainWindow), bg="#D8CFF7", bd = 5)
        HomeWindow_Button.place(x=50, y=10)



        #Display Regex for NFA
    def display_regex_NFA(self):
        global regexText
        regexText = tk.Label(self, text=self.regex, font=("Arial Bold", 20))
        regexText.place(x=50, y=250)
        regexText.config(fg="#877796")
        self.show_nfa()


    #Display NFA GRAPH
    def show_nfa(self):
        a = FA.Regex2NFA(self.regex)
        a.create_nfa()
        Generated_NFA = Image.open('nfa.gv.png')
        Generated_NFA = ImageTk.PhotoImage(Generated_NFA)

        global nfa_label
        nfa_label = tk.Label(image=Generated_NFA)
        nfa_label.image = Generated_NFA
        nfa_label.place(x=50, y=300)

    def clear_window(self):
        regexText.place_forget()
        nfa_label.place_forget()
        dfa_label.place_forget()

    ###############Display Regex for DFA##############
    def display_regex_DFA(self):
        global regexText
        regexText = tk.Label(self, text=self.regex, font=("Arial Bold", 20))
        regexText.place(x=50, y=250)
        self.show_dfa()

###############Show Created DFA##############
    def show_dfa(self):
        a = FA.Regex2NFA(self.regex)
        b = FA.NFA2DFA(a.nfa)
        b.create_dfa()

        dfa = Image.open('dfa.gv.png')
        dfa = ImageTk.PhotoImage(dfa)
        global dfa_label
        dfa_label = tk.Label(image=dfa)
        dfa_label.image = dfa
        dfa_label.place(x=50, y=300)

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=720)
        window.grid_columnconfigure(0, minsize=1280)
        self.frames = {}
        for f in [MainWindow, NFA_Window]:
            frame = f(window, self)
            self.frames[f] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(MainWindow)

    def showFrame(self, page):
        frame = self.frames[page]
        frame.tkraise() #stack frames on top of each other


if __name__ == '__main__':
    window = Gui()
    window.title("Automata&Computability Final Project")
    window.mainloop()




