


"""
@mainpage Planning Poker GUI Documentation

@section project_presentation Project Presentation

The Planning Poker GUI is designed to facilitate the Planning Poker estimation technique in Agile development.
It provides a visually intuitive interface for teams to collaboratively estimate task efforts during sprint planning.
The GUI aims to enhance communication, accuracy, and efficiency in the estimation process.


This separation enables easy updates to the user interface and logic independently, promoting a more flexible and
maintainable codebase.

@section chosen_patterns Chosen Patterns

The GUI leverages the Observer pattern to efficiently handle updates in the voting process. The Model notifies the
View of any changes in the data (e.g., votes), ensuring real-time updates in the user interface.

The Strategy pattern is employed in the implementation of voting rules. The ability to switch between Strict and
Average rules is achieved by encapsulating each rule in a separate class (StrictRule and AverageRule). This allows
for interchangeable rule implementations without modifying the core application logic.

@section diagrams_explanation Diagrams Explanation

### Class Diagram:
@image html 1.png "Class Diagram"
A Class Diagram provides an overview of the classes in the application and their relationships. It illustrates how
the PlanningPokerGUI, StrictRule, and AverageRule classes are structured and interact.

### Sequence Diagram:
@image html sequence_diagram.png "Sequence Diagram"
A Sequence Diagram demonstrates the flow of interactions during the voting process. It showcases how the GUI
coordinates with the voting rules, players, and features to achieve a collaborative estimation.

@section continuous_integration Continuous Integration

Continuous Integration (CI) is set up using a CI/CD pipeline with a version control system (e.g., Git) and a CI service
such as Jenkins or GitHub Actions. The pipeline includes steps for code linting, unit testing, and deployment.

- Code Linting: Ensures code consistency and adherence to coding standards.
- Unit Testing: Validates the functionality of individual units or components.
- Deployment: Automates the deployment process to ensure a consistent and reliable release.

CI enables early detection of issues, promotes code quality, and streamlines the development and deployment workflow.

@note
For detailed information on each topic, refer to the specific sections in the documentation.

@see
For detailed documentation on each class and their methods, refer to the respective class documentation.
"""




import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from tkinter import ttk
import json
from PIL import Image, ImageTk
import tkinter.font as tkFont
from strict_rule import StrictRule
from average_rule import AverageRule

