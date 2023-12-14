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

#         self.root.minsize(800, 500)
#         self.root.after(100, self.set_initial_size)

#         self.players = []
#         self.features = []
#         self.votes = {}
#         self.rules = None
#         self.voting_window = None 

#         self.left_frame = tk.Frame(self.root, width=250, bg='teal')
#         self.left_frame.pack_propagate(False)
#         self.left_frame.pack(side='left', fill='y')

#         self.main_frame = tk.Frame(self.root)
#         self.main_frame.pack(side='left', fill='both', expand=True)
        
#         self.selected_rule_label = tk.Label(self.main_frame, text="Selected Rules: None")

#         # Divide the right side into two parts (40%, 60%)
#         right_frame = tk.Frame(self.main_frame)
#         right_frame.pack(side='left', fill='both', expand=True, pady=0)  # Adjust pady value as needed
#         self.top_labels = []

#         frame1 = tk.Frame(right_frame)
#         frame1.grid(row=0, column=0, pady=20)

#         frame2 = tk.Frame(right_frame)
#         frame2.grid(row=0, column=1, pady=20)

#         # Create initial top labels in the frames
#         label1 = tk.Label(frame1, text="Label 1")
#         label1.pack()

#         label2 = tk.Label(frame2, text="Label 2")
#         label2.pack()

#         # Append labels to the list
#         self.top_labels.extend([label1, label2])

#         # Create a label to display players
#         self.players_label = tk.Label(right_frame)

#         self.create_menu()

#     def create_menu(self):
#         menu_frame = tk.Frame(self.left_frame, bg='teal')
#         menu_frame.pack()

#         font_style = tkFont.Font(family="Comic Sans MS", size=16, weight="bold", slant="italic")
#         tk.Label(menu_frame, text="Planning Poker", font=font_style, bg='teal', fg='white').grid(row=0, column=0, pady=10)

#         img = Image.open("1.png")
#         img = img.resize((100, 100))
#         img = ImageTk.PhotoImage(img)
#         image_label = tk.Label(menu_frame, image=img, bg='teal')
#         image_label.image = img
#         image_label.grid(row=1, column=0, pady=5)

#         buttons = [
#             ("Enter Players", lambda: self.enter_players_count(self.root)),
#             ("Choose Rules", self.choose_rules),
#             ("Enter Features", self.enter_features),
#             ("Start Voting", self.start_voting),
#             ("Save Progress", self.save_progress),
#             ("Load Progress", self.load_progress),
#             ("Exit", self.root.destroy)
#         ]

#         for i, (text, command) in enumerate(buttons, start=2):
#             style = ttk.Style()
#             style.configure(f"TButton{i}.TButton", font=("Helvetica", 12), foreground='black', background='#008080')
#             hover_style = ttk.Style()
#             hover_style.map(f"TButton{i}.TButton",
#                             foreground=[('pressed', 'black'), ('active', 'black')],
#                             background=[('pressed', '#008080'), ('active', '#008080')])

#             ttk.Button(menu_frame, text=text, command=command, style=f"TButton{i}.TButton").grid(row=i, column=0, pady=5)

#     def set_initial_size(self):
#         self.root.geometry("400x300")

#     def enter_players_count(self, window):
#         players_entry_window = tk.Toplevel(self.root)
#         players_entry_window.title("Enter Players")
#         players_entry_window.geometry("400x400")
#         players_entry_window.configure(bg='teal')
#         players_entry_window.resizable(width=False, height=False)

#         num_players_label = tk.Label(players_entry_window, text="Enter the number of players:", bg='teal', fg='white')
#         num_players_label.pack(pady=5)
#         num_players_entry = tk.Entry(players_entry_window)
#         num_players_entry.pack(pady=5)

#         confirm_button = tk.Button(players_entry_window, text="Confirm", command=lambda: self.process_players_input(players_entry_window, num_players_entry.get()))
#         confirm_button.pack(pady=10)

