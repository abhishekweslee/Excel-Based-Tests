from datetime import datetime
import sys
from Core.dev.Common_opts import common

class BusTicketBooking(common):

    def home_page(self):
        print("**** WELCOME TO BUS TICKET BOOKING ****")

    def read_src(self):
        user_input = input(f"Enter source (default: {self.src}): ")
        if user_input:
            self.src = user_input
        return self.src

    def read_dest(self):
        user_input = input(f"Enter destination (default: {self.dest}): ")
        if user_input:
            self.dest = user_input
        return self.dest

    def read_name(self):
        user_input = input(f"Enter name (default: {self.nm}): ")
        if user_input:
            self.nm = user_input
        return self.nm

    def read_date(self):
        user_input = input(f"Enter travel date (YYYY-MM-DD, default: {self.d.strftime('%Y-%m-%d')}): ")
        if user_input:
            try:
                travel_date = datetime.strptime(user_input, '%Y-%m-%d')
                if travel_date < datetime.now():
                    print("Travel date cannot be in the past.")
                    return
                self.d = travel_date
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return self.d

    def read_age(self):
        try:
            user_input = input(f"Enter your age (default: {self.age}): ")
            if user_input:
                self.age = int(user_input)
                if self.age <= 0:
                    raise ValueError
        except ValueError:
            print("Invalid age. Please enter a positive integer.")
        return self.age

    def read_phone(self):
        user_input = input(f"Enter your phone number (default: {self.ph}): ")
        if user_input:
            if user_input.isdigit() and len(user_input) >= 10:
                self.ph = user_input
            else:
                print("Invalid phone number. It should contain at least 10 digits.")
        return self.ph

    def print_booking_details(self):
        return (
            f"Source: {self.src}\n"
            f"Destination: {self.dest}\n"
            f"Date: {self.d}\n"
            f"Name: {self.nm}\n"
            f"Age: {self.age}\n"
            f"Phone Number: {self.ph}"
        )

    def menu(self):
        print("\n--- Main Menu ---")
        print("1. Enter source")
        print("2. Enter destination")
        print("3. Save entered source and destination details")
        print("4. Save entered details to a file (Save As)")
        print("5. Back to home page")
        print("6. Go to Date and Name Entry menu")
        print("7. Go to Age and Phone Number Entry menu")
        print("8. Quit")

    def submenu1(self):
        print("\n--- Date and Name Entry ---")
        print("1. Enter travel date")
        print("2. Enter name")
        print("3. Save entered date and name")
        print("4. Save entered details to a file (Save As)")
        print("5. Back to main menu")
        print("6. Go to Age and Phone Number Entry menu")
        print("7. Quit")

    def submenu2(self):
        print("\n--- Age and Phone Number Entry ---")
        print("1. Enter age")
        print("2. Enter phone no.")
        print("3. Save entered age and phone no.")
        print("4. Save entered details to a file (Save As)")
        print("5. Back to main menu")
        print("6. Go to Date and Name Entry menu")
        print("7. Quit")

    def run(self):
        self.home_page()
        current_menu = 'main'
        path = ["Main Menu"]

        while True:
            if current_menu == 'main':
                self.menu()
                choice = input("Select an option: ")

                if choice == '1':
                    self.read_src()
                elif choice == '2':
                    self.read_dest()
                elif choice == '3':
                    self.save_details()
                elif choice == '4':
                    self.save_as()
                elif choice == '5':
                    path = ["Main Menu"]
                elif choice == '6':
                    current_menu = 'date_name'
                    path = ["Main Menu", "Date and Name Entry"]
                elif choice == '7':
                    current_menu = 'age_phno'
                    path = ["Main Menu", "Age and Phone Number Entry"]
                elif choice == '8':
                    print("Exiting the application...")
                    sys.exit(0)
                else:
                    print("Invalid option. Please try again.")

            elif current_menu == 'date_name':
                self.submenu1()
                sub_choice = input("Select an option: ")

                if sub_choice == '1':
                    self.read_date()
                elif sub_choice == '2':
                    self.read_name()
                elif sub_choice == '3':
                    self.save_details()
                elif sub_choice == '4':
                    self.save_as()
                elif sub_choice == '5':
                    current_menu = 'main'
                    path = ["Main Menu"]
                elif sub_choice == '6':
                    current_menu = 'age_phno'
                    path = ["Main Menu", "Age and Phone Number Entry"]
                elif sub_choice == '7':
                    print("Exiting the application...")
                    sys.exit(0)
                else:
                    print("Invalid option. Please try again.")

            elif current_menu == 'age_phno':
                self.submenu2()
                sub_choice = input("Select an option: ")

                if sub_choice == '1':
                    self.read_age()
                elif sub_choice == '2':
                    self.read_phone()
                elif sub_choice == '3':
                    self.save_details()
                elif sub_choice == '4':
                    self.save_as()
                elif sub_choice == '5':
                    current_menu = 'main'
                    path = ["Main Menu"]
                elif sub_choice == '6':
                    current_menu = 'date_name'
                    path = ["Main Menu", "Date and Name Entry"]
                elif sub_choice == '7':
                    print("Exiting the application...")
                    sys.exit(0)
                else:
                    print("Invalid option. Please try again.")

if __name__ == "__main__":
    booking = BusTicketBooking()
    booking.run()
