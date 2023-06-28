from customtkinter import *
from CTkMessagebox import CTkMessagebox
from datetime import datetime

# global variables
font_title = ('times', 20, 'bold')
font_body = ('times', 16, 'normal')
placeholder_str = "Start typing when you're ready:"
TIME = 5
set_appearance_mode('light')


# --------------------- FRAME CLASS with all needed functions -------------------------
# frame instead of window to start over more easily after 1st time
class FastWriting(CTkFrame):
    def __init__(self, main_win):
        super().__init__(main_win)
        self.main_win = main_win  # master window
        self.timer = None  # to save after_window

        self.label1 = CTkLabel(master=self, font=font_title, text='Write fast!', justify='left')
        self.label1.grid(row=0, pady=(30, 0))

        self.label2 = CTkLabel(master=self, font=font_body, text="After 5 seconds without writing, all is lost")
        self.label2.grid(row=1)

        self.text = CTkTextbox(master=self, width=800, height=400, wrap=WORD)
        self.text.bind('<Button-1>', self.clear_placeholder)
        self.text.bind('<Leave>', self.set_placeholder)
        self.set_placeholder()
        self.text.grid(row=2, pady=20, padx=30)

        self.time = CTkLabel(self, font=font_title)

        self.appearance_mode_label = CTkLabel(master=self, text="Appearance Mode:")
        self.appearance_mode_label.grid(row=4)

    # change appearance mode is possibile with an option menu too
    #     self.appearance_mode_optionsmenu = CTkOptionMenu(self, values=["Light", "Dark"],
    #                                                      command=self.change_appearance_mode_event)
    #     self.appearance_mode_optionsmenu.grid(row=5, padx=20, pady=(10, 10))
    #
    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     set_appearance_mode(new_appearance_mode)

        self.appearance_mode = StringVar(value="Light")
        self.appearance_mode_optionsmenu = CTkSwitch(self, offvalue="Light", onvalue="Dark", textvariable=self.appearance_mode,
                                                     variable=self.appearance_mode, command=self.change_appearance_mode_event)
        self.appearance_mode_optionsmenu.grid(row=5, padx=20, pady=(10, 10))

    def change_appearance_mode_event(self):
        """Switch between light and dark theme (default=light)"""
        set_appearance_mode(self.appearance_mode.get())

    def clear_placeholder(self, event):
        """When user starts typing, clear placeholder and start timer"""
        if self.text.get(1.0, "end-1c") == placeholder_str:
            self.text.delete(1.0, "end-1c")
            self.text.bind('<Key>', self.reset_timer)

    def set_placeholder(self, *args):
        """Tell user what to do to start, setting a placeholder in the textbox"""
        # "end-1c" instead of END, or else I get a single newline character that the text widget always adds
        # 1.0 means line one, character zero
        if self.text.get(1.0, "end-1c") == '':
            self.text.insert("end-1c", placeholder_str)
            self.focus()
            self.text.unbind('<Key>')

    def reset_timer(self, event):
        """When user starts typing or inputs any key, reset the timer"""
        if self.timer:
            self.after_cancel(self.timer)
        self.count_down(TIME)
        self.time.grid(row=3)

    def count_down(self, time):
        """Support function for timer"""
        self.time.configure(text=time)
        if time > 0:
            self.timer = self.after(1000, self.count_down, time - 1)
        else:
            self.finish()

    def finish(self):
        """When time expires, disable typing and show button to close or start a new try"""
        self.text.configure(state='disabled')
        result = self.text.get(1.0, END)
        self.text.delete(1.0, END)
        msg = CTkMessagebox(title="Time expired!", message="Do you want to start over?",
                            icon="question", option_3="Yes", option_2="Yes and save results", option_1="No").get()
        if msg == "No":  # option A: close the program (=master window)
            return self.main_win.destroy()
        if msg == "Yes and save results":  # option B: save results and start over
            curr_time = datetime.now().strftime("%Y%m%d-%H.%M.%S")
            if not os.path.exists("texts"):  # directory must exist, or else file.write gets error
                os.mkdir("texts")
            with open(f"texts/fastwrite_text_{curr_time}.doc", "w", encoding='utf8') as file:  # directory must already exist!
                file.write(result)
        self.destroy()  # option C: start over without saving (=close current frame, open a new one)
        new_frame = FastWriting(self.main_win)
        new_frame.pack()


# --------------------------------- MAIN PROGRAM: create master window and the first frame -----------------------
root = CTk()
root.title("Fast writing app")
# self.geometry("800x600")
# root.config(padx=30, pady=30)
# root.grid_rowconfigure()

frame = FastWriting(root)
frame.pack()

root.mainloop()
