# atlas_module.py – FIXED AND FINAL VERSION
import wx
import random

class AtlasPanel(wx.Panel):
    def __init__(self, parent, countries_file="E:\Python\Python project\country_list.txt"):
        super().__init__(parent)

        self.countries_file = countries_file
        self.countries = []
        self.used_countries = []
        self.current_letter = ""
        self.game_active = False

        self.InitUI()
        self.load_countries()
        self.new_game()

    # ---------------------------------------------------------
    #  UI SETUP
    # ---------------------------------------------------------
    def InitUI(self):
        self.SetBackgroundColour(wx.Colour(25, 5, 35))

        main = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self, label="ATLAS – COUNTRY CHAIN GAME")
        title.SetForegroundColour(wx.Colour(200, 200, 255))
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Rules box
        box = wx.Panel(self)
        box.SetBackgroundColour(wx.Colour(55, 20, 75))
        box_s = wx.BoxSizer(wx.VERTICAL)

        rules = wx.StaticText(box, label=
            "Rules:\n"
            "• Game gives a starting letter\n"
            "• You enter a country with that letter\n"
            "• Bot answers using your last letter\n"
            "• No repeats allowed\n"
            "• Type 'exit' to quit"
        )
        rules.SetForegroundColour(wx.Colour(200, 200, 255))
        rules.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        box_s.Add(rules, 1, wx.ALL, 15)

        box.SetSizer(box_s)
        main.Add(box, 0, wx.EXPAND | wx.ALL, 10)

        # Next Letter Display
        self.letter_display = wx.StaticText(self, label="Next: ?")
        self.letter_display.SetForegroundColour(wx.Colour(0, 255, 255))
        self.letter_display.SetFont(wx.Font(28, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main.Add(self.letter_display, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Status Display (MULTILINE, FIXED OVERLAP)
        self.status_display = wx.StaticText(self, label="", style=wx.ALIGN_LEFT)
        self.status_display.SetForegroundColour(wx.Colour(170, 221, 255))
        self.status_display.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main.Add(self.status_display, 0, wx.EXPAND | wx.ALL, 10)

        # Input row
        row = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label="Your country: ")
        label.SetForegroundColour(wx.Colour(255, 200, 255))
        row.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        self.input_box = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.input_box.Bind(wx.EVT_TEXT_ENTER, self.on_player_turn)
        row.Add(self.input_box, 1, wx.EXPAND)

        main.Add(row, 0, wx.EXPAND | wx.ALL, 10)

        # Used Countries
        used_title = wx.StaticText(self, label="Used Countries:")
        used_title.SetForegroundColour(wx.Colour(255, 200, 0))
        used_title.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main.Add(used_title, 0, wx.LEFT | wx.TOP, 10)

        self.used_list = wx.ListBox(self, size=(-1, 150))
        main.Add(self.used_list, 0, wx.EXPAND | wx.ALL, 10)

        # New game button
        new_btn = wx.Button(self, label="New Game")
        new_btn.Bind(wx.EVT_BUTTON, self.new_game)
        main.Add(new_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main)

    # ---------------------------------------------------------
    #  LOAD & CLEAN COUNTRY DATA
    # ---------------------------------------------------------
    def load_countries(self):
        try:
            with open(self.countries_file, "r", encoding="utf-8") as f:
                self.countries = [
                    c.strip().lower()
                    for c in f.readlines()
                    if c.strip()
                ]
        except:
            wx.MessageBox("country_list.txt missing!", "Error")

    # ---------------------------------------------------------
    #  NEW GAME
    # ---------------------------------------------------------
    def new_game(self, event=None):
        self.used_countries = []
        self.used_list.Clear()
        self.game_active = True
        self.input_box.SetValue("")

        # Generate first letter (avoid X, W)
        letter = random.choice([c for c in "abcdefghijklmnopqrstuvwxyz" if c not in "xw"])

        self.current_letter = letter
        self.letter_display.SetLabel(f"Next: {letter.upper()}")

        self.status_display.SetLabel("Start the game! Enter a country beginning with the letter above.")
        self.status_display.Wrap(400)

    # ---------------------------------------------------------
    #  PLAYER TURN
    # ---------------------------------------------------------
    def on_player_turn(self, event):
        if not self.game_active:
            return

        country = self.input_box.GetValue().strip().lower()
        self.input_box.SetValue("")

        if country == "exit":
            self.end_game("You quit the game.")
            return

        # invalid input
        if (
            not country or
            country not in self.countries or
            country[0] != self.current_letter or
            country in self.used_countries
        ):
            self.end_game("Invalid entry! You lose.")
            return

        # valid player move
        self.used_countries.append(country)
        self.update_used_list()

        last_letter = country[-1]

        # bot move
        bot = self.find_bot_country(last_letter)

        if bot is None:
            self.end_game("Bot cannot answer. YOU WIN!")
            return

        self.used_countries.append(bot)
        self.update_used_list()

        self.current_letter = bot[-1]

        self.letter_display.SetLabel(f"Next: {self.current_letter.upper()}")

        self.status_display.SetLabel(
            f"You: {country.title()}\n"
            f"Bot: {bot.title()}\n"
            f"Your turn → Start with: {self.current_letter.upper()}"
        )
        self.status_display.Wrap(400)

    # ---------------------------------------------------------
    #  BOT SEARCH
    # ---------------------------------------------------------
    def find_bot_country(self, letter):
        for c in self.countries:
            if c.startswith(letter) and c not in self.used_countries:
                return c
        return None

    # ---------------------------------------------------------
    #  UPDATE USED LIST
    # ---------------------------------------------------------
    def update_used_list(self):
        self.used_list.Clear()
        for c in self.used_countries:
            self.used_list.Append(c.title())

    # ---------------------------------------------------------
    #  END GAME
    # ---------------------------------------------------------
    def end_game(self, message):
        self.game_active = False
        self.status_display.SetLabel(message)
        self.status_display.Wrap(400)
        self.letter_display.SetLabel("GAME OVER")