#     def process_players_input(self, window, num_players):
#         try:
#             num_players = int(num_players)
#             if num_players <= 0:
#                 tk.messagebox.showwarning("Warning", "Number of players must be a positive integer.")
#                 return
#         except ValueError:
#             tk.messagebox.showwarning("Warning", "Invalid input. Please enter a valid number.")
#             return

#         player_names_label = tk.Label(window, text=f"Enter {num_players} player names separated by commas:", bg='teal', fg='white')
#         player_names_label.pack(pady=5)
#         player_names_entry = tk.Entry(window)
#         player_names_entry.pack(pady=5)

#         confirm_button = tk.Button(window, text="Confirm", command=lambda: self.process_player_names(player_names_entry.get(), num_players, window))
#         confirm_button.pack(pady=10)

#     def process_player_names(self, players_input, num_players, window):
#         window.destroy()

#         if players_input is None:
#             tk.messagebox.showwarning("Warning", "No players entered.")
#             return

#         player_names = [name.strip() for name in players_input.split(',')]

#         if len(player_names) != num_players:
#             tk.messagebox.showwarning("Warning", f"Entered {len(player_names)} players, but expected {num_players}. Please try again.")
#             return

#         self.players = player_names
#         self.update_players_label()

#     def update_players_label(self):
#         players_text = "Players:\n" + "\n".join([f"Player {i}: {player_name}" for i, player_name in enumerate(self.players, start=1)])
#         self.players_label.config(text=players_text)
#         self.top_labels[0].config(text=f" {players_text}")

#     def choose_rules(self):
#         rule_selection_window = tk.Toplevel(self.root)
#         rule_selection_window.title("Select Planning Poker Rules")
#         rule_selection_window.geometry("400x400")
#         rule_selection_window.configure(bg='teal')
#         rule_selection_window.resizable(width=False, height=False)

#         instruction_label = tk.Label(rule_selection_window, text="Select planning poker rules:", bg='teal', fg='white')
#         instruction_label.pack(pady=10)

#         rules_list = ["Strict (Unanimity)", "Average"]
#         selected_rule_var = tk.StringVar(value=rules_list[0])
#         rules_combobox = ttk.Combobox(rule_selection_window, values=rules_list, textvariable=selected_rule_var)
#         rules_combobox.pack(pady=10)

#         confirm_button = tk.Button(rule_selection_window, text="Confirm", command=lambda: self.process_rule_selection(rule_selection_window, selected_rule_var.get()))
#         confirm_button.pack(pady=10)

#     def process_rule_selection(self, window, selected_rule):
#         window.destroy()

#         if selected_rule == "Strict (Unanimity)":
#             self.rules = StrictRule()
#         elif selected_rule == "Average":
#             self.rules = AverageRule()

#         self.selected_rule_label.config(text=f"Selected Rule: {selected_rule}")
#         self.top_labels[1].config(text=f"Selected Rule: {selected_rule}")

#     def enter_features(self):
#         features_entry_window = tk.Toplevel(self.root)
#         features_entry_window.title("Enter Features")
#         features_entry_window.geometry("400x400")
#         features_entry_window.configure(bg='teal')
#         features_entry_window.resizable(width=False, height=False)

#         features_label = tk.Label(features_entry_window, text="Enter features (backlog) in JSON format: ", bg='teal', fg='white')
#         features_label.pack(pady=10)

#         features_entry = tk.Text(features_entry_window, wrap="word", height=10, width=40)
#         features_entry.pack(pady=10)

#         confirm_button = tk.Button(features_entry_window, text="Confirm", command=lambda: self.process_features_input(features_entry.get("1.0", tk.END), features_entry_window))
#         confirm_button.pack(pady=10)

#     def process_features_input(self, features_input, window):
#         window.destroy()

#         if not features_input.strip():
#             tk.messagebox.showwarning("Warning", "No features entered.")
#             return

#         try:
#             self.features = json.loads(features_input)
#         except json.decoder.JSONDecodeError:
#             tk.messagebox.showerror("Error", "Invalid JSON format. Please enter features in correct JSON format.")
#             return

