import wx
import os

from quiz_module import Game1Panel
from riddle_module import RiddlesPanel
from word_guessing import HangmanPanel
from atlas_module import AtlasPanel
from crystalgame import CrystalGamePanel
from scramble import WordScramblePanel

# ================= THEME =================
BG = wx.Colour(10, 10, 20)
CARD = wx.Colour(20, 20, 40)
NEON = wx.Colour(170, 120, 255)
NEON_HOVER = wx.Colour(200, 160, 255)
TEXT = wx.Colour(220, 220, 255)

ASSETS = "assets"


# ================= ACHIEVEMENT POPUP =================
class AchievementPopup(wx.Frame):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            style=wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.STAY_ON_TOP
        )
        self.SetBackgroundColour(wx.Colour(25, 25, 50))
        self.SetSize((320, 90))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(25, 25, 50))

        label = wx.StaticText(panel, label=f"🏆 Achievement Unlocked!\n{text}")
        label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.BOLD))
        label.SetForegroundColour(NEON)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 1, wx.CENTER | wx.ALL, 15)
        panel.SetSizer(sizer)

        screen_w, screen_h = wx.GetDisplaySize()
        self.SetPosition((screen_w - 340, screen_h))

        self.alpha = 0
        self.SetTransparent(self.alpha)
        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.animate)
        self.timer.Start(15)

    def animate(self, event):
        x, y = self.GetPosition()
        if self.alpha < 240:
            self.alpha += 15
            self.SetTransparent(self.alpha)
            self.SetPosition((x, y - 3))
        else:
            self.timer.Stop()
            wx.CallLater(1500, self.Destroy)


# ================= THUMBNAIL TILE =================
class GameTile(wx.Panel):
    def __init__(self, parent, image, label, callback):
        super().__init__(parent, size=(220, 170))
        self.callback = callback
        self.SetBackgroundColour(CARD)

        img = wx.Image(image).Scale(200, 120, wx.IMAGE_QUALITY_HIGH)
        self.bmp = wx.StaticBitmap(self, bitmap=wx.Bitmap(img))

        text = wx.StaticText(self, label=label)
        text.SetForegroundColour(TEXT)
        text.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.BOLD))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.bmp, 0, wx.CENTER | wx.TOP, 5)
        sizer.Add(text, 0, wx.CENTER | wx.TOP, 8)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.bmp.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def on_hover(self, event):
        self.SetBackgroundColour(NEON)
        self.Refresh()

    def on_leave(self, event):
        self.SetBackgroundColour(CARD)
        self.Refresh()

    def on_click(self, event):
        self.callback()


# ================= WELCOME SCREEN =================
class WelcomePanel(wx.Panel):
    def __init__(self, parent, frame):
        super().__init__(parent)
        self.frame = frame
        self.SetBackgroundColour(BG)

        title = wx.StaticText(self, label="⚡ CYBER GAME LAUNCHER ⚡")
        title.SetFont(wx.Font(28, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour(NEON)

        grid = wx.GridSizer(2, 3, 20, 20)

        games = [
            ("quiz.png", "Quiz Game"),
            ("riddles.png", "Riddles"),
            ("hangman.png", "Word Guessing"),
            ("atlas.png", "Atlas"),
            ("crystal.png", "Crystal Game"),
            ("scramble.png", "Scramble Game"),
        ]

        for i, (img, name) in enumerate(games, start=1):
            tile = GameTile(
                self,
                os.path.join(ASSETS, img),
                name,
                lambda n=i: self.frame.show_game(n)
            )
            grid.Add(tile, 0, wx.CENTER)

        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(title, 0, wx.CENTER | wx.ALL, 25)
        main.Add(grid, 0, wx.CENTER | wx.ALL, 20)

        self.SetSizer(main)


# ================= MAIN FRAME =================
class ChatbotFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Cyber Game Launcher", size=(950, 780))
        self.SetBackgroundColour(BG)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG)

        self.notebook = wx.Notebook(self.panel)

        self.notebook.AddPage(Game1Panel(self.notebook), "Quiz")
        self.notebook.AddPage(RiddlesPanel(self.notebook), "Riddles")
        self.notebook.AddPage(HangmanPanel(self.notebook), "Hangman")
        self.notebook.AddPage(AtlasPanel(self.notebook), "Atlas")
        self.notebook.AddPage(CrystalGamePanel(self.notebook), "Crystal")
        self.notebook.AddPage(WordScramblePanel(self.notebook), "Scramble")

        self.welcome = WelcomePanel(self.panel, self)

        self.chat = wx.TextCtrl(
            self.panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE
        )
        self.chat.SetBackgroundColour(wx.Colour(15, 15, 30))
        self.chat.SetForegroundColour(TEXT)
        self.chat.AppendText("🤖 Bot: Welcome to Cyber Game Launcher!\n\n")

        self.input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_send)

        send = wx.Button(self.panel, label="Send")
        send.SetBackgroundColour(NEON)
        send.SetForegroundColour(wx.BLACK)
        send.Bind(wx.EVT_BUTTON, self.on_send)

        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer.Add(self.input, 1, wx.EXPAND | wx.ALL, 6)
        input_sizer.Add(send, 0, wx.ALL, 6)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.welcome, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.notebook, 2, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.chat, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(sizer)
        self.notebook.Hide()
        self.Show()

    def fade(self):
        for a in range(255, 180, -15):
            self.SetTransparent(a)
            wx.MilliSleep(12)
        for a in range(180, 255, 15):
            self.SetTransparent(a)
            wx.MilliSleep(12)

    def show_game(self, num):
        self.fade()
        self.welcome.Hide()
        self.notebook.Show()
        self.notebook.SetSelection(num - 1)
        self.panel.Layout()

        self.chat.AppendText(f"🎮 Bot: Game {num} launched!\n\n")
        AchievementPopup(self, "First Game Launched")

    def on_send(self, event):
        msg = self.input.GetValue().strip()
        if msg.lower() == "back":
            self.notebook.Hide()
            self.welcome.Show()
            self.panel.Layout()
            self.chat.AppendText("🤖 Bot: Returned to launcher\n\n")
        elif msg:
            self.chat.AppendText(f"👤 You: {msg}\n🤖 Bot: Keep playing!\n\n")
        self.input.SetValue("")


# ================= RUN =================
if __name__ == "__main__":
    app = wx.App(False)
    ChatbotFrame()
    app.MainLoop()
