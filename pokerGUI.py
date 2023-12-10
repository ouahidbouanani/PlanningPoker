# import tkinter as tk
# from tkinter import simpledialog, filedialog, messagebox
# from tkinter import ttk
# import json
# from PIL import Image, ImageTk
# import tkinter.font as tkFont
# from strict_rule import StrictRule
# from average_rule import AverageRule

# class PlanningPokerGUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Planning Poker")

#         self.players = []
#         self.features = []
#         self.votes = {}
#         self.rules = None

#         # Create the left frame for the menu bar
#         self.left_frame = tk.Frame(self.root, width=250, bg='teal')
#         self.left_frame.pack_propagate(False)
#         self.left_frame.pack(side='left', fill='y')

#         # Create the main frame for the content
#         self.main_frame = tk.Frame(self.root)
#         self.main_frame.pack(side='left', fill='both', expand=True)

#         self.create_menu()

#     def create_menu(self):
#         menu_frame = tk.Frame(self.left_frame, bg='teal')
#         menu_frame.pack()

#         # Set a custom font style for the label
#         font_style = tkFont.Font(family="Comic Sans MS", size=16, weight="bold", slant="italic")
#         tk.Label(menu_frame, text="Planning Poker", font=font_style, bg='teal', fg='white').grid(row=0, column=0, pady=10)

#         # Load and display the image
#         img = Image.open("1.png")  # Replace with the path to your image
#         img = img.resize((100, 100))
#         img = ImageTk.PhotoImage(img)
#         image_label = tk.Label(menu_frame, image=img, bg='teal')
#         image_label.image = img
#         image_label.grid(row=1, column=0, pady=5)

#         buttons = [
#             ("Enter Players", self.enter_players),
#             ("Choose Rules", self.choose_rules),
#             ("Enter Features", self.enter_features),
#             ("Start Voting", self.start_voting),
#             ("Save Progress", self.save_progress),
#             ("Load Progress", self.load_progress),
#             ("Exit", self.root.destroy)
#         ]

#         for i, (text, command) in enumerate(buttons, start=2):
#             # Create themed buttons with hover effect
#             style = ttk.Style()
#             style.configure(f"TButton{i}.TButton", font=("Helvetica", 12), foreground='black', background='#008080')
#             hover_style = ttk.Style()
#             hover_style.map(f"TButton{i}.TButton",
#                             foreground=[('pressed', 'black'), ('active', 'black')],
#                             background=[('pressed', '#008080'), ('active', '#008080')])
        
#             ttk.Button(menu_frame, text=text, command=command, style=f"TButton{i}.TButton").grid(row=i, column=0, pady=5)


#     def choose_rules(self):
#         rules_list = ["Strict (Unanimity)", "Average"]
#         rule_choice = simpledialog.askstring("Choose Rules", "Choose planning poker rules:", initialvalue=rules_list[0])
#         if rule_choice == "Strict (Unanimity)":
#             self.rules = StrictRule()
#         elif rule_choice == "Average":
#             self.rules = AverageRule()

#     def enter_players(self):
#         num_players = simpledialog.askinteger("Enter Players", "Enter the number of players:")
#         for i in range(num_players):
#             player_name = simpledialog.askstring("Enter Players", f"Enter nickname for Player {i + 1}:")
#             self.players.append(player_name)

#     def enter_features(self):
#         features_str = simpledialog.askstring("Enter Features", "Enter features (backlog) in JSON format:")

#         if features_str is None:
#             tk.messagebox.showwarning("Warning", "No features entered.")
#             return

#         try:
#             self.features = json.loads(features_str)
#         except json.decoder.JSONDecodeError:
#             tk.messagebox.showerror("Error", "Invalid JSON format. Please enter features in correct JSON format.")
#             return

#     def start_voting(self):
#         if not self.players or not self.features or not self.rules:
#             tk.messagebox.showwarning("Warning", "Please enter players, features, and choose rules before starting voting.")
#             return

#         voting_frame = tk.Toplevel(self.root)
#         tk.Label(voting_frame, text="Voting Screen").pack()

#         for feature in self.features:
#             tk.Label(voting_frame, text=f"Voting for Feature: {feature}").pack()
#             self.votes = {}
#             for player in self.players:
#                 vote = simpledialog.askstring("Voting", f"{player}'s vote:")
#                 self.votes[player] = vote

#             if self.rules.validate_votes(self.votes):
#                 tk.Label(voting_frame, text=f"Feature {feature} approved!").pack()
#             else:
#                 tk.Label(voting_frame, text=f"Feature {feature} not approved. Repeating voting.").pack()

#     def save_progress(self):
#         if not self.players or not self.features or not self.rules:
#             tk.messagebox.showwarning("Warning", "Nothing to save. Please enter players, features, and choose rules before saving.")
#             return

#         file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
#         if file_path:
#             progress_data = {
#                 "players": self.players,
#                 "features": self.features,
#                 "rules": "StrictRule" if isinstance(self.rules, StrictRule) else "AverageRule",
#             }

#             with open(file_path, "w") as file:
#                 json.dump(progress_data, file)
#             tk.messagebox.showinfo("Save Progress", "Progress saved successfully.")

#     def load_progress(self):
#         file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
#         if file_path:
#             with open(file_path, "r") as file:
#                 progress_data = json.load(file)

#             self.players = progress_data.get("players", [])
#             self.features = progress_data.get("features", [])
#             rules_type = progress_data.get("rules", "")

