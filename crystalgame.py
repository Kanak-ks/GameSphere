import wx
import random


class CrystalPanel(wx.Panel):
    """
    A custom panel that draws the Magic Crystal Ball using GraphicsContext
    for smooth anti-aliased graphics and gradients.
    """
    def __init__(self, parent):
        super().__init__(parent)  # removed fixed size
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.display_text = "???"  # 3 digits
        self.is_glowing = False

        # Colors
        self.bg_color = wx.Colour(26, 11, 46)   # Dark Purple Background
        self.ball_base = wx.Colour(40, 0, 80)   # Deep Indigo
        self.ball_light = wx.Colour(100, 100, 255)  # Light Blue/Purple
        self.text_color = wx.Colour(0, 255, 255)    # Cyan

        # Optional minimum so it doesn't shrink too much
        self.SetMinSize((300, 300))

    def set_text(self, text, glow=False):
        self.display_text = text
        self.is_glowing = glow
        self.Refresh()  # Triggers a redraw

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)

        # Fill background
        dc.SetBackground(wx.Brush(self.bg_color))
        dc.Clear()

        if not gc:
            return

        w, h = self.GetClientSize()
        cx, cy = w / 2, h / 2
        radius = min(w, h) * 0.3

        # 1. Draw Outer Glow (Halo)
        path = gc.CreatePath()
        path.AddCircle(cx, cy, radius + 20)
        brush = gc.CreateRadialGradientBrush(
            cx, cy, cx, cy, radius + 20,
            wx.Colour(100, 50, 200, 100),
            wx.Colour(26, 11, 46, 0)
        )
        gc.SetBrush(brush)
        gc.FillPath(path)

        # 2. Draw Main Crystal Sphere
        path = gc.CreatePath()
        path.AddCircle(cx, cy, radius)

        grad_brush = gc.CreateRadialGradientBrush(
            cx - 30, cy - 30, cx, cy, radius,
            wx.Colour(130, 100, 255, 200),  # Center light
            self.ball_base                  # Edge dark
        )
        gc.SetBrush(grad_brush)
        gc.SetPen(wx.Pen(wx.Colour(200, 200, 255, 100), 1))  # Subtle rim
        gc.FillPath(path)
        gc.StrokePath(path)

        # 3. Draw Shine/Reflection (Top Left)
        path = gc.CreatePath()
        path.AddEllipse(cx - 50, cy - 60, 60, 40)
        shine_brush = gc.CreateLinearGradientBrush(
            cx - 50, cy - 60, cx, cy,
            wx.Colour(255, 255, 255, 150),
            wx.Colour(255, 255, 255, 0)
        )
        gc.SetBrush(shine_brush)
        gc.FillPath(path)

        # 4. Draw The Text inside
        font_size = max(24, int(radius * 0.5))
        font = wx.Font(font_size, wx.FONTFAMILY_TELETYPE,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, self.text_color)

        text_w, text_h = gc.GetTextExtent(self.display_text)

        # Add a glow effect to text if revealed
        if self.is_glowing:
            gc.SetFont(font, wx.Colour(255, 255, 255, 100))  # blur imitation layer
            gc.DrawText(self.display_text, cx - text_w/2 + 2, cy - text_h/2 + 2)
            gc.SetFont(font, self.text_color)

        gc.DrawText(self.display_text, cx - text_w/2, cy - text_h/2)


