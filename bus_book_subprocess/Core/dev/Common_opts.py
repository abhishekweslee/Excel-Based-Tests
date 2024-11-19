import os.path
from datetime import datetime

class Paths:
    Log_dir = "Tests/test_outputs/logs"
    excel_path = "Tests/test_inputs/Ticket_booking.xlsx"
    ticket_dir = "Tests/test_outputs/tickets/user_generated_tickets"
    automatic_ticket_dir = "Tests/test_outputs/tickets/output_tickets"

class common:
    def __init__(self):
        # Initialize default values
        self.src = 'default-Hyderabad'
        self.dest = 'default-Pithapuram'
        self.d = datetime.now()
        self.nm = 'default-ram'
        self.age = 20
        self.ph = 'default-1234567890'
        self.ticket_number = self.get_last_ticket_number()
        self.saved = False
        self.current_version = 0

    def get_last_ticket_number(self):
        """Read the last ticket number from a file."""
        try:
            with open("Tests/test_outputs/tickets/last_ticket_number.txt", "r") as file:
                return int(file.read().strip())  # Read and return the number
        except (FileNotFoundError, ValueError):
            return 0

    def update_last_ticket_number(self):
        """Update the last ticket number to a file."""
        with open("Tests/test_outputs/tickets/last_ticket_number.txt", "w") as file:
            file.write(str(self.ticket_number))

    def save_details(self):
        if self.saved:
            print("Details are already saved. No need to save again.")
            return

        # Generate a new file name using the incremented ticket number
        base_file_name = f"ticket{self.ticket_number}"
        file_name = f"{base_file_name}.txt"
        full_path = os.path.join(Paths.automatic_ticket_dir, file_name)

        # Display and save ticket details
        print("HERE IS BOOKED TICKET DETAILS...\n")
        print(
            f"Source: {self.src}\nDestination: {self.dest}\nDate: {self.d}\nName: {self.nm}\nAge: {self.age}\nPhone No: {self.ph}\n"
        )

        # Save ticket details to the file
        with open(full_path, "w") as file:
            file.write(f"Source: {self.src}\n")
            file.write(f"Destination: {self.dest}\n")
            file.write(f"Date: {self.d}\n")
            file.write(f"Name: {self.nm}\n")
            file.write(f"Age: {self.age}\n")
            file.write(f"Phone Number: {self.ph}\n")

        print(f"Ticket details saved as {os.path.basename(full_path)}.")

        # Increment the ticket number after saving
        self.ticket_number += 1  # Increment the ticket number
        self.update_last_ticket_number()

        # Set the saved flag to True to indicate successful save
        self.saved = True

    def save_as(self):
        # Ask the user for the filename
        file_name = input("Enter a filename to save the details: ")
        file_name = file_name + ".txt"
        full_path = os.path.join(Paths.ticket_dir, file_name)

        # Check if the file already exists
        if os.path.exists(full_path):
            print(f"Error: A ticket with the name '{file_name}' already exists.")
            return  # Exit the method without saving

        # Write the ticket details to the file
        with open(full_path, "w") as file:
            file.write(f"Source: {self.src}\n")
            file.write(f"Destination: {self.dest}\n")
            file.write(f"Date: {self.d}\n")
            file.write(f"Name: {self.nm}\n")
            file.write(f"Age: {self.age}\n")
            file.write(f"Phone Number: {self.ph}\n")

        print(f"Details saved in {file_name}.")


