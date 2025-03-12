import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import Image, ImageTk
from src.database.dbHandler import dbHandler
from src.database.utils.imageBlobHandling import blobToImage, imageToBlob


class AccountListFrame(ttk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the account list with scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
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

        # Set up header
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(header_frame, text="User Information", font=("TkDefaultFont", 12, "bold")).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Points", font=("TkDefaultFont", 12, "bold")).pack(side="right", padx=5)

        # Separator
        ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=5)

        # Display each account
        for account in accounts:
            self._create_account_item(account)

    def _create_account_item(self, account):
        # Create a frame for the account
        account_frame = ttk.Frame(self.scrollable_frame)
        account_frame.pack(fill="x", padx=10, pady=10)

        # Left part: Avatar
        avatar_frame = ttk.Frame(account_frame, width=60, height=60)
        avatar_frame.pack(side="left", padx=10)

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

        # Middle part: User info
        info_frame = ttk.Frame(account_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Username (nickname)
        username_label = ttk.Label(info_frame, text=account['username'], font=("TkDefaultFont", 11, "bold"))
        username_label.pack(anchor="w")

        # Email, name and surname (smaller font)
        full_name = f"{account['name']} {account['surname']}"
        name_label = ttk.Label(info_frame, text=full_name, font=("TkDefaultFont", 9))
        name_label.pack(anchor="w")

        email_label = ttk.Label(info_frame, text=account['email'], font=("TkDefaultFont", 9))
        email_label.pack(anchor="w")

        # Right part: Points and workplace
        right_frame = ttk.Frame(account_frame)
        right_frame.pack(side="right", padx=10)

        # Points
        points_label = ttk.Label(right_frame, text=f"{account['points']} pts", font=("TkDefaultFont", 12, "bold"))
        points_label.pack(anchor="e")

        # Workplace
        workplace = self.db_handler.getPlaceById(account['workplaceId'])
        if workplace:
            workplace_name = workplace['name']
            workplace_label = ttk.Label(right_frame, text=f"Works at: {workplace_name}", font=("TkDefaultFont", 9))
            workplace_label.pack(anchor="e")

        # Add a separator after each account
        ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=5)


# Example usage:
if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    root.title("Accounts List")
    root.geometry("600x500")

    # Apply theme
    sv_ttk.set_theme("dark")

    # Create database handler
    db = dbHandler("uiActivy.db")
    db.createTables()
    db.createPlace("ZETESEL LACZNOSCIBOMBA W LACZNOSCSŁ", 52.407, 16.934, True)
    image = imageToBlob("zvekon.png")
    # db.createPlace("Most Siennicki", 52.407, 16.934, False)
    db.createAccount("Max", "Sobolewski", "Zvekogffhdfsuidffyudsdsfdsfydsfsdfdsffdsyun", "zvekosjdsuhuadyasuidyasuidasuidyasdasuduadsydasngaming@gmail.com", "1234", 1, 1, 3, avatar=image)

    # Create and display the accounts list
    accounts_frame = AccountListFrame(root, db)
    accounts_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Run the application
    root.mainloop()

    # Close database connection when done
    db.closeConnection()