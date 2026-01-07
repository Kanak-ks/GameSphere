import wx

class Game1Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set purple themed background
        self.SetBackgroundColour(wx.Colour(25, 5, 35))

        self.topic = None
        self.level = 1
        self.score = 0
        self.score1 = 0
        self.score2 = 0
        self.q_index = 0
        self.state = "choose_topic"
        self.edit_mode = False

        # ---------- COMPLETE QUIZ DATA ----------
        self.quiz_data = {
            "a": {  # General Knowledge
                1: [
                    ("What is the capital of india?", ["delhi"]),
                    ("How many states are there in india?", ["28"]),
                    ("How many uninon territories are there in India?", ["9"]),
                    ("What does www stands for?", ["world wide web"]),
                    ("What is the national game of India?", ["hockey"]),
                ],
                2: [
                    ("Which city in India is known as 'City of Joy'?", ["kolkata"]),
                    ("What is study of fossils called?", ["paleontology"]),
                    ("Which city is known as the Silicon Valley of India?", ["bangalore"]),
                    ("Which country is known as the leading producer of 'tea'?", ["china"]),
                    ("'Madhubani', a Style of folk Paintings, is popular in which state of India?", ["bihar"]),
                ],
                3: [
                    ("Which Indian state has the smallest coastline?", ["goa"]),
                    ("Which city has the title of 'Scotland of the East' in India?", ["shillong"]),
                    ("How many languages does the Indian constitution recognise?", ["22"]),
                    ("Which ancient Indian text is known for its teachings on governance?", ["arthashastra"]),
                    ("How many minutes are there in a week", ["10080"]),
                ],
            },
            "b": {  # Sports Knowledge
                1: [
                    ("Who captained India to its first ever cricket world cup victory?", ["kapil dev"]),
                    ("Who was the first Indian cricketer to score a double century in ODI?", ["sachin tendulkar"]),
                    ("Which Indian chess player holds the title of Grandmaster?", ["vishwanathan anand","vishwanathan"]),
                    ("Which athlete is known as the 'Flying Sikh'?", ["milkha singh","milka singh"]),
                    ("Who is the youngest Indian woman to climb Mount Everest?", ["bachendri pal"]),
                ],
                2: [
                    ("Who is the only Indian male boxer to win an Olympic medal?", ["vijender singh"]),
                    ("Who won India's first Olympic badminton medal?", ["prakash padukone"]),
                    ("Naidu cup is associated with which sport?", ["chess"]),
                    ("Eden Gardens stadium is located in which city?", ["kolkata"]),
                    ("What is the national sport of China?", ["table tennis"]),
                ],
                3: [
                    ("Which sport has stones slid on ice?", ["curling"]),
                    ("India first participated in which Olympics?", ["1920"]),
                    ("Which country has won most cricket world cups?", ["australia"]),
                    ("Where was the first Olympic games held?", ["canada"]),
                    ("Which term is used in badminton & volleyball?", ["deuce"]),
                ],
            },
            "c": {  # Aptitude
                1: [
                    ("Which is the smallest prime number?", ["2"]),
                    ("What % of numbers from 1-70 end with 1 or 9?", ["20"]),
                    ("Two numbers ratio 4:5, LCM 240 → sum?", ["108"]),
                    ("If a-b=16 & a2-b2=544, find 2ab.", ["450"]),
                    ("Square root of 44521?", ["211"]),
                ],
                2: [
                    ("Smallest number to add to 2190 to make cube?", ["7"]),
                    ("Today Wed. What day after 81 days?", ["sunday"]),
                    ("Prime factors count in 9900?", ["11"]),
                    ("HCF of 405,585,765,900?", ["45"]),
                    ("MANGO→NZOHQ; APPLE→?", ["bqqmf"]),
                ],
                3: [
                    ("Largest 4-digit number divisible by 8?", ["9992"]),
                    ("Third odd integer if 3×1st = 2×3rd + 3?", ["54"]),
                    ("Product=9375, quotient=15 → sum?", ["400"]),
                    ("10% radius reduction reduces area by?", ["19"]),
                    ("Coins of 4 types, no. of sums?", ["15"]),
                ],
            },
            "d": {  # Fun
                1: [
                    ("What is always coming but never arrives?", ["tomorrow"]),
                    ("What gets wetter while drying?", ["towel"]),
                    ("What can be broken but not held?", ["promise"]),
                    ("Starts & ends with E but holds one letter?", ["envelope"]),
                    ("I grow shorter as I stand. What am I?", ["candle"]),
                ],
                2: [
                    ("What can you hold without touching?", ["conversation"]),
                    ("What can you make yet never see?", ["noise"]),
                    ("So fragile that speaking breaks it?", ["silence"]),
                    ("What goes up when rain comes down?", ["umbrella"]),
                    ("2's company, 3's crowd. 4+5?", ["nine","9"]),
                ],
                3: [
                    ("What has 4 eyes but can't see?", ["mississippi"]),
                    ("What has one eye but can't see?", ["needle"]),
                    ("Before Everest was discovered, tallest mountain?", ["everest","mount everest"]),
                    ("If VP dies, who becomes president?", ["president"]),
                    ("Pass 2nd place in race → place?", ["second"]),
                ],
            }
        }

        # ---------------- UI ----------------
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(self, label="QUIZ GAME")
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        title.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        # Output Display
        self.output = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE | wx.TE_RICH2
        )
        self.output.SetBackgroundColour(wx.Colour(40, 10, 55))
        self.output.SetForegroundColour(wx.Colour(255, 255, 255))
        self.output.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(self.output, 1, wx.EXPAND | wx.ALL, 10)

        # Input Row
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.input.SetBackgroundColour(wx.Colour(70, 30, 110))
        self.input.SetForegroundColour(wx.Colour(255, 255, 255))
        self.input.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_submit)
        hbox.Add(self.input, 1, wx.EXPAND | wx.ALL, 5)

        self.submit_btn = wx.Button(self, label="Submit")
        self.submit_btn.SetBackgroundColour(wx.Colour(120, 40, 165))
        self.submit_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.submit_btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        hbox.Add(self.submit_btn, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.EXPAND)

        self.SetSizer(vbox)

        # Start game
        self.show_welcome()
        self.ask_topic()

    # ---------- Game Logic ----------
    def show_welcome(self):
        self.append("Welcome to the Quiz Game\n")
        self.append("Choose a topic:\n")
        self.append("a - General Knowledge\n")
        self.append("b - Sports Knowledge\n")
        self.append("c - Aptitude Quiz\n")
        self.append("d - Fun Questions\n")

    def ask_topic(self):
        self.state = "choose_topic"
        self.append("\nType a, b, c or d and press Enter:\n")

    def show_edit_mode(self):
        self.edit_mode = True
        self.append("\n📝 EDIT MODE - Customize Questions 📝\n")
        self.append("Commands:\n")
        self.append("- add a 1 \"What?\" answer1 answer2\n")
        self.append("- remove a 1 2 (removes Q#2 from a level 1)\n")
        self.append("- list a 1 (shows all Qs in a level 1)\n")
        self.append("- reset (restore defaults)\n")
        self.append("- done (start playing)\n")
        self.state = "edit_mode"

    def start_level(self, level):
        self.level = level
        self.q_index = 0
        if level == 1: self.score = 0
        if level == 2: self.score1 = 0
        if level == 3: self.score2 = 0

        self.append(f"\nYour Topic: {self.topic_name()}\n")
        self.append(f"Level {level}\n")
        self.state = "asking"
        self.ask_question()

    def topic_name(self):
        names = {
            "a": "General Knowledge",
            "b": "Sports Knowledge", 
            "c": "Aptitude Quiz",
            "d": "Fun Questions",
        }
        return names.get(self.topic, "")

    def ask_question(self):
        questions = self.quiz_data[self.topic][self.level]
        if self.q_index < len(questions):
            q = questions[self.q_index][0]
            self.append(f"\nQuestion {self.q_index + 1}: {q}\n")
        else:
            self.finish_level()

    def finish_level(self):
        questions = self.quiz_data[self.topic][self.level]
        total = len(questions)
        score = {1: self.score, 2: self.score1, 3: self.score2}[self.level]

        self.append(f"\nYou got {score} correct\n")
        self.append(f"Your score: {score * 5} / {total * 5}\n")

        if score >= 3 and self.level < 3:
            self.append(f"\nGreat! You cleared Level {self.level}.\n")
            self.append("Go to next level? (yes/no)\n")
            self.state = "ask_next_level"
        elif score >= 3 and self.level == 3:
            self.append("\n🎉 You completed ALL levels! 🎉\n")
            self.state = "finished"
        else:
            self.append("\nYou did not clear the level. Type 'restart' to try again.\n")
            self.state = "finished"

    def on_submit(self, event):
        text = self.input.GetValue().strip()
        if not text: return

        self.append(f"\nYou: {text}\n")
        self.input.SetValue("")

        if self.state == "choose_topic":
            self.handle_topic_input(text)
        elif self.state == "asking":
            self.handle_answer(text)
        elif self.state == "ask_next_level":
            self.handle_next_level_choice(text)
        elif self.state == "finished":
            self.handle_finished(text)
        elif self.state == "edit_mode":
            self.handle_edit_mode(text)
        elif self.state == "choose_restart_mode":
            self.handle_restart_choice(text)

    def handle_topic_input(self, text):
        t = text.lower()
        if t in ["a", "b", "c", "d"]:
            self.topic = t
            self.edit_mode = False
            self.start_level(1)
        else:
            self.append("Invalid topic. Please enter a, b, c or d.\n")

    def handle_answer(self, text):
        answer = text.lower()
        questions = self.quiz_data[self.topic][self.level]
        q_text, correct_answers = questions[self.q_index]

        if answer in correct_answers:
            self.append("✅ Correct!\n")
            if self.level == 1: self.score += 1
            elif self.level == 2: self.score1 += 1
            else: self.score2 += 1
        else:
            self.append("❌ Incorrect!\n")
            correct_str = " or ".join(correct_answers)
            self.append(f"Correct answer: {correct_str}\n")

        self.q_index += 1
        self.ask_question()

    def handle_next_level_choice(self, text):
        if text.lower() == "yes":
            self.start_level(self.level + 1)
        else:
            self.append("Quiz ended. Type 'restart' to play again.\n")
            self.state = "finished"

    def handle_edit_mode(self, text):
        parts = text.split()
        if not parts:
            return

        cmd = parts[0].lower()
        
        if cmd == "done":
            self.edit_mode = False
            self.show_welcome()
            self.ask_topic()
            return
            
        elif cmd == "reset":
            self.reset_questions()
            self.append("✅ Default questions restored!\n")
            return
            
        elif cmd == "list" and len(parts) >= 3:
            topic, level = parts[1].lower(), int(parts[2])
            if topic in self.quiz_data and level in self.quiz_data[topic]:
                questions = self.quiz_data[topic][level]
                self.append(f"\n📋 {self.topic_name_for(topic)} Level {level}:\n")
                for i, (q, answers) in enumerate(questions, 1):
                    self.append(f"{i}. {q} | Answers: {', '.join(answers)}\n")
            else:
                self.append("❌ Invalid topic/level\n")
            return
            
        elif cmd == "add" and len(parts) >= 4:
            topic = parts[1].lower()
            level = int(parts[2])
            question = " ".join(parts[3:])
            answers = question.split(" | ")[1:] if " | " in question else [question.split(" ")[-1]]
            
            if topic not in self.quiz_data:
                self.quiz_data[topic] = {}
            if level not in self.quiz_data[topic]:
                self.quiz_data[topic][level] = []
                
            self.quiz_data[topic][level].append((question.split(" | ")[0], answers))
            self.append(f"✅ Added to {topic} level {level}: {question.split(' | ')[0]}\n")
            return
            
        elif cmd == "remove" and len(parts) >= 4:
            topic = parts[1].lower()
            level = int(parts[2])
            q_index = int(parts[3]) - 1
            
            if (topic in self.quiz_data and level in self.quiz_data[topic] 
                and 0 <= q_index < len(self.quiz_data[topic][level])):
                removed = self.quiz_data[topic][level].pop(q_index)
                self.append(f"✅ Removed from {topic} level {level}: {removed[0]}\n")
            else:
                self.append("❌ Question not found\n")
            return
        
        self.append("❌ Use: add/remove/list/reset/done\n")

    def topic_name_for(self, topic):
        names = {"a": "General Knowledge", "b": "Sports Knowledge", "c": "Aptitude Quiz", "d": "Fun Questions"}
        return names.get(topic, topic.upper())

    def reset_questions(self):
        # Restore all original questions (this method contains ALL original data)
        self.quiz_data = {
            "a": {
                1: [("What is the capital of india?", ["delhi"]), ("How many states are there in india?", ["28"]), ("How many uninon territories are there in India?", ["9"]), ("What does www stands for?", ["world wide web"]), ("What is the national game of India?", ["hockey"])],
                2: [("Which city in India is known as 'City of Joy'?", ["kolkata"]), ("What is study of fossils called?", ["paleontology"]), ("Which city is known as the Silicon Valley of India?", ["bangalore"]), ("Which country is known as the leading producer of 'tea'?", ["china"]), ("'Madhubani', a Style of folk Paintings, is popular in which state of India?", ["bihar"])],
                3: [("Which Indian state has the smallest coastline?", ["goa"]), ("Which city has the title of 'Scotland of the East' in India?", ["shillong"]), ("How many languages does the Indian constitution recognise?", ["22"]), ("Which ancient Indian text is known for its teachings on governance?", ["arthashastra"]), ("How many minutes are there in a week", ["10080"])]
            },
            "b": {
                1: [("Who captained India to its first ever cricket world cup victory?", ["kapil dev"]), ("Who was the first Indian cricketer to score a double century in ODI?", ["sachin tendulkar"]), ("Which Indian chess player holds the title of Grandmaster?", ["vishwanathan anand","vishwanathan"]), ("Which athlete is known as the 'Flying Sikh'?", ["milkha singh","milka singh"]), ("Who is the youngest Indian woman to climb Mount Everest?", ["bachendri pal"])],
                2: [("Who is the only Indian male boxer to win an Olympic medal?", ["vijender singh"]), ("Who won India's first Olympic badminton medal?", ["prakash padukone"]), ("Naidu cup is associated with which sport?", ["chess"]), ("Eden Gardens stadium is located in which city?", ["kolkata"]), ("What is the national sport of China?", ["table tennis"])],
                3: [("Which sport has stones slid on ice?", ["curling"]), ("India first participated in which Olympics?", ["1920"]), ("Which country has won most cricket world cups?", ["australia"]), ("Where was the first Olympic games held?", ["canada"]), ("Which term is used in badminton & volleyball?", ["deuce"])]
            },
            "c": {
                1: [("Which is the smallest prime number?", ["2"]), ("What % of numbers from 1-70 end with 1 or 9?", ["20"]), ("Two numbers ratio 4:5, LCM 240 → sum?", ["108"]), ("If a-b=16 & a2-b2=544, find 2ab.", ["450"]), ("Square root of 44521?", ["211"])],
                2: [("Smallest number to add to 2190 to make cube?", ["7"]), ("Today Wed. What day after 81 days?", ["sunday"]), ("Prime factors count in 9900?", ["11"]), ("HCF of 405,585,765,900?", ["45"]), ("MANGO→NZOHQ; APPLE→?", ["bqqmf"])],
                3: [("Largest 4-digit number divisible by 8?", ["9992"]), ("Third odd integer if 3×1st = 2×3rd + 3?", ["54"]), ("Product=9375, quotient=15 → sum?", ["400"]), ("10% radius reduction reduces area by?", ["19"]), ("Coins of 4 types, no. of sums?", ["15"])]
            },
            "d": {
                1: [("What is always coming but never arrives?", ["tomorrow"]), ("What gets wetter while drying?", ["towel"]), ("What can be broken but not held?", ["promise"]), ("Starts & ends with E but holds one letter?", ["envelope"]), ("I grow shorter as I stand. What am I?", ["candle"])],
                2: [("What can you hold without touching?", ["conversation"]), ("What can you make yet never see?", ["noise"]), ("So fragile that speaking breaks it?", ["silence"]), ("What goes up when rain comes down?", ["umbrella"]), ("2's company, 3's crowd. 4+5?", ["nine","9"])],
                3: [("What has 4 eyes but can't see?", ["mississippi"]), ("What has one eye but can't see?", ["needle"]), ("Before Everest was discovered, tallest mountain?", ["everest","mount everest"]), ("If VP dies, who becomes president?", ["president"]), ("Pass 2nd place in race → place?", ["second"])]
            }
        }

    def handle_finished(self, text):
        if text.lower() == "restart":
            self.output.Clear()
            self.topic = None
            self.level = 1
            self.score = self.score1 = self.score2 = 0
            self.q_index = 0
            self.append("🔄 Restarting... EDIT questions first? (edit/restart)\n")
            self.state = "choose_restart_mode"
        else:
            self.append("Type 'restart' to play again.\n")

    def handle_restart_choice(self, text):
        t = text.lower()
        if t == "edit":
            self.show_edit_mode()
        elif t == "restart":
            self.show_welcome()
            self.ask_topic()
        else:
            self.append("Type 'edit' or 'restart':\n")

    def append(self, msg):
        self.output.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 255, 255)))
        self.output.AppendText(msg)

