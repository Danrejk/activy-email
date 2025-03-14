import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import Image, ImageTk
import io


class AccountListComponent(ttk.Frame):
    def __init__(self, parent, db_handler, max_width=800, height=500,
                 middle_width=200, right_width=200, left_min_width=300,
                 row_height=120):
        """
        Create an account list component with fixed column widths and row heights.

        Parameters:
        - parent: parent tkinter widget
        - db_handler: database handler instance
        - max_width: maximum width of the component (default: 800)
        - height: height of the component (default: 500)
        - middle_width: fixed width for the middle section (default: 200)
        - right_width: fixed width for the right section (default: 200)
        - left_min_width: minimum width for the left section (default: 300)
        - row_height: height for each account row (default: 120)
        """
        super().__init__(parent)
        self.db_handler = db_handler
        self.max_width = max_width
        self.height = height
        self.middle_width = middle_width
        self.right_width = right_width
        self.left_min_width = left_min_width
        self.row_height = row_height

        # Create the UI structure
        self.create_widgets()

    def create_widgets(self):
        # Create outer frame with fixed dimensions
        self.outer_frame = ttk.Frame(self, width=self.max_width, height=self.height)
        self.outer_frame.pack(fill="both", expand=True)
        self.outer_frame.pack_propagate(False)  # Prevent resizing

        # Create a scrollable canvas
        self.canvas = tk.Canvas(self.outer_frame)
        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.max_width - 20)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Configure grid layout
        self.outer_frame.columnconfigure(0, weight=1)
        self.outer_frame.rowconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Load accounts
        self.load_accounts()

    def load_accounts(self):
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get all accounts from database
        accounts = self.db_handler.getAllAccounts()

        # Create a display for each account
        for account in accounts:
            self.create_account_row(account)

    def create_account_row(self, account):
        # Create a frame for this account with fixed height
        account_frame = ttk.Frame(self.scrollable_frame, height=self.row_height)
        account_frame.pack(fill="x", padx=5, pady=5)
        account_frame.pack_propagate(False)  # Prevent the frame from shrinking

        # Use fixed widths for each section
        available_width = self.max_width - 20  # Account for scrollbar and padding

        # Left section (expandable with min width)
        left_frame = self.create_left_section(account_frame, account)
        left_frame.place(x=0, y=0, height=self.row_height - 10, width=self.left_min_width)

        # Middle section (fixed width)
        middle_frame = self.create_middle_section(account_frame, account)
        middle_frame.place(x=self.left_min_width, y=0, height=self.row_height - 10, width=self.middle_width)

        # Right section (fixed width)
        right_frame = self.create_right_section(account_frame, account)
        right_frame.place(x=self.left_min_width + self.middle_width, y=0, height=self.row_height - 10,
                          width=self.right_width)

        # Add separator after each account
        ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=2)

    def create_left_section(self, parent, account):
        left_frame = ttk.Frame(parent)

        # Profile picture
        avatar_frame = ttk.Frame(left_frame, width=80, height=80)
        avatar_frame.pack(side="left", padx=(10, 20), pady=10)
        avatar_frame.pack_propagate(False)  # Maintain size

        # Create avatar image
        if account.get('avatar'):
            try:
                # Convert blob to image
                pil_image = self.blob_to_image(account['avatar'])
                # Resize to fit the avatar area
                pil_image = pil_image.resize((80, 80), Image.LANCZOS)
                # Convert to PhotoImage for Tkinter
                tk_image = ImageTk.PhotoImage(pil_image)

                # Display avatar
                avatar_label = ttk.Label(avatar_frame, image=tk_image)
                avatar_label.image = tk_image  # Keep reference
                avatar_label.pack(fill="both", expand=True)
            except Exception as e:
                print(f"Error loading avatar: {e}")
                self.create_default_avatar(avatar_frame)
        else:
            self.create_default_avatar(avatar_frame)

        # User info
        info_frame = ttk.Frame(left_frame)
        info_frame.pack(side="left", fill="both", expand=True, pady=10)

        # Nickname
        nickname_label = ttk.Label(info_frame, text=account['username'], font=("Arial", 12, "bold"))
        nickname_label.pack(anchor="w", pady=(5, 2))

        # Name and surname
        name_label = ttk.Label(info_frame,
                               text=f"{account['name']} {account['surname']}",
                               font=("Arial", 10))
        name_label.pack(anchor="w", pady=2)

        # Email
        email_label = ttk.Label(info_frame, text=account['email'], font=("Arial", 9))
        email_label.pack(anchor="w", pady=2)

        return left_frame

    def create_middle_section(self, parent, account):
        middle_frame = ttk.Frame(parent)

        # Create a vertical container for the three elements
        container = ttk.Frame(middle_frame)
        container.pack(expand=True, pady=15)

        # Get location data
        home_data = self.db_handler.getPlaceById(account['homeId'])
        workplace_data = self.db_handler.getPlaceById(account['workplaceId'])

        # Home location
        home_label = ttk.Label(container, text=home_data['name'], font=("Arial", 9))
        home_label.pack(pady=(0, 2))  # Reduced padding between elements

        # Double arrow
        arrow_label = ttk.Label(container, text="<->", font=("Arial", 9, "bold"))
        arrow_label.pack(pady=2)  # Reduced padding between elements

        # Workplace
        workplace_label = ttk.Label(container, text=workplace_data['name'], font=("Arial", 9))
        workplace_label.pack(pady=(2, 0))  # Reduced padding between elements

        return middle_frame

    def create_right_section(self, parent, account):
        right_frame = ttk.Frame(parent)

        # Get challenge data
        challenge_data = self.db_handler.getChallengeById(account['challengeId'])

        # Container for right content
        container = ttk.Frame(right_frame)
        container.pack(expand=True, pady=15, padx=10, anchor="e")

        # Points with "ptk" suffix
        points_label = ttk.Label(container, text=f"{account['points']}ptk", font=("Arial", 16, "bold"))
        points_label.pack(anchor="e", pady=(0, 5))

        # Description
        challenge_name = challenge_data['name']

        # Create a multiline label that wraps
        challenge_label = ttk.Label(
            container,
            text=challenge_name,
            font=("Arial", 9),
            wraplength=self.right_width - 30  # Allow wrapping with some padding
        )
        challenge_label.pack(anchor="e")

        return right_frame

    def create_default_avatar(self, frame):
        # Create a default avatar placeholder
        canvas = tk.Canvas(frame, width=80, height=80, bg="#2a2a2a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Add a simple user icon
        canvas.create_oval(20, 15, 60, 45, fill="#555555", outline="")
        canvas.create_oval(30, 50, 50, 70, fill="#555555", outline="")

    def blob_to_image(self, blob_data):
        """Convert binary blob data to PIL Image"""
        return Image.open(io.BytesIO(blob_data))


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Account List Component")
    root.geometry("800x500")

    # Apply theme
    sv_ttk.set_theme("dark")

    # Create database handler
    from src.database.dbHandler import dbHandler

    db = dbHandler("uiActivy.db")

    # Create account list component
    account_list = AccountListComponent(
        root,
        db,
        max_width=800,
        middle_width=200,
        right_width=150,
        left_min_width=300,
        row_height=120
    )
    account_list.pack(fill="both", expand=True, padx=10, pady=10)

    # Run the application
    root.mainloop()

    # Close database connection
    db.closeConnection()