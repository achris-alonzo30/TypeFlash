import string
import sys
import time
import styles
from tkinter import *
from wonderwords import RandomSentence


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("Speed Typing App")
        # ------------------------------------------------------------------------------------------------------------ #
        self.images = {}

        # ------------------------------------------------------------------------------------------------------------ #
        # Canvas 2 Variables
        self.random_sentence = RandomSentence()
        self.expected_chars = []
        self.actual_chars = []
        self.answer = None
        self.char_count = 0
        self.error_count = 0
        self.remaining_time = 0

        # Labels
        self.description_label = None
        self.difficulty_var = None
        self.sentence_label = None
        self.timer_label = None
        self.cpm_label = None
        self.wpm_label = None

        # Buttons
        self.start_time = None
        self.restart_button_main = None
        self.resume_button = None
        self.pause_button = None
        # ------------------------------------------------------------------------------------------------------------ #
        # Canvas 3 Variables
        self.time_taken = None
        self.wpm_score = None
        self.cpm_score = None
        self.accuracy_score = None
        self.error_rate = None
        self.play_again_button = None
        self.quit_button = None

        # ------------------------------------------------------------------------------------------------------------ #
        # Calculate the screen width and height of user screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 600
        window_height = 600

        # Calculate the x and y coordinates for centering the main window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window geometry to center it on the screen
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # User prompt canvas
        self.canvas_1 = Canvas(self.root,
                               width = window_width,
                               height = window_height,
                               bg = styles.main_color)

        # Main app canvas
        self.canvas_2 = Canvas(self.root, width = window_width, height = window_height, bg = styles.main_color)

        # Results canvas
        self.canvas_3 = Canvas(self.root, width = window_width, height = window_height, bg = styles.main_color)

        self.current_canvas = self.canvas_1
        self.load_images()
        self.create_canvas_1_elements()
        self.placeholder_active = True
        self.timer_running = False

        self.duration = 0

        self.canvas_1.pack()
        self.canvas_2.pack()
        self.canvas_3.pack()

        self.root.mainloop()
        # ------------------------------------------------------------------------------------------------------------ #

    def load_images(self):
        image_files = {
            "app_name": "images/app_name.png",
            "board": "images/typing_frame.png",
            "difficulty_label": "images/difficulty.png",
            "exit": "images/exit.png",
            "pause": "images/pause.png",
            "play_button": "images/play.png",
            "quit_button": "images/quit.png",
            "restart_main": "images/restart_main.png",
            "play_again": "images/play_again.png",
            "resume": "images/resume.png",
            "scoreboard": "images/scoreboard.png",
            "screen": "images/screen_frame.png",
            "top_board": "images/top_board_frame.png",
            "quit":  "images/quit.png",
        }

        for name, file in image_files.items():
            self.images[name] = PhotoImage(file = file)

    # ---------------------------------------------------------------------------------------------------------------- #
    # Canvas 1 elements
    def create_canvas_1_elements(self):
        app_name_img = self.images["app_name"]
        self.canvas_1.create_image(300, 100, anchor = 'center', image = app_name_img)

        difficulty_label_img = self.images["difficulty_label"]
        self.canvas_1.create_image(300, 250, anchor = 'center', image = difficulty_label_img)

        self.difficulty_var = StringVar()
        self.difficulty_var.set("Easy")  # Set the default difficulty

        # Create Radiobuttons for difficulty options
        easy_button = Radiobutton(self.canvas_1,
                                  text = "EASY",
                                  variable = self.difficulty_var,
                                  value = "Easy",
                                  font = ("Helvetica", 20, "bold"),
                                  fg = styles.font_color, )
        medium_button = Radiobutton(self.canvas_1,
                                    text = "MEDIUM",
                                    variable = self.difficulty_var,
                                    value = "Medium",
                                    font = ("Helvetica", 20, "bold"),
                                    fg = styles.font_color, )
        hard_button = Radiobutton(self.canvas_1,
                                  text = "HARD",
                                  variable = self.difficulty_var,
                                  value = "Hard",
                                  font = ("Helvetica", 20, "bold"),
                                  fg = styles.font_color, )

        # Configure Radiobuttons appearance
        for button in (easy_button, medium_button, hard_button):
            button.config(bg = styles.main_color, fg = styles.font_color, padx = 5, pady = 5)

        # Place Radiobuttons
        easy_button.place(x = 145, y = 300)
        medium_button.place(x = 245, y = 300)
        hard_button.place(x = 370, y = 300)

        play_button_img = self.images["play_button"]
        play_button = self.canvas_1.create_image(300, 400, anchor = 'center', image = play_button_img)
        self.canvas_1.tag_bind(play_button, "<Button-1>", lambda event: self.switch_to_canvas_2())

        quit_button_img = self.images["quit_button"]
        quit_button = self.canvas_1.create_image(300, 500, anchor = 'center', image = quit_button_img)
        self.canvas_1.tag_bind(quit_button, "<Button-1>", lambda event: sys.exit())

    # ---------------------------------------------------------------------------------------------------------------- #
    # Canvas 2 elements

    def switch_to_canvas_2(self):
        self.canvas_1.pack_forget()  # Hide the current canvas

        if self.difficulty_var.get() == "Easy":
            self.duration = 60
        elif self.difficulty_var.get() == "Medium":
            self.duration = 180
        else:
            self.duration = 300

        self.current_canvas = self.canvas_2
        self.create_canvas_2_elements()
        self.generate_sentence()
        self.canvas_2.pack()

    def create_canvas_2_elements(self):
        top_board_img = self.images["top_board"]
        self.canvas_2.create_image(300, 100, anchor = 'center', image = top_board_img)

        # Timer Label
        self.timer_label = self.canvas_2.create_text(160, 100,
                                                     text = "00:00",
                                                     font = ("Courier", 40),
                                                     fill = "black")

        # CPM Label
        self.cpm_label = self.canvas_2.create_text(300, 100,
                                                   text = "?",
                                                   font = ("Courier", 40),
                                                   fill = "black")

        # WPM Label
        self.wpm_label = self.canvas_2.create_text(440, 100,
                                                   text = "?",
                                                   font = ("Courier", 40),
                                                   fill = "black")

        # ------------------------------------------------------------------------------------------------------------ #

        screen_img = self.images["screen"]
        self.canvas_2.create_image(300, 275, anchor = 'center', image = screen_img)

        self.sentence_label = self.canvas_2.create_text(300, 265,
                                                        text = "",
                                                        font = ("Courier", 17, 'italic'),
                                                        fill = 'black')
        # ------------------------------------------------------------------------------------------------------------ #

        board_img = self.images["board"]
        self.canvas_2.create_image(300, 425, anchor = 'center', image = board_img)

        self.answer = Text(self.canvas_2,
                           width = 23, height = 3,
                           font = ("Courier", 15, 'bold'),
                           wrap = WORD,
                           bg = styles.main_color,
                           fg = styles.font_color,
                           highlightthickness = 0,
                           borderwidth = 0)
        self.answer.tag_configure("center", justify = "center")
        self.answer.place(x = 300, y = 420, anchor = "center")
        self.set_placeholder_text("START TYPING HERE")
        self.answer.bind('<KeyRelease>', self.handle_key_event)

        # ------------------------------------------------------------------------------------------------------------ #
        restart_main_img = self.images["restart_main"]
        restart_main_label = Label(self.canvas_2, image = restart_main_img)
        restart_main_label.image = restart_main_img  # Keep a reference to the image
        restart_button = self.canvas_2.create_image(500, 535, anchor = "center", image = restart_main_label.image)
        self.canvas_2.tag_bind(restart_button, "<Button-1>", lambda event: self.update_items())

        restart_description = "RESTART"  # Description for restart button

        # Event handling for hover-in and hover-out
        self.canvas_2.tag_bind(restart_button, "<Enter>",
                               lambda event, desc=restart_description: self.show_description(event, desc))
        self.canvas_2.tag_bind(restart_button, "<Leave>", lambda event: self.hide_description())

        resume_img = self.images["resume"]
        resume_label = Label(self.canvas_2, image = resume_img)
        resume_label.image = resume_img  # Keep a reference to the image
        resume_button = self.canvas_2.create_image(300, 535, anchor = 'center', image = resume_label.image)
        self.canvas_2.tag_bind(resume_button, "<Button-1>", lambda event: self.resume())

        resume_description = "RESUME"  # Description for restart button

        # Event handling for hover-in and hover-out
        self.canvas_2.tag_bind(resume_button, "<Enter>",
                               lambda event, desc=resume_description: self.show_description(event, desc))
        self.canvas_2.tag_bind(resume_button, "<Leave>", lambda event: self.hide_description())

        pause_img = self.images["pause"]
        pause_label = Label(self.canvas_2, image = pause_img)
        pause_label.image = pause_img  # Keep a reference to the image
        pause_button = self.canvas_2.create_image(100, 535, anchor = 'center', image = pause_label.image)
        self.canvas_2.tag_bind(pause_button, "<Button-1>", lambda event: self.pause_timer())

        pause_description = "RESTART"  # Description for restart button

        # Event handling for hover-in and hover-out
        self.canvas_2.tag_bind(pause_button, "<Enter>",
                               lambda event, desc=pause_description: self.show_description(event, desc))
        self.canvas_2.tag_bind(pause_button, "<Leave>", lambda event: self.hide_description())

        self.restart_button_main = restart_main_label  # Update the start_button variable
        self.resume_button = resume_label  # Update the resume_button variable
        self.pause_button = pause_label  # Update the pause_button variable

    def show_description(self, event, description):
        # Create a label or tooltip to display the description
        self.description_label = Label(self.canvas_2,
                                       text = description,
                                       font = ("Courier", 20, 'bold'),
                                       bg = styles.main_color,
                                       fg = styles.font_color,
                                       relief = 'solid')
        # Adjust the position of the label as per your requirement
        self.description_label.place(x = event.x, y = 500)

    def hide_description(self):
        if self.description_label is not None:
            self.description_label.destroy()
            self.description_label = None

    def set_placeholder_text(self, text):
        self.answer.insert("1.0", text)
        self.answer.tag_add("center", "1.0", "end")
        self.answer.tag_config("center",
                               justify = "center",
                               font = ("Courier", 15, 'bold'),
                               foreground = styles.font_color)

    def update_items(self):
        # Update the placeholder text, timer, CPM, and WPM label
        self.placeholder_active = True
        self.timer_running = False
        self.answer.delete("1.0", "end-1c")
        self.set_placeholder_text("START TYPING HERE")
        self.canvas_2.itemconfig(self.timer_label, text = "00:00")
        self.canvas_2.itemconfig(self.cpm_label, text = "?")
        self.canvas_2.itemconfig(self.wpm_label, text = "?")

        # Then generate another new sentence
        self.generate_sentence()

        # Reset the counts
        self.char_count = 0  # Reset the char_count
        self.error_count = 0  # Reset the error count

        # Empty the variables
        self.expected_chars = []
        self.actual_chars = []
        self.remaining_time = 0

    def start_timer(self):
        self.timer_running = True
        self.pause_button.config(state = NORMAL)
        self.restart_button_main.config(state = DISABLED)
        self.resume_button.config(state = DISABLED)
        self.start_time = time.time()  # Initialize the start time
        self.run_timer()

    def stop_timer(self):
        if self.remaining_time <= 0:
            self.update_items()

    def run_timer(self):
        if self.timer_running:
            self.remaining_time = self.duration - int(time.time() - self.start_time)
            self.canvas_2.itemconfig(self.timer_label, text = self.format_time(self.remaining_time))
            self.root.after(1000, self.run_timer)
        else:
            self.stop_timer()

    def pause_timer(self):
        self.timer_running = False
        self.restart_button_main.config(state = NORMAL)
        self.resume_button.config(state = NORMAL)
        self.pause_button.config(state = DISABLED)

    def resume(self):
        self.timer_running = True
        self.start_time = time.time() - (self.duration - self.remaining_time)
        self.run_timer()

    def generate_sentence(self):
        random_sentence = self.random_sentence.sentence()
        random_sentence = random_sentence.rstrip(".")  # Remove the period at the end of the sentence
        self.canvas_2.itemconfig(self.sentence_label, text = random_sentence)

    def start_typing(self, event):
        if self.placeholder_active:
            # If the placeholder is active, clear the answer field
            self.answer.delete("1.0", "end-1c")
            self.placeholder_active = False
            self.start_timer()  # Start the timer

        if self.remaining_time > 0:
            # Check if there is remaining time
            self.actual_chars = self.answer.get("1.0", "end-1c")
            self.expected_chars = self.canvas_2.itemcget(self.sentence_label, "text")

            if event.keysym == "Return":
                # Count the number of printable characters typed correctly
                current_char_count = sum(
                    1 for a, e in zip(self.actual_chars, self.expected_chars) if a == e and a in string.printable)

                # Count the number of printable error characters
                current_error_count = sum(
                    1 for a, e in zip(self.actual_chars, self.expected_chars) if a != e and a in string.printable)

                # Get the remaining expected characters (excluding spaces)
                remaining_expected_chars = [e for e in self.expected_chars if e != ' ']

                # Count the remaining error characters including spaces
                remaining_error_count = len(remaining_expected_chars) - current_char_count + self.expected_chars.count(
                    ' ')

                self.char_count += current_char_count
                self.error_count += current_error_count + remaining_error_count

                print(current_char_count)

                self.generate_sentence()
                self.answer.delete("1.0", "end-1c")  # Delete the text

                print(self.char_count, self.error_count)

                # Calculate the current CPM and WPM
                cpm = (self.char_count / self.duration) * 60
                wpm = cpm / 5

                self.canvas_2.itemconfig(self.cpm_label, text = round(cpm, 2))
                self.canvas_2.itemconfig(self.wpm_label, text = round(wpm, 2))

        if self.remaining_time == 0:
            self.canvas_2.pack_forget()  # Hide the current canvas

            self.current_canvas = self.canvas_3

            # Calculate CPM, WPM, and User Accuracy
            final_cpm = (self.char_count / (self.duration / 60))
            final_wpm = (final_cpm / 5) / (self.duration / 60)
            accuracy = (self.char_count / (self.char_count + self.error_count)) * 100
            # accuracy_per_minute = self.accuracy / (self.duration / 60)

            self.create_canvas_3_elements(final_cpm, final_wpm, accuracy)
            self.canvas_3.pack()

    # Key event handling function
    def handle_key_event(self, event):
        # Check for specific keys and exclude them from triggering the check_typing method
        excluded_keys = ['Shift_L', 'Shift_R', 'space', 'Delete', 'BackSpace']
        if event.keysym not in excluded_keys:
            self.start_typing(event)

    @staticmethod
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    # ---------------------------------------------------------------------------------------------------------------- #
    # Canvas 3 elements
    def create_canvas_3_elements(self, cpm, wpm, accuracy):

        scoreboard_img = self.images["scoreboard"]
        self.canvas_3.create_image(300, 275, anchor = 'center', image = scoreboard_img)

        # Timer Label
        self.time_taken = self.canvas_3.create_text(375, 170,
                                                    text = self.format_time(self.duration),
                                                    font = ("Courier", 20),
                                                    fill = "black")

        # CPM Label
        self.cpm_score = self.canvas_3.create_text(375, 220,
                                                   text = cpm,
                                                   font = ("Courier", 20),
                                                   fill = "black")

        # WPM Label
        self.wpm_score = self.canvas_3.create_text(375, 270,
                                                   text = wpm,
                                                   font = ("Courier", 20),
                                                   fill = "black")

        # Accuracy Label
        self.accuracy_score = self.canvas_3.create_text(375, 320,
                                                        text = f"{round(accuracy, 2)}%",
                                                        font = ("Courier", 20),
                                                        fill = "black")

        # Error Rate
        self.error_rate = self.canvas_3.create_text(375, 370,
                                                    text = self.error_count,
                                                    font = ("Courier", 20),
                                                    fill = "black")
        # ------------------------------------------------------------------------------------------------------------ #

        play_again_img = self.images["play_again"]
        play_again_label = Label(self.canvas_3, image = play_again_img)
        play_again_label.image = play_again_img  # Keep a reference to the image
        play_again_button = self.canvas_3.create_image(500, 530, anchor = "center", image = play_again_label.image)
        self.canvas_3.tag_bind(play_again_button, "<Button-1>", lambda event: self.switch_to_canvas_1())

        quit_img = self.images["quit"]
        quit_label = Label(self.canvas_3, image = quit_img)
        quit_label.image = quit_img  # Keep a reference to the image
        quit_button = self.canvas_3.create_image(100, 530, anchor = 'center', image = quit_label.image)
        self.canvas_3.tag_bind(quit_button, "<Button-1>", lambda event: sys.exit())

        self.play_again_button = play_again_label
        self.quit_button = quit_label

    def switch_to_canvas_1(self):
        self.canvas_3.pack_forget()  # Hide the current canvas (canvas_3)
        self.current_canvas = self.canvas_1  # Set current_canvas to canvas_1
        self.update_items()
        self.create_canvas_1_elements()  # Recreate canvas_1 elements
        self.canvas_1.pack()  # Display canvas_1

    # ---------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    Application()
