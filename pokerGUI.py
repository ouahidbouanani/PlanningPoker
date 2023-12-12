
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

        self.left_frame = tk.Frame(self.root, width=250, bg='teal')
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side='left', fill='y')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side='left', fill='both', expand=True)

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

        # Create a label to display players
        self.players_label = tk.Label(self.main_frame, text="Players:")
        self.players_label.pack(side='left', padx=5)  # Use 'left' to place it on the left side


    def set_initial_size(self):
        self.root.geometry("400x300")

    def choose_rules(self):
        rules_list = ["Strict (Unanimity)", "Average"]
        rule_choice = simpledialog.askstring("Choose Rules", "Choose planning poker rules:", initialvalue=rules_list[0])
        if rule_choice == "Strict (Unanimity)":
            self.rules = StrictRule()
        elif rule_choice == "Average":
            self.rules = AverageRule()

    def enter_players_count(self,window):
        # Create a custom dialog window
        players_entry_window = tk.Toplevel(self.root)
        players_entry_window.title("Enter Players")
        players_entry_window.geometry("500x500")
        players_entry_window.configure(bg='teal')
        players_entry_window.resizable(width=False, height=False)

        # Label and Entry for entering the number of players
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

        # Label and Entry for entering player names
        player_names_label = tk.Label(window, text=f"Enter {num_players} player names separated by commas:", bg='teal', fg='white')
        player_names_label.pack(pady=5)
        player_names_entry = tk.Entry(window)
        player_names_entry.pack(pady=5)

        # Button to confirm and proceed
        confirm_button = tk.Button(window, text="Confirm", command=lambda: self.process_player_names(player_names_entry.get(), num_players, window))
        confirm_button.pack(pady=10)

    def process_player_names(self, players_input, num_players, window):
        # Destroy the input window after processing
        window.destroy()

        if players_input is None:
            tk.messagebox.showwarning("Warning", "No players entered.")
            return

        # Split the input by commas to get individual player names
        player_names = [name.strip() for name in players_input.split(',')]

        # Check if the entered number of players matches the count
        if len(player_names) != num_players:
            tk.messagebox.showwarning("Warning", f"Entered {len(player_names)} players, but expected {num_players}. Please try again.")
            return

        # Update the players list
        self.players = player_names

        # Update the label in the main window
        self.update_players_label()


           


    def update_players_label(self):
        players_text = "Players:\n" + "\n".join([f"Player {i}: {player_name}" for i, player_name in enumerate(self.players, start=1)])
        self.players_label.config(text=players_text)

    

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

            # Update the label in the main window
            self.update_players_label()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    planning_poker_gui = PlanningPokerGUI()
    planning_poker_gui.run()
