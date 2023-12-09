# pokerGUI.py

import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import json
from strict_rule import StrictRule
from average_rule import AverageRule

class PlanningPokerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planning Poker")

        self.players = []
        self.features = []
        self.votes = {}
        self.rules = None

        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack()

        tk.Label(menu_frame, text="Planning Poker Menu").grid(row=0, column=1, pady=10)

        tk.Button(menu_frame, text="Enter Players", command=self.enter_players).grid(row=1, column=1)
        tk.Button(menu_frame, text="Choose Rules", command=self.choose_rules).grid(row=2, column=1)
        tk.Button(menu_frame, text="Enter Features", command=self.enter_features).grid(row=3, column=1)
        tk.Button(menu_frame, text="Start Voting", command=self.start_voting).grid(row=4, column=1)
        tk.Button(menu_frame, text="Save Progress", command=self.save_progress).grid(row=5, column=1)
        tk.Button(menu_frame, text="Load Progress", command=self.load_progress).grid(row=6, column=1)
        tk.Button(menu_frame, text="Exit", command=self.root.destroy).grid(row=7, column=1)

    def choose_rules(self):
        rules_list = ["Strict (Unanimity)", "Average"]  # Add more rules as needed
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
            # User clicked Cancel or closed the dialog
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
            self.votes = {}  # Reset votes for each feature
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
                # Add other data you want to save
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