class PlanningPokerGUI:
    """
    @brief Class for the Planning Poker GUI application.

    @details
    This class represents the graphical user interface (GUI) for a Planning Poker application.
    It includes attributes to manage the main window, players, features, votes, rules, and the voting process.

    @note
    To use this class, create an instance and call the `run` method to start the Tkinter main loop.

    @warning
    Make sure to set the necessary attributes such as players, features, and rules before starting the voting process.

    @code
    planning_poker_gui = PlanningPokerGUI()
    planning_poker_gui.run()
    @endcode

    @see
    For additional information on how to use this class, refer to the documentation of its methods.

    @par Attributes:
    - root: The main Tkinter window.
    - players: List of player names.
    - features: List of features (backlog).
    - votes: Dictionary to store votes.
    - rules: Rules object for voting validation.
    - voting_window: Tkinter window for the voting process.
    - current_player_index: Index to keep track of the current player.
    - current_feature_index: Index to keep track of the current feature.
    - left_frame: Tkinter Frame for the left side of the main window.
    - main_frame: Tkinter Frame for the main content.
    - selected_rule_label: Tkinter Label to display the selected rules.
    - top_labels: List to store top labels for display.
    """
    def __init__(self):
        """
        @brief Constructor for the PlanningPokerGUI class.

        Initializes the main Tkinter window and sets up the GUI elements.
        """
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
        
        frame3 = tk.Frame(right_frame)
        frame3.grid(row=0, column=2, pady=20)

        # Create initial top labels in the frames
        label1 = tk.Label(frame1, text="Players........")
        label1.pack()

        label2 = tk.Label(frame2, text="Rules.........")
        label2.pack()
        
        label3 = tk.Label(frame3, text="Features.........")
        label3.pack()

        # Append labels to the list
        self.top_labels.extend([label1, label2,label3])

        # Create a label to display players
        self.players_label = tk.Label(right_frame)
        self.create_menu()


    def create_menu(self):
        """
        @brief Create the menu section on the left side of the main window.

        Creates labels, buttons, and other GUI elements for user interaction.
        """
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
        """
        @brief Set the initial size of the main window.

        Called after a delay to adjust the size of the main window.
        """
        self.root.geometry("400x300")


    def enter_players_count(self, window):
        """
        @brief Prompt the user to enter the number of players.

        This method creates a new Toplevel window for entering the number of players.
        It includes a label, an entry field, and a confirmation button.
        The confirmation button triggers the processing of player input.

        @param window The Tkinter window for player count input.

        @return void
        """
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
        """
        @brief Process user input for the number of players and set up player name entry.

        This function takes the graphical user interface window and the number of players as input.
        It attempts to convert the provided number of players to an integer and validates if it is a positive integer.
        If the input is invalid, warning messages are displayed, and the function returns.
        If the input is valid, the function dynamically creates a label and an entry widget for player names.
        Additionally, a "Confirm" button is created with a callback function to process the entered player names.

        @param window The graphical user interface window in which the input will be processed.
        @param num_players The user-provided input indicating the desired number of players.

        @return void
        """
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
        """
        @brief Process the entered player names and update the players list.

        This function takes the entered player names, the expected number of players, and the Tkinter window for player names input.
        It destroys the input window and performs validation on the entered player names.
        If no players are entered, a warning message is displayed, and the function returns.
        If the number of entered players does not match the expected number, a warning message is shown, and the function returns.
        Otherwise, the players list is updated, and the method 'update_players_label' is called to reflect the changes.

        @param players_input Entered player names separated by commas.
        @param num_players Number of players expected.
        @param window Tkinter window for player names input.

        @return void
        """
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
        """
        @brief Update the label displaying the list of players.

        This method updates the label that displays the list of players.
        It generates a formatted text containing the player names and their corresponding indices, and updates the GUI accordingly.

        @return void
        """
        players_text = "Players:\n" + "\n".join([f"Player {i}: {player_name}" for i, player_name in enumerate(self.players, start=1)])
        self.players_label.config(text=players_text)
        self.top_labels[0].config(text=f" {players_text}")


    def choose_rules(self):
        """
        @brief Create a window for selecting planning poker rules.

        This method creates a window for selecting planning poker rules. The window includes a label with instructions,
        a combobox for choosing from a predefined list of rules, and a confirmation button.
        The selected rule is then processed using the 'process_rule_selection' method.

        @return void
        """
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
        """
        @brief Process the selected planning poker rule and update the rules attribute.

        This method takes the Tkinter window for rule selection and the selected planning poker rule as input.
        It destroys the rule selection window and updates the 'rules' attribute based on the selected rule.
        The method then updates the labels displaying the selected rule in the GUI.

        @param window Tkinter window for rule selection.
        @param selected_rule Selected planning poker rule.

        @return void
        """
        window.destroy()

        if selected_rule == "Strict (Unanimity)":
            self.rules = StrictRule()
        elif selected_rule == "Average":
            self.rules = AverageRule()

        self.selected_rule_label.config(text=f"Selected Rule: {selected_rule}")
        self.top_labels[1].config(text=f"Selected Rule: {selected_rule}")


    def enter_features(self):
        """
        @brief Create a window for entering features in JSON format.

        This method creates a window for entering features (backlog) in JSON format. The window includes a label with instructions,
        a text entry field for typing the features, and a confirmation button.
        The entered features are then processed using the 'process_features_input' method.

        @return void
        """
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
        """
        @brief Process the entered features in JSON format and update the features attribute.

        This method takes the entered features in JSON format and the Tkinter window for feature entry as input.
        It destroys the feature entry window and attempts to parse the entered JSON features.
        If successful, it updates the 'features' attribute; otherwise, it displays an error message.

        @param features_input Entered features in JSON format.
        @param window Tkinter window for feature entry.

        @return void
        """
        window.destroy()

        if not features_input.strip():
            tk.messagebox.showwarning("Warning", "No features entered.")
            return

        try:
            self.features = json.loads(features_input)
            self.update_features_label()
        except json.decoder.JSONDecodeError:
            tk.messagebox.showerror("Error", "Invalid JSON format. Please enter features in correct JSON format.")
            return


    def set_vote_result(self, player, result_entry, feature, label_text):
        """
        @brief Set the vote result for a player on a specific feature.
    
        This method takes the player, result entry, feature, and label text as input.
        It collects and stores the vote result for the given player and feature.
        After each vote, it checks if all votes are collected before evaluating.
        It then updates the indices for the next set of widgets and clears the content of the text box.
        If all features or votes are collected, it resets the corresponding indices and updates the label text accordingly.
        If all votes are collected, it automatically submits the votes.
    
        @param player The player casting the vote.
        @param result_entry The text entry field where the vote result is entered.
        @param feature The feature for which the vote is being cast.
        @param label_text The label text to be updated for the next set of widgets.
    
        @return void
        """
        result = result_entry.get("1.0", tk.END).strip()
        self.votes[(player, feature)] = result
    
        # Check if all votes are collected before evaluating
        if len(self.votes) == len(self.players) * len(self.features):
            self.evaluate_votes()
        else:
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


    
    
    def start_voting(self):
        """
        @brief Start the voting process by creating a window for voting.

        This method initiates the voting process, ensuring that players, features, and rules are entered.
        It resets the votes dictionary and indices, creates a new Toplevel window for voting, or updates the existing one.
        The window includes labels for current voting information, text widget for voting, and buttons for submitting votes.
        PNG images are used on buttons for different vote values.

        @return void
        """
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

        # Create buttons with corresponding PNG images
        image_paths = ["cartes_0.png", "cartes_1.png", "cartes_2.png", "cartes_3.png", "cartes_5.png", "cartes_8.png", "cartes_13.png", "cartes_20.png", "cartes_40.png", "cartes_100.png", "cartes_cafe.png", "cartes_interro.png"]

        for i, image_path in enumerate(image_paths):
            img = Image.open(image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)

            button = tk.Button(self.voting_window, image=img, command=lambda v=i: self.update_vote_text(v))
            button.image = img
            button.pack(side="left", padx=5)


    
    
    
    

    def submit_vote(self, vote_text, label_text):
        """
        @brief Submit a vote and handle the voting process.

        This method takes a text entry field for voting (`vote_text`) and the label text for updating the next set of widgets.
        It inserts the selected vote into the corresponding player's text box and checks if all votes are collected before evaluating.
        If all votes are collected, it triggers the evaluation process. Otherwise, it moves to the next player and updates the label.
        If all features have been voted on, it shows the result; otherwise, it updates the label for the next set of widgets.

        @param vote_text The text entry field containing the selected vote.
        @param label_text The label text for updating the next set of widgets.

        @return void
        """
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


    
    def evaluate_votes(self):
        """
        @brief Evaluate and process the collected votes.
    
        This method prints the collected votes to the console and uses the specified rules to validate the votes.
        If the votes are approved, it displays a message with the voting result, and you can customize the logic for further actions.
        If the votes are not approved, it shows a warning message, clears the votes, and restarts the voting process.
    
        @return void
        """
        print("Collected Votes:")
        for (player, feature), vote in self.votes.items():
            print(f"{player}'s Vote for {feature}: {vote}")
    
        # Use rules to validate the votes
        if self.rules:
            approval_status = self.rules.validate_votes(self.votes)
            if approval_status:
                # Check if the voting process is unanimous for all features
                if self._is_unanimous_for_all_features():
                    tk.messagebox.showinfo("Voting Result", "Voting process is complete. Display the result here.")
                    self.voting_window.destroy()
                else:
                    tk.messagebox.showwarning("Warning", "Not all features received unanimous votes. Repeating the voting process.")
                    # Clear votes and restart the voting process
                    self.votes = {}
            else:
                tk.messagebox.showwarning("Warning", "Feature not approved. Repeating the voting process.")
                # Clear votes and restart the voting process
                self.votes = {}
                self.start_voting()
            # Destroy the voting window
            if self.voting_window:
                self.voting_window.destroy()
    
    def _is_unanimous_for_all_features(self):
        """
        @brief Check if the voting process is unanimous for all features.
    
        This method checks if all features have received unanimous votes from all players.
    
        @return bool: True if unanimous for all features, False otherwise.
        """
        for feature in self.features:
            feature_votes = {player: self.votes.get((player, feature), '') for player in self.players}
            print(feature_votes)
            if not self.rules._check_unanimous(feature_votes):
                return False
        return True
    
    
                    
    def save_difficulty_estimations(self):
        """
        @brief Save the difficulty estimations based on the collected votes to a JSON file.

        This method prompts the user to choose a file path for saving the difficulty estimations in JSON format.
        It calculates the average vote for each feature and saves the difficulty estimations to the specified file.
        After saving, it displays an information message indicating the successful save.

        @return void
        """
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
        """
        @brief Update the vote text with the selected value.

        This method takes a value and updates the text entry field for the current player's vote.
        The value is inserted at the end of the current text.

        @param value The selected value to be added to the vote text.

        @return void
        """
        # Get the currently selected vote_text
        current_vote_text = self.vote_texts[self.current_player_index]
        # Insert the selected value into the text box
        current_vote_text.insert(tk.END, str(value))


    def set_button_value(self, button_value, vote_text):
        """
        @brief Set the corresponding button value in the text box.

        This method sets the corresponding button value in the text entry field for the current player's vote.
        The value is appended to the existing text.

        @param button_value The value associated with the clicked button.
        @param vote_text The text entry field for the current player's vote.

        @return void
        """
        # Set the corresponding button value in the text box
        current_text = vote_text.get("1.0", tk.END)
        updated_text = f"{current_text.strip()}\n{button_value}"
        vote_text.delete("1.0", tk.END)
        vote_text.insert(tk.END, updated_text)


    def close_voting_screen(self):
        """
        @brief Close the voting screen window.

        This method checks if the voting window is open and closes it if it exists.
        It sets the voting window attribute to None after closing.

        @return void
        """
        if self.voting_window:
            self.voting_window.destroy()
            self.voting_window = None

            
            
    def save_progress(self):
        """
        @brief Save the current progress, including players, features, rules, and collected votes, to a JSON file.

        This method prompts the user to choose a file path for saving the progress in JSON format.
        It includes information about players, features, rules, and collected votes in the saved data.

        @return void
        """
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


    def load_progress(self):
        """
        @brief Load a saved progress file, updating the state of the PlanningPokerGUI instance.

        This method prompts the user to choose a progress file in JSON format.
        It loads the data from the file, updating players, features, rules, and collected votes.

        @return void
        """
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

            
            self.update_players_label()
            self.update_features_label()
            self.update_rules_label()

            # Load collected votes
            self.votes = progress_data.get("votes", {})

            tk.messagebox.showinfo("Load Progress", "Progress loaded successfully.")

        self.update_features_label()
        self.update_rules_label()

    def update_features_label(self):
        # Update the label displaying features
        features_text = ", ".join(self.features)
        self.top_labels[2].config(text=f"Features: {features_text}")

    def update_rules_label(self):
        # Update the label displaying selected rules
        if self.rules:
            rules_text = f"Selected Rules: {self.rules.__class__.__name__}"
        else:
            rules_text = "Selected Rules: None"
        self.selected_rule_label.config(text=rules_text)



    def run(self):
        """
        @brief Run the Tkinter main loop.
    
        This method starts the Tkinter main loop, allowing the graphical user interface to function.
    
        @return void
        """
        self.root.mainloop()


if __name__ == "__main__":
    planning_poker_gui = PlanningPokerGUI()
    planning_poker_gui.run()