#     def start_voting(self):
#         if not self.players or not self.features or not self.rules:
#             tk.messagebox.showwarning("Warning", "Please enter players, features, and choose rules before starting voting.")
#             return

#         # Create a new Toplevel window for voting or update the existing one
#         if self.voting_window is None:
#             self.voting_window = tk.Toplevel(self.root)
#             self.voting_window.title("Voting Screen")
#         else:
#             # Clear previous content if updating
#             for widget in self.voting_window.winfo_children():
#                 widget.destroy()

#         for feature in self.features:
#             feature_label = tk.Label(self.voting_window, text=f"Voting for Feature: {feature}")
#             feature_label.pack()

#             for player in self.players:
#                 vote_entry, confirm_button = self.get_vote_widgets(self.voting_window, player)
#                 confirm_button.config(command=lambda p=player, v=vote_entry: self.set_vote_result(p, v))

#     def get_vote_widgets(self, parent, player):
#         # Use the parent window (voting_window) for creating widgets
#         # ...

#         # Example: Entry widget for vote input
#         vote_entry = tk.Entry(parent)
#         vote_entry.pack(pady=10)

#         # Button to confirm the vote
#         confirm_button = tk.Button(parent, text="Confirm")
#         confirm_button.pack(pady=10)

#         return vote_entry, confirm_button

#     def set_vote_result(self, player, result_entry):
#         result = result_entry.get()
#         self.votes[player] = result

#         # Check if all votes are collected before evaluating
#         if len(self.votes) == len(self.players) * len(self.features):
#             self.evaluate_votes()

#     def evaluate_votes(self):
#         for feature in self.features:
#             if self.rules.validate_votes(self.votes):
#                 result_text = f"Feature {feature} approved!"
#             else:
#                 result_text = f"Feature {feature} not approved. Repeating voting."

#             result_label = tk.Label(self.voting_window, text=result_text)
#             result_label.pack()

#         # Clear votes for the next round
#         self.votes = {}

#     def evaluate_votes(self):
#         for feature in self.features:
#             if self.rules.validate_votes(self.votes):
#                 result_text = f"Feature {feature} approved!"
#             else:
#                 result_text = f"Feature {feature} not approved. Repeating voting."

#             result_label = tk.Label(self.root, text=result_text)
#             result_label.pack()


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

