import wx

class RiddlesPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # ----- State variables -----
        self.level = None
        self.state = "choose_level"
        self.score = 0
        self.total = 0
        self.q_index = 0
        self.waiting_for_hint_answer = False
        self.current_correct_answers = None
        self.current_hint = None

        # ----- QUESTION BANKS -----
        self.questions_easy = [
            ("1. What has keys but can't open locks?", ["keyboard", "piano"]),
            ("2. What has a neck but no head?", ["bottle"]),
            ("3. I fly without wings, I cry without eyes. Whenever I go, darkness flies. What am I?", ["cloud"]),
            ("4. The more you take, the more you leave behind. What am I?", ["footsteps"]),
            ("5. I have a face and two hands but no arms or legs. What am I?", ["clock"]),
            ("6. What has one eye but can't see?", ["needle"]),
            ("7. What goes up but never comes down?", ["age", "height"]),
            ("8. What has to be broken before you can use it?", ["egg"]),
            ("9. Which building has the most stories?", ["library"]),
            ("10. What disappears as soon as you say its name?", ["silence"]),
        ]

        self.questions_medium = [
            ("1. The more of this there is, the less you see. What is it?",
             ["darkness"], "You can hold a lamp to fight me."),
            ("2. I have cities, but no houses... mountains, but no trees...",
             ["map", "maps"], "You often look at me to figure out where you're going."),
            ("3. What is always coming but never arrives?",
             ["tomorrow"], "It is always ahead of you."),
            ("4. I belong to you, but other people use me more often.",
             ["name", "your name"], "You use me when introducing yourself."),
            ("5. Forward I am heavy, but backward I am not.",
             ["ton"], "It is a weight measurement."),
            ("6. What kind of room has no doors or windows?",
             ["mushroom"], "You can eat me."),
            ("7. I have a tongue but cannot talk…",
             ["sole", "sole of shoe"], "Part of your footwear."),
            ("8. What starts with T, ends with T, and has T in it?",
             ["teapot"], "You drink from me."),
            ("9. I am black when clean, white when dirty.",
             ["blackboard"], "Teachers use me."),
            ("10. I stand tall in the morning and disappear at night.",
             ["shadow"], "You see me when the sun is out."),
        ]

        self.questions_hard = [
            ("1. What is always in front of you but can't be seen?",
             ["future", "tomorrow"], "It relates to time."),
            ("2. Taken from a mine, locked in wood, used by all.",
             ["pencil"], "Used for writing."),
            ("3. A boy and doctor fish… doctor not father?",
             ["mother"], "Consider gender."),
            ("4. A 6-letter word: remove 1 and 12 remains.",
             ["dozens"], "Plural of twelve."),
            ("5. You can see me in water but never get wet.",
             ["reflection"], "In a mirror or water."),
            ("6. Two words that hold thousands of letters.",
             ["post office"], "Mail."),
            ("7. Runs but never walks… murmurs but never talks…",
             ["river"], "Flows."),
            ("8. Runs around the yard without moving.",
             ["fence"], "Boundary."),
            ("9. Six faces, 21 eyes, cannot see.",
             ["dice", "die"], "Used in games."),
            ("10. Drop me and I crack; smile and I smile back.",
             ["mirror"], "Reflective object."),
        ]

        # ----- UI COLORS (matched to HangmanPanel) -----
        self.bg_color = wx.Colour(26, 11, 46)          # dark purple
        self.box_color = wx.Colour(40, 20, 80)         # darker contrast purple
        self.text_light = wx.Colour(203, 178, 255)     # soft purple
        self.cyan = wx.Colour(0, 255, 255)             # cyan
        self.gold = wx.Colour(255, 206, 0)             # gold

        self.SetBackgroundColour(self.bg_color)

        # Build UI
        self.build_ui()

        # Show rules initially
        self.append("Rules:\n- Type 'exit' to quit\n- Type easy/medium/hard to select level\nAll the best!\n")

    # ------------------------------------------------------------------
    # UI BUILD
    # ------------------------------------------------------------------
    def build_ui(self):
        main = wx.BoxSizer(wx.VERTICAL)

        # ----- TITLE -----
        title = wx.StaticText(self, label="RIDDLES – BRAIN CHALLENGE")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(self.text_light)
        main.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # ----- RULES BOX -----
        rules_panel = wx.Panel(self)
        rules_panel.SetBackgroundColour(self.box_color)
        rules_sizer = wx.BoxSizer(wx.VERTICAL)

        rules = wx.StaticText(rules_panel,
            label="• Select difficulty level\n• Answer the riddles\n• Medium/Hard allow hints\n• Score: 1 point (no hint), 0.5 (hint)")
        rules.SetForegroundColour(wx.Colour(180, 200, 255))
        rules.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        rules_sizer.Add(rules, 1, wx.ALL | wx.EXPAND, 8)
        rules_panel.SetSizer(rules_sizer)
        main.Add(rules_panel, 0, wx.ALL | wx.EXPAND, 10)

        # ----- OUTPUT BOX -----
        self.output = wx.TextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
        )
        self.output.SetBackgroundColour(wx.Colour(20, 20, 60))
        self.output.SetForegroundColour(wx.Colour(230, 230, 255))
        main.Add(self.output, 1, wx.EXPAND | wx.ALL, 5)

        # ----- INPUT LINE -----
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        prompt = wx.StaticText(self, label="Your answer:")
        prompt.SetForegroundColour(self.text_light)
        hbox.Add(prompt, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        self.input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.input.SetBackgroundColour(wx.Colour(20, 20, 60))
        self.input.SetForegroundColour(wx.Colour(230, 230, 255))
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_submit)
        hbox.Add(self.input, 1, wx.EXPAND | wx.ALL, 5)

        # ----- SUBMIT BUTTON -----
        submit_btn = wx.Button(self, label="Submit")
        submit_btn.SetBackgroundColour(wx.Colour(106, 17, 203))
        submit_btn.SetForegroundColour(wx.WHITE)
        submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        hbox.Add(submit_btn, 0, wx.ALL, 5)

        main.Add(hbox, 0, wx.EXPAND)
        self.SetSizer(main)

        # Offer level options
        self.append("\nSelect difficulty: easy / medium / hard\n")

    # ------------------------------------------------------------------
    def append(self, msg: str):
        self.output.AppendText(msg)

    # ------------------------------------------------------------------
    # INPUT HANDLER
    # ------------------------------------------------------------------
    def on_submit(self, event):
        text = self.input.GetValue().strip()
        if not text:
            return

        self.append(f"\nYou: {text}\n")
        self.input.SetValue("")

        if self.state == "finished":
            self.handle_finished(text)
            return

        if self.state == "choose_level":
            self.handle_level_choice(text)
        elif self.state in ["easy", "medium", "hard"]:
            self.handle_answer(text)
        elif self.state in ["medium_hint", "hard_hint"]:
            self.handle_hint_decision(text)

    # ------------------------------------------------------------------
    # LEVEL SELECTION
    # ------------------------------------------------------------------
    def handle_level_choice(self, text):
        t = text.lower()
        if t in ["easy", "medium", "hard"]:
            self.level = t
            self.state = t
            self.score = self.total = self.q_index = 0
            self.append(f"\nLevel selected: {self.level.upper()}\n")
            self.ask_question()
        else:
            self.append("Please choose: easy / medium / hard\n")

    def get_questions(self):
        return {
            "easy": self.questions_easy,
            "medium": self.questions_medium,
            "hard": self.questions_hard
        }[self.level]

    # ------------------------------------------------------------------
    # ASK NEXT QUESTION
    # ------------------------------------------------------------------
    def ask_question(self):
        questions = self.get_questions()

        if self.q_index >= len(questions):
            self.append(f"\nFinal Score: {self.score} / {self.total}\n")
            self.append("Type 'restart' or 'change'.\n")
            self.state = "finished"
            return

        self.append(f"\n{questions[self.q_index][0]}\n")

    # ------------------------------------------------------------------
    # ANSWER LOGIC
    # ------------------------------------------------------------------
    def handle_answer(self, text):
        if text.lower() == "exit":
            self.append(f"Final Score: {self.score} / {self.total}\n")
            self.state = "finished"
            return

        questions = self.get_questions()

        q = questions[self.q_index]
        if self.level == "easy":
            q_text, ans_list = q
            hint = None
        else:
            q_text, ans_list, hint = q

        self.total += 1
        low = [a.lower() for a in ans_list]

        if text.lower() in low:
            self.append("✔ Correct!\n")
            self.score += 1
            self.q_index += 1
            self.ask_question()
        else:
            if self.level == "easy":
                self.append("✘ Wrong!\nCorrect answer: " + ", ".join(ans_list) + "\n")
                self.q_index += 1
                self.ask_question()
            else:
                self.append("Wrong. Need a hint? (yes/no)\n")
                self.state = self.level + "_hint"
                self.current_correct_answers = ans_list
                self.current_hint = hint

    # ------------------------------------------------------------------
    # HINT LOGIC
    # ------------------------------------------------------------------
    def handle_hint_decision(self, text):
        t = text.lower()

        if not self.waiting_for_hint_answer:
            if t == "yes":
                self.append("Hint: " + self.current_hint + "\nYour answer: ")
                self.waiting_for_hint_answer = True
            elif t == "no":
                self.append("Correct answer: " + ", ".join(self.current_correct_answers) + "\n")
                self.reset_hint_state()
                self.q_index += 1
                self.state = self.level
                self.ask_question()
            else:
                self.append("Please type yes or no.\n")
        else:
            if t in [a.lower() for a in self.current_correct_answers]:
                self.append("✔ Correct (with hint)! +0.5\n")
                self.score += 0.5
            else:
                self.append("✘ Wrong!\nCorrect: " + ", ".join(self.current_correct_answers) + "\n")

            self.reset_hint_state()
            self.q_index += 1
            self.state = self.level
            self.ask_question()

    def reset_hint_state(self):
        self.waiting_for_hint_answer = False
        self.current_correct_answers = None
        self.current_hint = None

    # ------------------------------------------------------------------
    # FINISHED STATE: restart / change
    # ------------------------------------------------------------------
    def handle_finished(self, text):
        t = text.lower()
        if t == "restart":
            self.score = self.total = self.q_index = 0
            self.output.Clear()
            self.append("Restarted!\n")
            self.state = self.level
            self.ask_question()
        elif t == "change":
            self.output.Clear()
            self.state = "choose_level"
            self.append("Select level: easy / medium / hard\n")
       
