
from datetime import datetime


def ask_user_input():
    while True:
        try:
            max_results = int(input("Enter the maximum number of results to scrape (default 5): ") or 5)
            if max_results <= 0:
                raise ValueError("Maximum results must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    while True:
        availability_start = input("Enter the start date for availability filter (default 01/01/2025, format DD/MM/YYYY): ") or "01/01/2025"
        if validate_date(availability_start):
            break
        else:
            print("Invalid date format. Please use DD/MM/YYYY.")

    while True:
        availability_end = input("Enter the end date for availability filter (default 31/12/2025, format DD/MM/YYYY): ") or "31/12/2025"
        if validate_date(availability_end):
            break
        else:
            print("Invalid date format. Please use DD/MM/YYYY.")

    medical_request = input("Enter the type of medical professional to search for (default medecin-generaliste): ") or "medecin-generaliste"
    insurance_type = input("Enter the type of insurance coverage (default secteur 1): ") or "secteur 1"
    consultation_type = input("Enter the type of consultation (e.g., in-person or teleconsultation, default in-person): ") or "in-person"

    while True:
        try:
            price_min = int(input("Enter the minimum price for consultation (default 50): ") or 50)
            if price_min < 0:
                raise ValueError("Price must be a non-negative integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    while True:
        try:
            price_max = int(input("Enter the maximum price for consultation (default 150): ") or 150)
            if price_max < price_min:
                raise ValueError("Maximum price must be greater than or equal to minimum price.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    geographical_filter = input("Enter the geographical location to filter results (default Paris): ") or "Paris"

    return {
        "max_results": max_results,
        "availability_start": availability_start,
        "availability_end": availability_end,
        "medical_request": medical_request,
        "insurance_type": insurance_type,
        "consultation_type": consultation_type,
        "price_min": price_min,
        "price_max": price_max,
        "geographical_filter": geographical_filter,
    }

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Ask the user for input
user_input = ask_user_input()