#             if rules_type == "StrictRule":
#                 self.rules = StrictRule()
#             elif rules_type == "AverageRule":
#                 self.rules = AverageRule()

#             tk.messagebox.showinfo("Load Progress", "Progress loaded successfully.")

#     def run(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     planning_poker_gui = PlanningPokerGUI()
#     planning_poker_gui.run()



import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from tkinter import ttk
import json
from PIL import Image, ImageTk
import tkinter.font as tkFont
from strict_rule import StrictRule
from average_rule import AverageRule

class PlanningPokerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planning Poker")

        # Set minimum window size
        self.root.minsize(800, 500)

        # Schedule the set_initial_size method to run after the main loop has started
        self.root.after(100, self.set_initial_size)

        self.players = []
        self.features = []
        self.votes = {}
        self.rules = None

        # Create the left frame for the menu bar
        self.left_frame = tk.Frame(self.root, width=250, bg='teal')
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side='left', fill='y')

        # Create the main frame for the content
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side='left', fill='both', expand=True)

        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self.left_frame, bg='teal')
        menu_frame.pack()

        # Set a custom font style for the label
        font_style = tkFont.Font(family="Comic Sans MS", size=16, weight="bold", slant="italic")
        tk.Label(menu_frame, text="Planning Poker", font=font_style, bg='teal', fg='white').grid(row=0, column=0, pady=10)

        # Load and display the image
        img = Image.open("1.png")  # Replace with the path to your image
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(menu_frame, image=img, bg='teal')
        image_label.image = img
        image_label.grid(row=1, column=0, pady=5)

        buttons = [
            ("Enter Players", self.enter_players),
            ("Choose Rules", self.choose_rules),
            ("Enter Features", self.enter_features),
            ("Start Voting", self.start_voting),
            ("Save Progress", self.save_progress),
            ("Load Progress", self.load_progress),
            ("Exit", self.root.destroy)
        ]

        for i, (text, command) in enumerate(buttons, start=2):
            # Create themed buttons with hover effect
            style = ttk.Style()
            style.configure(f"TButton{i}.TButton", font=("Helvetica", 12), foreground='black', background='#008080')
            hover_style = ttk.Style()
            hover_style.map(f"TButton{i}.TButton",
                            foreground=[('pressed', 'black'), ('active', 'black')],
                            background=[('pressed', '#008080'), ('active', '#008080')])

            ttk.Button(menu_frame, text=text, command=command, style=f"TButton{i}.TButton").grid(row=i, column=0, pady=5)

    def set_initial_size(self):
        self.root.geometry("400x300")

    def choose_rules(self):
        rules_list = ["Strict (Unanimity)", "Average"]
        rule_choice = simpledialog.askstring("Choose Rules", "Choose planning poker rules:", initialvalue=rules_list[0])
        if rule_choice == "Strict (Unanimity)":
            self.rules = StrictRule()
        elif rule_choice == "Average":
            self.rules = AverageRule()

    def enter_players(self):
        num_players = simpledialog.askinteger("Enter Players", "Enter the number of players:")
        for i in range(num_players):
            player_name = simpledialog.askstring("Enter Players", f"Enter nickname for Player {i + 1}:")
            self.players.append(player_name)

    def enter_features(self):
        features_str = simpledialog.askstring("Enter Features", "Enter features (backlog) in JSON format:")

        if features_str is None:
            tk.messagebox.showwarning("Warning", "No features entered.")
            return

        try:
            self.features = json.loads(features_str)
        except json.decoder.JSONDecodeError:
            tk.messagebox.showerror("Error", "Invalid JSON format. Please enter features in correct JSON format.")
            return

    def start_voting(self):
        if not self.players or not self.features or not self.rules:
            tk.messagebox.showwarning("Warning", "Please enter players, features, and choose rules before starting voting.")
            return

        voting_frame = tk.Toplevel(self.root)
        tk.Label(voting_frame, text="Voting Screen").pack()

        for feature in self.features:
            tk.Label(voting_frame, text=f"Voting for Feature: {feature}").pack()
            self.votes = {}
            for player in self.players:
                vote = simpledialog.askstring("Voting", f"{player}'s vote:")
                self.votes[player] = vote

            if self.rules.validate_votes(self.votes):
                tk.Label(voting_frame, text=f"Feature {feature} approved!").pack()
            else:
                tk.Label(voting_frame, text=f"Feature {feature} not approved. Repeating voting.").pack()

    def save_progress(self):
        if not self.players or not self.features or not self.rules:
            tk.messagebox.showwarning("Warning", "Nothing to save. Please enter players, features, and choose rules before saving.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            progress_data = {
                "players": self.players,
                "features": self.features,
                "rules": "StrictRule" if isinstance(self.rules, StrictRule) else "AverageRule",
            }

            with open(file_path, "w") as file:
                json.dump(progress_data, file)
            tk.messagebox.showinfo("Save Progress", "Progress saved successfully.")

    def load_progress(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                progress_data = json.load(file)

            self.players = progress_data.get("players", [])
            self.features = progress_data.get("features", [])
            rules_type = progress_data.get("rules", "")

            if rules_type == "StrictRule":
                self.rules = StrictRule()
            elif rules_type == "AverageRule":
                self.rules = AverageRule()

            tk.messagebox.showinfo("Load Progress", "Progress loaded successfully.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    planning_poker_gui = PlanningPokerGUI()
    planning_poker_gui.run()
