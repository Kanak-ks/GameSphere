# word_guessing.py - Final HangmanPanel with Rules Display
import wx
import random


class HangmanPanel(wx.Panel):
    def __init__(self, parent, file_path=r"E:\Python\Python project\words[1].txt"):
        super().__init__(parent)
        self.file_path = file_path
        self.random_word = ""
        self.list_word = []
        self.list_dashes = []
        self.chances = "HANGMAN"  # 7 chances as per rules
        self.list_chances = list(self.chances)
        self.game_active = False
        self.on_win_callback = None
        self.on_lose_callback = None

        # Background colour (dark purple)
        self.bg_color = wx.Colour(26, 11, 46)
        self.SetBackgroundColour(self.bg_color)

        self.init_ui()
        self.new_game()

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self, label="WORD GUESSING – HANGMAN")
        title_font = wx.Font(16, wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(203, 178, 255))  # soft purple
        main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # Rules box with contrasting background
        rules_panel = wx.Panel(self)
        rules_panel.SetBackgroundColour(wx.Colour(40, 20, 80))  # darker purple box
        rules_sizer = wx.BoxSizer(wx.VERTICAL)

        rules_text = (
            "Rules:\n"
            "• Random word shown as dashes ( _ _ _ _ )\n"
            "• 7 chances (H A N G M A N)\n"
            "• Correct guess: letter revealed\n"
            "• Wrong guess: one letter → *\n"
            "• Win: complete word | Lose: all *\n"
            "• Type 'exit' to quit"
        )
        rules = wx.StaticText(rules_panel, label=rules_text)
        rules.SetForegroundColour(wx.Colour(180, 200, 255))  # light bluish text
        rules.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        rules_sizer.Add(rules, 1, wx.ALL | wx.EXPAND, 8)
        rules_panel.SetSizer(rules_sizer)

        main_sizer.Add(rules_panel, 0, wx.ALL | wx.EXPAND, 10)

        # Word display
        self.word_display = wx.StaticText(self, label="", style=wx.ALIGN_CENTER)
        font = wx.Font(28, wx.FONTFAMILY_TELETYPE,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.word_display.SetFont(font)
        self.word_display.SetForegroundColour(wx.Colour(0, 255, 255))  # cyan
        main_sizer.Add(self.word_display, 0, wx.ALL | wx.EXPAND, 10)

        # Hangman chances display
        self.chances_display = wx.StaticText(self, label="H A N G M A N")
        chances_font = wx.Font(18, wx.FONTFAMILY_SWISS,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.chances_display.SetFont(chances_font)
        self.chances_display.SetForegroundColour(wx.Colour(255, 206, 0))  # gold
        main_sizer.Add(self.chances_display, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Status / feedback line
        self.status_display = wx.StaticText(self, label="")
        self.status_display.SetForegroundColour(wx.Colour(170, 221, 255))  # light blue
        self.status_display.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS,
                                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(self.status_display, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # Letter input
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

        prompt = wx.StaticText(self, label="Guess letter or 'exit':")
        prompt.SetForegroundColour(wx.Colour(203, 178, 255))
        input_sizer.Add(prompt, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.letter_input = wx.TextCtrl(
            self, size=(80, -1), style=wx.TE_PROCESS_ENTER
        )
        self.letter_input.Bind(wx.EVT_TEXT_ENTER, self.on_guess)
        # Input colours
        self.letter_input.SetBackgroundColour(wx.Colour(20, 20, 60))
        self.letter_input.SetForegroundColour(wx.Colour(230, 230, 255))
        input_sizer.Add(self.letter_input, 0, wx.ALL, 5)

        main_sizer.Add(input_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.new_btn = wx.Button(self, label="New Game")
        self.new_btn.Bind(wx.EVT_BUTTON, self.new_game)
        # Button colours
        self.new_btn.SetBackgroundColour(wx.Colour(106, 17, 203))   # purple
        self.new_btn.SetForegroundColour(wx.WHITE)
        self.new_btn.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS,
                                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn_sizer.Add(self.new_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 15)

        self.SetSizer(main_sizer)

    def new_game(self, event=None):
        try:
            with open(self.file_path, "r") as file:
                words = file.readlines()
            self.random_word = random.choice(words).strip().upper()
            self.list_word = list(self.random_word)
            self.list_dashes = ['_'] * len(self.list_word)
            self.chances = "HANGMAN"
            self.list_chances = list(self.chances)
            self.game_active = True
            self.letter_input.SetValue("")
            self.status_display.SetLabel("New game started. Good luck!")
            self.update_display()
        except FileNotFoundError:
            wx.MessageBox(
                f"Word file not found: {self.file_path}",
                "Error", wx.OK | wx.ICON_ERROR
            )

    def on_guess(self, event):
        if not self.game_active:
            return

        guess = self.letter_input.GetValue().strip().upper()
        self.letter_input.SetValue("")

        if guess == 'EXIT':
            self.status_display.SetLabel(f"Game quit! Word was: {self.random_word}")
            self.game_active = False
            return

        if len(guess) != 1 or not guess.isalpha():
            self.status_display.SetLabel("Enter a single letter A–Z.")
            return

        if guess in self.list_word:
            for i in range(len(self.list_word)):
                if self.list_word[i] == guess:
                    self.list_dashes[i] = guess
            self.update_display()
            self.status_display.SetLabel(f"Nice! '{guess}' is in the word.")

            if ''.join(self.list_dashes) == self.random_word:
                self.chances_display.SetLabel("🎉 YOU WON! 🎉")
                self.status_display.SetLabel("You guessed the word correctly!")
                self.game_active = False
                if self.on_win_callback:
                    self.on_win_callback()
        else:
            # Replace one letter from HANGMAN with *
            for i in range(len(self.list_chances) - 1, -1, -1):
                if self.list_chances[i] != '*':
                    self.list_chances[i] = '*'
                    break
            self.update_display()
            self.status_display.SetLabel(f"'{guess}' is not in the word.")

            if self.list_chances.count('*') == len(self.list_chances):
                self.word_display.SetLabel(f"{self.random_word}")
                self.chances_display.SetLabel("💀 YOU LOST! 💀")
                self.status_display.SetLabel("No more chances left.")
                self.game_active = False
                if self.on_lose_callback:
                    self.on_lose_callback()

    def update_display(self):
        self.word_display.SetLabel(' '.join(self.list_dashes))
        self.chances_display.SetLabel(' '.join(self.list_chances))

    def set_callbacks(self, on_win=None, on_lose=None):
        self.on_win_callback = on_win
        self.on_lose_callback = on_lose
