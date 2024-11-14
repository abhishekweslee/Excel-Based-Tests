import os.path
from datetime import datetime

class Paths:
    Log_dir = "Tests/test_outputs/logs"
    excel_path = "Tests/test_input"
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
        self.ticket_number = 0


    def save_details(self):
        # Automatically assign a ticket filename with an incremented number
        file_name = f"ticket{self.ticket_number}.txt"
        full_path = os.path.join(Paths.automatic_ticket_dir, file_name)

        # Display and save ticket details
        print("HERE IS BOOKED TICKET DETAILS...\n")
        print(
            f"Source: {self.src}\nDestination: {self.dest}\nDate: {self.d}\nName: {self.nm}\nAge: {self.age}\nPhone No: {self.ph}\n")

        with open(full_path, "w") as file:
            file.write(f"Source: {self.src}\n")
            file.write(f"Destination: {self.dest}\n")
            file.write(f"Date: {self.d}\n")
            file.write(f"Name: {self.nm}\n")
            file.write(f"Age: {self.age}\n")
            file.write(f"Phone Number: {self.ph}\n")

        print(f"Ticket details saved as {file_name}.")
        self.ticket_number += 1


    def save_as(self):
        file_name = input("Enter a filename to save the details: ")
        file_name = file_name + ".txt"
        full_path = os.path.join(Paths.ticket_dir,file_name)
        with open(full_path, "w") as file:
            file.write(f"Source: {self.src}\n")
            file.write(f"Destination: {self.dest}\n")
            file.write(f"Date: {self.d}\n")
            file.write(f"Name: {self.nm}\n")
            file.write(f"Age: {self.age}\n")
            file.write(f"Phone Number: {self.ph}\n")
            print(f"Details saved in {file_name}.")



