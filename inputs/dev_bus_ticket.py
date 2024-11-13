import pandas as pd
from datetime import datetime
# Function to read data from Excel


def read_date():
    date = input("Enter travel date (YYYY-MM-DD): ")
    try:
        travel_date = datetime.strptime(date, '%Y-%m-%d')
        if travel_date < datetime.now():
            print("Travel date cannot be in the past.")
            return
    except ValueError:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return
    return date


def read_age():
    # Validate age input
    try:
        age = int(input("Enter your age: "))
        if age <= 0:
            raise ValueError
    except ValueError:
        print("Invalid age. Please enter a positive integer.")
    return age

def read_phone():
    phone = input("Enter your phone number: ")

    # Simple phone number validation
    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number. It should contain at least 10 digits.")
        return
    return phone



def read_excel_data(file_path):
    df = pd.read_excel(file_path)
    return df


# Function to print details
def print_booking_details(src, dest, name, date, age, phone_no):
    print("\nBooking Details:")
    print(f"Source: {src}")
    print(f"Destination: {dest}")
    print(f"Name: {name}")
    print(f"Date: {date}")
    print(f"Age: {age}")
    print(f"Phone Number: {phone_no}")


# Main function
def main():
    while True:
        print("\n--- Bus Ticket Booking ---")
        print("1. Enter source")
        print("2. Enter destination")
        print("3. Enter Date")
        print("4. Enter name")
        print("5. Enter age")
        print("6. Enter phone number")
        print("7. Done")

        choice = input("Select an option between 1 to 7 : ")

        if choice== '1':
            src = input("Enter source: ")
        elif choice== '2':
            dest = input("Enter destination: ")
        elif choice == '3':
            d = read_date()
        elif choice == '4':
            name = input("Enter name: ")
        elif choice == '5':
            age = read_age()
        elif choice == '6':
            ph = read_phone()
        elif choice == '7':
            print_booking_details(src,dest,d,name,age,ph)
            exit()






if __name__ == "__main__":
    main()