class CrystalGamePanel(wx.Panel):
    """
    Panel version of the Crystal game to embed inside a wx.Notebook.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.bg_color = wx.Colour(26, 11, 46)
        self.SetBackgroundColour(self.bg_color)

        # Game State
        self.target_number = ""
        self.game_active = False

        self.init_ui()
        self.start_new_game()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self, label="CRYSTAL DIVINATION")
        title_font = wx.Font(16, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(203, 178, 255))
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # The Custom Crystal Drawing Panel
        self.crystal_panel = CrystalPanel(self)
        vbox.Add(self.crystal_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Input Field
        self.input_txt = wx.TextCtrl(
            self,
            style=wx.TE_CENTER | wx.TE_PROCESS_ENTER,
            size=(150, 40)
        )
        self.input_txt.SetFont(wx.Font(
            18, wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        ))
        self.input_txt.SetMaxLength(3)  # Limit input to 3 chars

        # Bind ENTER key to the action
        self.input_txt.Bind(wx.EVT_TEXT_ENTER, self.on_action)
        vbox.Add(self.input_txt, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        # Action Button
        self.action_btn = wx.Button(self, label="GAZE INTO ORB", size=(160, 40))
        self.action_btn.Bind(wx.EVT_BUTTON, self.on_action)
        self.action_btn.SetBackgroundColour(wx.Colour(106, 17, 203))
        self.action_btn.SetForegroundColour(wx.WHITE)
        font_btn = wx.Font(10, wx.FONTFAMILY_SWISS,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.action_btn.SetFont(font_btn)
        vbox.Add(self.action_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        # Score Label
        self.score_lbl = wx.StaticText(self, label="")
        score_font = wx.Font(14, wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.score_lbl.SetFont(score_font)
        self.score_lbl.SetForegroundColour(wx.Colour(255, 206, 0))
        vbox.Add(self.score_lbl, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)

        # Message Label
        self.msg_lbl = wx.StaticText(self, label="Enter 3 digits...")
        self.msg_lbl.SetForegroundColour(wx.Colour(170, 221, 255))
        vbox.Add(self.msg_lbl, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.SetSizer(vbox)

    def start_new_game(self):
        # Generate random number 0-999, pad with zeros (e.g., "052")
        self.target_number = "{:03d}".format(random.randint(0, 999))
        self.game_active = True

        # Reset UI
        self.crystal_panel.set_text("???", glow=False)
        self.input_txt.SetValue("")
        self.input_txt.Enable(True)
        self.input_txt.SetFocus()
        self.action_btn.SetLabel("GAZE INTO ORB")
        self.score_lbl.SetLabel("")
        self.msg_lbl.SetLabel("Enter 3 digits to align fate...")

    def on_action(self, event):
        if not self.game_active:
            self.start_new_game()
            return

        guess = self.input_txt.GetValue()

        # Validation for 3 digits
        if not guess.isdigit() or len(guess) != 3:
            wx.MessageBox(
                "The spirits require exactly 3 digits (0-9).",
                "Invalid Input",
                wx.OK | wx.ICON_WARNING
            )
            return

        # --- SCORING LOGIC FOR 3 DIGITS ---
        total_individual_scores = 0

        for i in range(3):
            t_digit = int(self.target_number[i])
            g_digit = int(guess[i])

            # Calculate difference
            diff = abs(t_digit - g_digit)

            # Formula: (10 - difference) * 10
            digit_score = (10 - diff) * 10

            total_individual_scores += digit_score

        # Total Score = Average of individual digit scores
        score = total_individual_scores / 3

        # Clean up score display (remove decimal if it's a whole number)
        if score.is_integer():
            score_display = int(score)
        else:
            score_display = round(score, 1)

        # Show Results
        self.crystal_panel.set_text(self.target_number, glow=True)
        self.score_lbl.SetLabel(f"Resonance Score: {score_display}%")

        if score == 100:
            self.msg_lbl.SetLabel("PERFECT VISION!")
        elif score >= 80:
            self.msg_lbl.SetLabel("The force is strong.")
        else:
            self.msg_lbl.SetLabel("The crystal remains cloudy.")

        self.game_active = False
        self.action_btn.SetLabel("RESET CRYSTAL")
        self.input_txt.Enable(False)


class MagicGameFrame(wx.Frame):
    """
    Optional standalone window for testing the game alone.
    """
    def __init__(self):
        super().__init__(None, title="Crystal Numerology", size=(400, 600))

        self.bg_color = wx.Colour(26, 11, 46)
        self.SetBackgroundColour(self.bg_color)

        self.target_number = ""
        self.game_active = False

        self.init_ui()
        self.start_new_game()
        self.Center()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="CRYSTAL DIVINATION")
        title_font = wx.Font(16, wx.FONTFAMILY_ROMAN,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(203, 178, 255))
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        self.crystal_panel = CrystalPanel(self)
        vbox.Add(self.crystal_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.input_txt = wx.TextCtrl(
            self, style=wx.TE_CENTER | wx.TE_PROCESS_ENTER, size=(150, 40)
        )
        self.input_txt.SetFont(wx.Font(
            18, wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD
        ))
        self.input_txt.SetMaxLength(3)
        self.input_txt.Bind(wx.EVT_TEXT_ENTER, self.on_action)
        vbox.Add(self.input_txt, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        self.action_btn = wx.Button(self, label="GAZE INTO ORB", size=(160, 40))
        self.action_btn.Bind(wx.EVT_BUTTON, self.on_action)
        self.action_btn.SetBackgroundColour(wx.Colour(106, 17, 203))
        self.action_btn.SetForegroundColour(wx.WHITE)
        font_btn = wx.Font(10, wx.FONTFAMILY_SWISS,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.action_btn.SetFont(font_btn)
        vbox.Add(self.action_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.score_lbl = wx.StaticText(self, label="")
        score_font = wx.Font(14, wx.FONTFAMILY_SWISS,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.score_lbl.SetFont(score_font)
        self.score_lbl.SetForegroundColour(wx.Colour(255, 206, 0))
        vbox.Add(self.score_lbl, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)

        self.msg_lbl = wx.StaticText(self, label="Enter 3 digits...")
        self.msg_lbl.SetForegroundColour(wx.Colour(170, 221, 255))
        vbox.Add(self.msg_lbl, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.SetSizer(vbox)

    def start_new_game(self):
        self.target_number = "{:03d}".format(random.randint(0, 999))
        self.game_active = True

        self.crystal_panel.set_text("???", glow=False)
        self.input_txt.SetValue("")
        self.input_txt.Enable(True)
        self.input_txt.SetFocus()
        self.action_btn.SetLabel("GAZE INTO ORB")
        self.score_lbl.SetLabel("")
        self.msg_lbl.SetLabel("Enter 3 digits to align fate...")

    def on_action(self, event):
        if not self.game_active:
            self.start_new_game()
            return

        guess = self.input_txt.GetValue()

        if not guess.isdigit() or len(guess) != 3:
            wx.MessageBox(
                "The spirits require exactly 3 digits (0-9).",
                "Invalid Input",
                wx.OK | wx.ICON_WARNING
            )
            return

        total_individual_scores = 0

        for i in range(3):
            t_digit = int(self.target_number[i])
            g_digit = int(guess[i])
            diff = abs(t_digit - g_digit)
            digit_score = (10 - diff) * 10
            total_individual_scores += digit_score

        score = total_individual_scores / 3

        if score.is_integer():
            score_display = int(score)
        else:
            score_display = round(score, 1)

        self.crystal_panel.set_text(self.target_number, glow=True)
        self.score_lbl.SetLabel(f"Resonance Score: {score_display}%")

        if score == 100:
            self.msg_lbl.SetLabel("PERFECT VISION!")
        elif score >= 80:
            self.msg_lbl.SetLabel("The force is strong.")
        else:
            self.msg_lbl.SetLabel("The crystal remains cloudy.")

        self.game_active = False
        self.action_btn.SetLabel("RESET CRYSTAL")
        self.input_txt.Enable(False)


if __name__ == "__main__":
    app = wx.App()
    frame = MagicGameFrame()
    frame.Show()
    app.MainLoop()
