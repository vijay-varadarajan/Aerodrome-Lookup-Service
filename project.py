import pyttsx3
import string
import csv
from unidecode import unidecode
from signup import sign_up
from login import log_in
from voice import say
from tabulate import tabulate


engine = pyttsx3.init()
engine.setProperty('rate', 180)


def main():
    say("Welcome to Vijay's aerodrome lookup service")
    print("Welcome to Vijay's aerodrome lookup service")
    choice = "y"
    if authenticate():
        while "y" in choice:
            final_airports = search()
            print(tabulate(final_airports, headers="keys", tablefmt="psql"))
            say("Do you want me to read the names along with the type and gps codes?")
            if "y" in input(
                "Do you want me to read the names along with the type and gps codes?"
            ):
                for airport in final_airports:
                    say(airport['name'])
                    if airport['gps code']:
                        say(airport["gps code"])
                    else:
                        say("No gps code")
                    say(airport['type'].replace('_', ' '))
            say("Do you want to search again?")
            choice = input("Do you want to search again? ")

    say("Thank you. Do visit again !")
    print("Thank you. Do visit again !")


def authenticate():
    logged_in, signed_up = False, False

    while True:
        try:
            say("Enter 1 to login or 2 to signup")
            choice = int(input("Enter 1 to login, 2 to signup: "))
            if choice == 1:
                logged_in = log_in()
                break
            elif choice == 2:
                signed_up = sign_up()
                break
            else:
                print("Invalid choice, try again")
                say("Invalid choice, try again")
                continue
        except ValueError:
            say("Invalid choice. Try again. Press Ctrl+C to exit.")
            print("Invalid choice. Try again. Press Ctrl+C to exit.")
            continue

    if logged_in or signed_up:
        return True


def search():

    while True:
        try:
            say("Enter name of the country to search for aerodromes")
            country_name = (
                input("Enter name of the country to search for aerodromes: ")
                .strip()
                .lower()
                .replace(" ", "")
            )
            country_code, country_name = get_country_code(country_name)

            if not country_code:
                say("Country not found")
                print("Country not found")
                raise ValueError("Not found")
            break
        except ValueError:
            continue

    airport_count = get_airports_country(country_code)
    say(f"There are {airport_count} aerodromes in {country_name}.")
    print(f"There are {airport_count} aerodromes in {country_name}.")

    while True:
        try:
            say("Enter name of the state to search for aerodromes")
            region_name = (
                input("Enter name of the state to search for aerodromes: ")
                .strip()
                .lower()
                .replace(" ", "")
            )
            region_code, region_name = get_region_code(region_name, country_code)
            if not region_code:
                say("State not found")
                print("State not found")
                raise ValueError("Not found")
            break
        except ValueError:
            continue

    airport_count = get_airports_region(region_code)
    say(f"There are {airport_count} aerodromes in {region_name}.")
    print(f"There are {airport_count} aerodromes in {region_name}.")

    while True:
        try:
            say("Enter name of the city to search for aerodromes")
            municipality = (
                input("Enter the city to search for aerodromes: ")
                .strip()
                .lower()
                .replace(" ", "")
            )
            airports = get_airports_city(
                region_code, municipality
            )
            if not airports:
                say("City not found or no aerodromes found in given city")
                print("City not found / no aerodromes found in given city")
                raise ValueError("Not found")
            break
        except ValueError:
            continue

    airport_types = {
        "balloonport": 0,
        "heliport": 0,
        "small_airport": 0,
        "medium_airport": 0,
        "large_airport": 0,
        "seaplane_base": 0,
        "closed": 0,
    }
    for airport in airports:
        airport_types[airport["type"].strip().lower()] += 1

    none_count = 0
    print("There are")
    say("There are")
    for i in airport_types.keys():
        if airport_types[i] > 0:
            result = f"{airport_types[i]} {i.replace('_', ' ')}"
            if i == "closed":
                result += " airport"
            if airport_types[i] > 1:
                result += "s"
            print(result)
            say(result)
            continue
        none_count += 1
    if none_count == 7:
        print(f"no", end=" ")
    say(
        f"found in {municipality.capitalize()}, {region_name.capitalize() if region_name else ''}, {country_name.capitalize() if country_name else ''}."
    )
    print(
        f"found in {municipality.capitalize()}, {region_name.capitalize() if region_name else ''}, {country_name.capitalize() if country_name else ''}."
    )
    print()

    final_airports = []
    print_count = 0
    if none_count == 6:
        while True:
            try:
                say(
                    f"Do you want the list of {airports[0]['type'].replace('_', ' ')}s"
                )
                if "y" in str(input("Do you want the list? ")).strip().lower():
                    say(
                        f"The following are the {airports[0]['type'].replace('_', ' ')}s in {municipality},{region_name}"
                    )
                    final_airports = airports
                break
            except ValueError:
                continue
    else:
        while True:
            try:
                say(
                    "What type of airport are you searching for? (Enter 'all' to get all the names): "
                )
                airport_type = (
                    input(
                        "What type of airport are you searching for? (Enter 'all' to get all the names): "
                    )
                    .strip()
                    .lower()
                    .replace(" ", "")
                )
                if airport_type == "all":
                    final_airports = sorted(airports, key=lambda x: x["type"])
                    print_count += 1
                else:
                    print(f"{airport_type}:")
                    final_airports = []
                    for airport in airports:
                        if airport_type in airport["type"]:
                            final_airports.append(
                                {
                                    "name": airport["name"],
                                    "type": airport["type"],
                                    "gps code": airport["gps code"],
                                }
                            )

                    print_count += 1

                if print_count == 0:
                    say("Invalid type of airport. Try again")
                    print("Invalid type of airport. Try again")
                    raise ValueError("Invalid type of airport")
                break
            except ValueError:
                continue

    return final_airports