#             # Update the label in the main window
#             self.update_players_label()

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

        self.root.minsize(800, 500)
        self.root.after(100, self.set_initial_size)

        self.players = []
        self.features = []
        self.votes = {}
        self.rules = None
        self.voting_window = None
        self.current_player_index = 0
        self.current_feature_index = 0

        self.left_frame = tk.Frame(self.root, width=250, bg='teal')
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side='left', fill='y')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side='left', fill='both', expand=True)

        self.selected_rule_label = tk.Label(self.main_frame, text="Selected Rules: None")

        # Divide the right side into two parts (40%, 60%)
        right_frame = tk.Frame(self.main_frame)
        right_frame.pack(side='left', fill='both', expand=True, pady=0)  # Adjust pady value as needed
        self.top_labels = []

        frame1 = tk.Frame(right_frame)
        frame1.grid(row=0, column=0, pady=20)

        frame2 = tk.Frame(right_frame)
        frame2.grid(row=0, column=1, pady=20)

        # Create initial top labels in the frames
        label1 = tk.Label(frame1, text="Label 1")
        label1.pack()

        label2 = tk.Label(frame2, text="Label 2")
        label2.pack()

        # Append labels to the list
        self.top_labels.extend([label1, label2])

        # Create a label to display players
        self.players_label = tk.Label(right_frame)

        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self.left_frame, bg='teal')
        menu_frame.pack()

        font_style = tkFont.Font(family="Comic Sans MS", size=16, weight="bold", slant="italic")
        tk.Label(menu_frame, text="Planning Poker", font=font_style, bg='teal', fg='white').grid(row=0, column=0, pady=10)

        img = Image.open("1.png")
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(menu_frame, image=img, bg='teal')
        image_label.image = img
        image_label.grid(row=1, column=0, pady=5)

        buttons = [
            ("Enter Players", lambda: self.enter_players_count(self.root)),
            ("Choose Rules", self.choose_rules),
            ("Enter Features", self.enter_features),
            ("Start Voting", self.start_voting),
            ("Save Progress", self.save_progress),
            ("Load Progress", self.load_progress),
            ("Exit", self.root.destroy)
        ]

        for i, (text, command) in enumerate(buttons, start=2):
            style = ttk.Style()
            style.configure(f"TButton{i}.TButton", font=("Helvetica", 12), foreground='black', background='#008080')
            hover_style = ttk.Style()
            hover_style.map(f"TButton{i}.TButton",
                            foreground=[('pressed', 'black'), ('active', 'black')],
                            background=[('pressed', '#008080'), ('active', '#008080')])

            ttk.Button(menu_frame, text=text, command=command, style=f"TButton{i}.TButton").grid(row=i, column=0, pady=5)

    def set_initial_size(self):
        self.root.geometry("400x300")

    def enter_players_count(self, window):
        players_entry_window = tk.Toplevel(self.root)
        players_entry_window.title("Enter Players")
        players_entry_window.geometry("400x400")
        players_entry_window.configure(bg='teal')
        players_entry_window.resizable(width=False, height=False)

        num_players_label = tk.Label(players_entry_window, text="Enter the number of players:", bg='teal', fg='white')
        num_players_label.pack(pady=5)
        num_players_entry = tk.Entry(players_entry_window)
        num_players_entry.pack(pady=5)

        confirm_button = tk.Button(players_entry_window, text="Confirm", command=lambda: self.process_players_input(players_entry_window, num_players_entry.get()))
        confirm_button.pack(pady=10)

    def process_players_input(self, window, num_players):
        try:
            num_players = int(num_players)
            if num_players <= 0:
                tk.messagebox.showwarning("Warning", "Number of players must be a positive integer.")
                return
        except ValueError:
            tk.messagebox.showwarning("Warning", "Invalid input. Please enter a valid number.")
            return

        player_names_label = tk.Label(window, text=f"Enter {num_players} player names separated by commas:", bg='teal', fg='white')
        player_names_label.pack(pady=5)
        player_names_entry = tk.Entry(window)
        player_names_entry.pack(pady=5)

        confirm_button = tk.Button(window, text="Confirm", command=lambda: self.process_player_names(player_names_entry.get(), num_players, window))
        confirm_button.pack(pady=10)

    def process_player_names(self, players_input, num_players, window):
        window.destroy()

        if players_input is None:
            tk.messagebox.showwarning("Warning", "No players entered.")
            return

        player_names = [name.strip() for name in players_input.split(',')]

        if len(player_names) != num_players:
            tk.messagebox.showwarning("Warning", f"Entered {len(player_names)} players, but expected {num_players}. Please try again.")
            return

        self.players = player_names
        self.update_players_label()

    def update_players_label(self):
        players_text = "Players:\n" + "\n".join([f"Player {i}: {player_name}" for i, player_name in enumerate(self.players, start=1)])
        self.players_label.config(text=players_text)
        self.top_labels[0].config(text=f" {players_text}")

    def choose_rules(self):
        rule_selection_window = tk.Toplevel(self.root)
        rule_selection_window.title("Select Planning Poker Rules")
        rule_selection_window.geometry("400x400")
        rule_selection_window.configure(bg='teal')
        rule_selection_window.resizable(width=False, height=False)

        instruction_label = tk.Label(rule_selection_window, text="Select planning poker rules:", bg='teal', fg='white')
        instruction_label.pack(pady=10)

        rules_list = ["Strict (Unanimity)", "Average"]
        selected_rule_var = tk.StringVar(value=rules_list[0])
        rules_combobox = ttk.Combobox(rule_selection_window, values=rules_list, textvariable=selected_rule_var)
        rules_combobox.pack(pady=10)

        confirm_button = tk.Button(rule_selection_window, text="Confirm", command=lambda: self.process_rule_selection(rule_selection_window, selected_rule_var.get()))
        confirm_button.pack(pady=10)

    def process_rule_selection(self, window, selected_rule):
        window.destroy()

        if selected_rule == "Strict (Unanimity)":
            self.rules = StrictRule()
        elif selected_rule == "Average":
            self.rules = AverageRule()

        self.selected_rule_label.config(text=f"Selected Rule: {selected_rule}")
        self.top_labels[1].config(text=f"Selected Rule: {selected_rule}")

    def enter_features(self):
        features_entry_window = tk.Toplevel(self.root)
        features_entry_window.title("Enter Features")
        features_entry_window.geometry("400x400")
        features_entry_window.configure(bg='teal')
        features_entry_window.resizable(width=False, height=False)

        features_label = tk.Label(features_entry_window, text="Enter features (backlog) in JSON format: ", bg='teal', fg='white')
        features_label.pack(pady=10)

        features_entry = tk.Text(features_entry_window, wrap="word", height=10, width=40)
        features_entry.pack(pady=10)

        confirm_button = tk.Button(features_entry_window, text="Confirm", command=lambda: self.process_features_input(features_entry.get("1.0", tk.END), features_entry_window))
        confirm_button.pack(pady=10)

    def process_features_input(self, features_input, window):
        window.destroy()

        if not features_input.strip():
            tk.messagebox.showwarning("Warning", "No features entered.")
            return

        try:
            self.features = json.loads(features_input)
        except json.decoder.JSONDecodeError:
            tk.messagebox.showerror("Error", "Invalid JSON format. Please enter features in correct JSON format.")
            return

    def set_vote_result(self, player, result_entry, feature, label_text):
        result = result_entry.get("1.0", tk.END).strip()
        self.votes[(player, feature)] = result

        # Check if all votes are collected before evaluating
        if len(self.votes) == len(self.players) * len(self.features):
            self.evaluate_votes()

        # Update indices for the next set of widgets
        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0
            self.current_feature_index += 1

        # If all features have been voted on, reset indices
        if self.current_feature_index == len(self.features):
            self.current_feature_index = 0

        # Clear the content of the text box
        result_entry.delete("1.0", tk.END)

        # Update the label for the next set of widgets
        label_text.set(f"{self.players[self.current_player_index]}'s Vote for {self.features[self.current_feature_index]}: ")

        # If all votes are collected, automatically submit the votes
        if len(self.votes) == len(self.players) * len(self.features):
            self.submit_votes()

    def submit_votes(self):
        # Implement the logic to handle the submitted votes
        # For example, you can print the collected votes
        print("Collected Votes:")
        for (player, feature), vote in self.votes.items():
            print(f"{player}'s Vote for {feature}: {vote}")



    def start_voting(self):
        if not self.players or not self.features or not self.rules:
            tk.messagebox.showwarning("Warning", "Please enter players, features, and choose rules before starting voting.")
            return

        # Reset the votes dictionary and indices
        self.votes = {}
        self.current_player_index = 0
        self.current_feature_index = 0

        # Create a new Toplevel window for voting or update the existing one
        if self.voting_window is None:
            self.voting_window = tk.Toplevel(self.root)
            self.voting_window.title("Voting Screen")
        else:
            # Clear previous content if updating
            for widget in self.voting_window.winfo_children():
                widget.destroy()

        # Label for displaying the current voting information
        label_text = tk.StringVar()
        label_text.set(f"{self.players[self.current_player_index]}'s Vote for {self.features[self.current_feature_index]}: ")
        current_vote_label = tk.Label(self.voting_window, textvariable=label_text)
        current_vote_label.pack(pady=5)

        # Text widget for voting
        vote_text = tk.Text(self.voting_window, wrap="word", height=5, width=40)
        vote_text.pack(pady=10)

        # Button to submit the vote
        submit_button = tk.Button(self.voting_window, text="Submit", command=lambda: self.submit_vote(vote_text, label_text))
        submit_button.pack(pady=10)

        # Store the vote_text in a list for later access
        self.vote_texts = [vote_text] * len(self.players)

        # Create buttons with corresponding values
        values = [0, 1, 2, 3, 5, 8, 13, 20, 40, 100, 200, 300]
        for i, value in enumerate(values):
            button = tk.Button(self.voting_window, text=str(value), command=lambda v=value: self.update_vote_text(v))
            button.pack(side="left", padx=5)

    def submit_vote(self, vote_text, label_text):
        # Get the currently selected vote_text
        current_vote_text = self.vote_texts[self.current_player_index]

        # Insert the selected value into the text box
        current_vote_text.insert(tk.END, vote_text.get("1.0", tk.END).strip())

        # Check if all votes are collected before evaluating
        if len(self.votes) == len(self.players) * len(self.features):
            self.evaluate_votes()
        else:
            # Move to the next player and update the label for the next set of widgets
            self.current_player_index += 1
            if self.current_player_index == len(self.players):
                self.current_player_index = 0
                self.current_feature_index += 1

            # If all features have been voted on, show the result
            if self.current_feature_index == len(self.features):
                self.evaluate_votes()
            else:
                # Update the label for the next set of widgets
                label_text.set(f"{self.players[self.current_player_index]}'s Vote for {self.features[self.current_feature_index]}: ")

            # Clear the content of the text box
            vote_text.delete("1.0", tk.END)

    # def evaluate_votes(self):
    #     print("Collected Votes:")
    #     for (player, feature), vote in self.votes.items():
    #         print(f"{player}'s Vote for {feature}: {vote}")
    #     tk.messagebox.showinfo("Voting Result", "Voting process is complete. Display the result here.")
    
    def evaluate_votes(self):
        print("Collected Votes:")
        for (player, feature), vote in self.votes.items():
            print(f"{player}'s Vote for {feature}: {vote}")

        # Use rules to validate the votes
        if self.rules:
            approval_status = self.rules.validate_votes(self.votes)
            if approval_status:
                tk.messagebox.showinfo("Voting Result", "Voting process is complete. Display the result here.")
                self.save_difficulty_estimations()
            else:
                tk.messagebox.showwarning("Warning", "Feature not approved. Repeating the voting process.")
                # Clear votes and restart the voting process
                self.votes = {}
                self.start_voting()
                
    def save_difficulty_estimations(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            difficulty_estimations = {}
            for feature in self.features:
                total_votes = sum(int(self.votes.get((player, feature), 0)) for player in self.players)
                average_vote = total_votes / len(self.players)
                difficulty_estimations[feature] = average_vote

            with open(file_path, "w") as file:
                json.dump(difficulty_estimations, file)
            tk.messagebox.showinfo("Save Difficulty Estimations", "Difficulty estimations saved successfully.")



    def update_vote_text(self, value):
        # Get the currently selected vote_text
        current_vote_text = self.vote_texts[self.current_player_index]
        # Insert the selected value into the text box
        current_vote_text.insert(tk.END, str(value))

    def set_button_value(self, button_value, vote_text):
        # Set the corresponding button value in the text box
        current_text = vote_text.get("1.0", tk.END)
        updated_text = f"{current_text.strip()}\n{button_value}"
        vote_text.delete("1.0", tk.END)
        vote_text.insert(tk.END, updated_text)
    

    def close_voting_screen(self):
        if self.voting_window:
            self.voting_window.destroy()
            self.voting_window = None
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
                "votes": self.votes  # Include collected votes in the progress data
            }

            with open(file_path, "w") as file:
                json.dump(progress_data, file)
            tk.messagebox.showinfo("Save Progress", "Progress saved successfully.")

# Update the load_progress method in PlanningPokerGUI class
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

            # Update the label in the main window
            self.update_players_label()

            # Load collected votes
            self.votes = progress_data.get("votes", {})

            tk.messagebox.showinfo("Load Progress", "Progress loaded successfully.")


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    planning_poker_gui = PlanningPokerGUI()
    planning_poker_gui.run()
