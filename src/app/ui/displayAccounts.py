import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import Image, ImageTk
from src.database.dbHandler import dbHandler
from src.database.utils.imageBlobHandling import blobToImage


class AccountListFrame(ttk.Frame):
    def __init__(self, parent, db_handler, max_width=600, info_ratio=0.7):
        """
        Create an account list frame with configurable width and ratio

        Parameters:
        - parent: parent tkinter widget
        - db_handler: database handler instance
        - max_width: maximum width of the account list (default: 600)
        - info_ratio: ratio of width allocated to user info vs points section (default: 0.7)
        """
        super().__init__(parent)
        self.db_handler = db_handler
        self.max_width = max_width
        self.info_ratio = info_ratio

        # Define the width proportions
        self.avatar_width = 80  # Fixed width for avatar section

        # Create the UI
        self.create_widgets()

    def truncate_text(self, text, max_chars):
        """Truncate text and add ellipsis if longer than max_chars"""
        if len(text) > max_chars:
            return text[:max_chars - 3] + "..."
        return text

    def create_widgets(self):
        # Create a frame with fixed width
        self.outer_frame = ttk.Frame(self, width=self.max_width)
        self.outer_frame.pack(fill="both", expand=True)
        self.outer_frame.pack_propagate(False)  # Prevent resizing

        # Create a frame for the account list with scrollbar
        self.canvas = tk.Canvas(self.outer_frame, width=self.max_width - 20)
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

        # Load and display accounts
        self.load_accounts()

    def load_accounts(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get all accounts
        accounts = self.db_handler.getAllAccounts()

        # Calculate widths based on ratios
        content_width = self.max_width - 20  # Account for padding
        info_width = int((content_width - self.avatar_width) * self.info_ratio)
        points_width = content_width - self.avatar_width - info_width

        # Set up header
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(header_frame, text="User Information", font=("TkDefaultFont", 12, "bold")).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Points", font=("TkDefaultFont", 12, "bold")).pack(side="right", padx=5)

        # Separator
        ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=5)

        # Display each account
        for account in accounts:
            self._create_account_item(account, info_width, points_width)

    def _create_account_item(self, account, info_width, points_width):
        # Create a frame for the account with fixed width
        account_frame = ttk.Frame(self.scrollable_frame)
        account_frame.pack(fill="x", padx=10, pady=10)

        # Left part: Avatar
        avatar_frame = ttk.Frame(account_frame, width=60, height=60)
        avatar_frame.pack(side="left", padx=10)
        avatar_frame.pack_propagate(False)  # Maintain size

        # Create a default blank avatar
        avatar_canvas = tk.Canvas(avatar_frame, width=60, height=60, bg="#2a2a2a", highlightthickness=0)
        avatar_canvas.pack(fill="both", expand=True)

        # If avatar exists, display it
        if account.get('avatar'):
            try:
                # Convert blob to image
                pil_image = blobToImage(account['avatar'])
                # Resize to fit the avatar area
                pil_image = pil_image.resize((60, 60), Image.LANCZOS)
                # Convert to PhotoImage for Tkinter
                tk_image = ImageTk.PhotoImage(pil_image)
                # Store reference to prevent garbage collection
                avatar_canvas.image = tk_image
                # Display on canvas
                avatar_canvas.create_image(30, 30, image=tk_image)
            except Exception as e:
                print(f"Error loading avatar for {account['username']}: {e}")

        # Middle part: User info (with fixed width)
        info_frame = ttk.Frame(account_frame, width=info_width)
        info_frame.pack(side="left", fill="y", padx=10)
        info_frame.pack_propagate(False)  # Prevent resizing

        # Calculate max characters based on width (approximate)
        max_chars_username = info_width // 8  # Bold text takes more space
        max_chars_details = info_width // 6  # Smaller font

        # Username (nickname) - truncated
        username_text = self.truncate_text(account['username'], max_chars_username)
        username_label = ttk.Label(info_frame, text=username_text, font=("TkDefaultFont", 11, "bold"))
        username_label.pack(anchor="w")

        # Full name - truncated
        full_name = f"{account['name']} {account['surname']}"
        full_name_text = self.truncate_text(full_name, max_chars_details)
        name_label = ttk.Label(info_frame, text=full_name_text, font=("TkDefaultFont", 9))
        name_label.pack(anchor="w")

        # Email - truncated
        email_text = self.truncate_text(account['email'], max_chars_details)
        email_label = ttk.Label(info_frame, text=email_text, font=("TkDefaultFont", 9))
        email_label.pack(anchor="w")

        # Right part: Points and workplace (with fixed width)
        right_frame = ttk.Frame(account_frame, width=points_width)
        right_frame.pack(side="right", fill="y", padx=10)
        right_frame.pack_propagate(False)  # Prevent resizing

        # Points
        points_label = ttk.Label(right_frame, text=f"{account['points']} pts", font=("TkDefaultFont", 12, "bold"))
        points_label.pack(anchor="e")

        # Workplace with truncation
        workplace = self.db_handler.getPlaceById(account['workplaceId'])
        if workplace:
            workplace_name = workplace['name']
            max_chars_workplace = points_width // 6
            workplace_text = f"Works at: {self.truncate_text(workplace_name, max_chars_workplace - 10)}"
            workplace_label = ttk.Label(right_frame, text=workplace_text, font=("TkDefaultFont", 9))
            workplace_label.pack(anchor="e")

        # Add a separator after each account
        ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=5)


# Example usage:
if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    root.title("Accounts List")
    root.geometry("700x500")

    # Apply theme
    sv_ttk.set_theme("dark")

    # Create database handler
    db = dbHandler("uiActivy.db")

    # Create and display the accounts list with custom width and ratio
    accounts_frame = AccountListFrame(
        root,
        db,
        max_width=450,  # Set maximum width to 650 pixels
        info_ratio=0.75  # Allocate 75% of space to user info, 25% to points section
    )
    accounts_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Run the application
    root.mainloop()

    # Close database connection when done
    db.closeConnection()