def get_airports_city(region_code, municipality):
    airport_list = []
    region_code, municipality = region_code.strip().upper(), municipality.strip().lower().replace(" ", '')

    with open("airports.csv", "r", errors="ignore") as airports:
        reader = csv.DictReader(airports)
        for row in reader:
            if row["iso_region"] == region_code.upper():
                if (
                    municipality.lower() in row["municipality"].lower()
                    or municipality.lower() in row["keywords"].lower()
                ):
                    airport_list.append(
                        {"name": row["name"], "type": row["type"], "gps code": row["gps_code"]}
                    )

    if not airport_list:
        return None
    
    return airport_list


def get_country_code(country_name):
    
    if len(country_name) == 2:
        with open("countries.csv", "r", errors="ignore") as countries:
            reader = csv.DictReader(countries)
            for row in reader:
                if unidecode(row["code"]) == country_name.upper():
                    return row["code"], row["name"]
                continue
    
    country_name = country_name.strip().lower().replace(" ", "")
    
    with open("countries.csv", "r", errors="ignore") as countries:
        reader = csv.DictReader(countries)

        for row in reader:
            if country_name == unidecode(row["name"]).lower().replace(" ", ""):
                return row["code"], row["name"]
            continue

    with open("countries.csv", "r", errors="ignore") as countries:
        reader = csv.DictReader(countries)
        for row in reader:
            if country_name in unidecode(row["keywords"]).lower().replace(" ", ""):
                return row["code"], row["name"]
            continue

    with open("countries.csv", "r", errors="ignore") as countries:
        reader = csv.DictReader(countries)
        for row in reader:
            if unidecode(row["name"]).lower().replace(" ", "") in country_name:
                return row["code"], row["name"]
            continue


    return None, None


def get_airports_country(country_code):

    airport_count = 0
    country_code = country_code.strip().upper().replace(" ", "")
    with open("airports.csv", "r", errors="ignore") as airports:
        reader = csv.DictReader(airports)
        for row in reader:
            if row["iso_country"] == country_code:
                airport_count += 1

    return airport_count


def get_region_code(region_name, country_code):
    region_name = region_name.strip().lower().replace(" ", "")
    with open("regions.csv", "r", errors="ignore") as airports:
        reader = csv.DictReader(airports)
        for row in reader:
            if (
                region_name.lower() in unidecode(row["name"]).lower().replace(" ", "")
                and row["iso_country"] == country_code.upper()
            ):
                return row["code"], row["name"]

    with open("regions.csv", "r", errors="ignore") as airports:
        reader = csv.DictReader(airports)
        for row in reader:
            if (
                region_name.lower() in unidecode(row["keywords"]).lower().replace(" ", "")
                and row["iso_country"] == country_code.upper()
            ):
                return row["code"], row["name"]

    with open("regions.csv", "r", errors="ignore") as airports:
        reader = csv.DictReader(airports)
        for row in reader:
            if (
                unidecode(row["name"]).lower().replace(" ", "") in region_name.lower()
                and row["iso_country"] == country_code.upper()
            ):
                return row["code"], row["name"]

    return None, None


def get_airports_region(region_code):

    airport_count = 0
    if region_code:
        with open("airports.csv", "r", errors="ignore") as airports:
            reader = csv.DictReader(airports)
            for row in reader:
                if row["iso_region"] == region_code.upper():
                    airport_count += 1

    return airport_count


if __name__ == "__main__":
    main()
