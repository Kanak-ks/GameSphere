import csv
import random
import wx


class WordScramblePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(wx.Colour(40, 20, 80))

        self.words_list = []
        self.used_words = []
        self.points = 0
        self.current_word = ""
        self.scrambled_word = ""
        self.attempts_left = 3
        self.level = ""
        self.game_active = False

        self.load_words()
        self.init_ui()

    # ---------- data ----------

    def load_words(self):
        try:
            with open(r"E:\Python\Python project\scramble_words.csv", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)
                self.words_list = list(reader)
        except FileNotFoundError:
            wx.MessageBox("scramble_words.csv file not found!", "Error",
                          wx.OK | wx.ICON_ERROR)

    def get_next_word(self):
        available = [
            row[1].lower()
            for row in self.words_list
            if len(row) >= 2
            and row[0].lower() == self.level
            and row[1].lower() not in self.used_words
        ]
        if not available:
            return None
        w = random.choice(available)
        self.used_words.append(w)
        return w

    # ---------- UI ----------

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # SMALLER TITLE
        title = wx.StaticText(self, label="🧩 Word Scramble", style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.Colour(70, 130, 180))
        main_sizer.Add(title, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 10)

        # SHORTER RULES BOX
        rules_panel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        rules_panel.SetBackgroundColour(wx.Colour(20, 20, 40))
        r_sizer = wx.BoxSizer(wx.VERTICAL)

        rules_text = wx.StaticText(
            rules_panel,
            label=("📋 RULES: Guess the scrambled word in 3 tries.\n"
                   "Easy: 5 pts | Medium: 10 pts | Hard: 15 pts."),
            style=wx.ALIGN_LEFT
        )
        rules_text.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        rules_text.SetForegroundColour(wx.Colour(255, 255, 255))
        r_sizer.Add(rules_text, 1, wx.ALL | wx.EXPAND, 5)
        rules_panel.SetSizer(r_sizer)
        main_sizer.Add(rules_panel, 0, wx.ALL | wx.EXPAND, 5)

        # COMPACT LEVEL ROW
        lvl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl_lbl = wx.StaticText(self, label="🎯 Level:")
        lvl_lbl.SetForegroundColour(wx.Colour(255, 255, 255))
        lvl_sizer.Add(lvl_lbl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.level_combo = wx.ComboBox(
            self, choices=["Easy", "Medium", "Hard"],
            style=wx.CB_READONLY, size=(100, -1)
        )
        self.level_combo.SetSelection(0)
        lvl_sizer.Add(self.level_combo, 0, wx.ALL, 5)

        self.start_btn = wx.Button(self, label="Start", size=(80, 30))
        self.start_btn.Bind(wx.EVT_BUTTON, self.start_game)
        lvl_sizer.Add(self.start_btn, 0, wx.ALL, 5)

        main_sizer.Add(lvl_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # SMALLER GAME PANEL
        game_panel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        game_panel.SetBackgroundColour(wx.Colour(40, 20, 80))
        g_sizer = wx.BoxSizer(wx.VERTICAL)

        self.word_display = wx.StaticText(
            game_panel, label="Click START to begin!", style=wx.ALIGN_CENTER
        )
        self.word_display.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.word_display.SetForegroundColour(wx.Colour(255, 100, 100))
        g_sizer.Add(self.word_display, 0, wx.ALL | wx.EXPAND, 5)

        sc_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.score_label = wx.StaticText(game_panel, label="Score: 0",
                                         style=wx.ALIGN_CENTER)
        self.score_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.score_label.SetForegroundColour(wx.Colour(0, 180, 0))
        sc_sizer.Add(self.score_label, 1, wx.ALL | wx.ALIGN_CENTER, 5)

        self.attempts_label = wx.StaticText(game_panel, label="Attempts: 3",
                                            style=wx.ALIGN_CENTER)
        self.attempts_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.attempts_label.SetForegroundColour(wx.Colour(255, 140, 0))
        sc_sizer.Add(self.attempts_label, 1, wx.ALL | wx.ALIGN_CENTER, 5)

        g_sizer.Add(sc_sizer, 0, wx.EXPAND, 5)

        self.next_btn = wx.Button(game_panel, label="Next", size=(70, 28))
        self.next_btn.Bind(wx.EVT_BUTTON, self.next_word)
        self.next_btn.Enable(False)
        g_sizer.Add(self.next_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        game_panel.SetSizer(g_sizer)
        main_sizer.Add(game_panel, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        # BIG INPUT ROW
        in_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.guess_input = wx.TextCtrl(
            self,
            style=wx.TE_CENTER | wx.TE_PROCESS_ENTER | wx.TE_MULTILINE,
        )
        self.guess_input.SetMinSize((400, 120))
        self.guess_input.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.guess_input.Enable(False)
        self.guess_input.Bind(wx.EVT_TEXT_ENTER, self.on_guess)
        in_sizer.Add(self.guess_input, 1, wx.ALL | wx.EXPAND, 5)

        self.submit_btn = wx.Button(self, label="OK", size=(70, 35))
        self.submit_btn.Bind(wx.EVT_BUTTON, self.on_guess)
        self.submit_btn.Enable(False)
        in_sizer.Add(self.submit_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        main_sizer.Add(in_sizer, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        # STATUS
        self.status_label = wx.StaticText(self, label="Select level & click Start",
                                          style=wx.ALIGN_CENTER)
        self.status_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.status_label.SetForegroundColour(wx.Colour(0, 150, 200))
        main_sizer.Add(self.status_label, 0, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(main_sizer)

    # ---------- game logic ----------

    def start_game(self, event):
        self.level = self.level_combo.GetValue().lower()
        self.used_words = []
        self.points = 0
        self.game_active = True
        self.attempts_left = 3
        self.update_score_display()

        self.start_btn.Enable(False)
        self.level_combo.Enable(False)

        self.guess_input.Enable(True)
        self.submit_btn.Enable(True)
        self.guess_input.SetValue("")
        self.guess_input.SetFocus()

        self.status_label.SetLabel("💡 Make your guess!")
        self.next_word()

    def next_word(self, event=None):
        if not self.game_active:
            return

        word = self.get_next_word()
        if word is None:
            self.end_game()
            return

        self.current_word = word
        self.scrambled_word = "".join(random.sample(word, len(word)))
        for _ in range(10):
            if self.scrambled_word != word:
                break
            self.scrambled_word = "".join(random.sample(word, len(word)))

        self.word_display.SetLabel(f"{self.scrambled_word.upper()}")
        self.attempts_left = 3
        self.update_score_display()

        self.status_label.SetLabel("💡 Make your guess!")
        self.status_label.SetForegroundColour(wx.Colour(0, 100, 200))

        self.guess_input.Enable(True)
        self.submit_btn.Enable(True)
        self.guess_input.SetValue("")
        self.guess_input.SetFocus()
        self.next_btn.Enable(False)

    def on_guess(self, event):
        if not self.game_active:
            return

        guess = self.guess_input.GetValue().lower().strip()
        if guess == "exit":
            self.end_game()
            return

        if guess == self.current_word:
            pts = {"easy": 5, "medium": 10, "hard": 15}
            self.points += pts.get(self.level, 0)
            self.status_label.SetLabel("Correct!")
            self.status_label.SetForegroundColour(wx.Colour(0, 200, 0))
            self.update_score_display()

            self.guess_input.Enable(False)
            self.submit_btn.Enable(False)
            self.next_btn.Enable(True)
        else:
            self.attempts_left -= 1
            self.update_score_display()
            if self.attempts_left <= 0:
                self.status_label.SetLabel(
                    f"Out of attempts. Word: {self.current_word}"
                )
                # WHITE TEXT for out-of-attempts
                self.status_label.SetForegroundColour(wx.Colour(255, 255, 255))
                self.guess_input.Enable(False)
                self.submit_btn.Enable(False)
                self.next_btn.Enable(True)
            else:
                self.status_label.SetLabel(
                    f"Wrong! {self.attempts_left} left"
                )
                self.status_label.SetForegroundColour(wx.Colour(255, 140, 0))

    def update_score_display(self):
        self.score_label.SetLabel(f"Score: {self.points}")
        self.attempts_label.SetLabel(f"Attempts: {self.attempts_left}")

    def end_game(self):
        self.game_active = False
        dlg = wx.MessageDialog(
            self,
            f"Level {self.level.title()} complete.\nScore: {self.points}",
            "Game Over",
            wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()

        self.points = 0
        self.used_words = []
        self.current_word = ""
        self.scrambled_word = ""
        self.attempts_left = 3
        self.update_score_display()

        self.word_display.SetLabel("Click START to begin!")
        self.status_label.SetLabel("Select level & click Start")
        self.status_label.SetForegroundColour(wx.Colour(0, 150, 200))

        self.guess_input.Enable(False)
        self.submit_btn.Enable(False)
        self.next_btn.Enable(False)
        self.start_btn.Enable(True)
        self.level_combo.Enable(True)
