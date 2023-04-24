# AERODROME LOOKUP SOFTWARE

### by **Vijay Varadarajan**
### from **Chennai, TamilNadu, India**

#### Video Demo: [Aerodrome_lookup_demo-video](https://www.youtube.com/watch?v=0_bQLJsMIWE)
#### Github Repo link: [Aerodrome_lookup_source-code](https://github.com/vijay-varadarajan/CS50p_FINAL_PROJECT)

## About this project

This is my final project for **CS50p**. This software displays via text and voice the names and gps codes of all the aerodromes found in a specific location given by the user. This is useful when a person wants to lookup the various aerodromes such as airports, heliports, seaplane bases and more in a particular location. 

## Features of this software

### This software encompasses the following features : 
 
 - Requirement of **logging in** / **signing up** before searching.
 
 - **Password masking** with **_'*'_** while typing.
 
 - Password **encryption** and **decryption** while storing and checking.
 
 - Prevention of duplicate usernames.
 
 - Displays not only the airports but also the **heliports, seaplane bases, balloonports** and any other type of aerodromes in a particular location.
 
 - Also displays the **different types of airports** such as small, medium and large airports, along with their gps codes (if available).
 
 - After logging in once, a user can make **any number of searches** one after the other, but is **logged out automatically** once the program terminates.

 - Display of output in a **tabulated format** with the type of aerodrome and gps code against each name for easy visualization.

 - The **cowsay** library is used to provide a visual treat to the user.
 
 - **The output data is displayed via text as well as audio (voice) giving the user a more immersive search experience. This also allows the blind to make use of this software.**

## New concepts

### I learnt the following new concepts and used them in this project :

 1. The various features offered by the python's text-to-speech library **_pyttsx3_**.

 2. Use of the **_pyttsx3 engine_** to convert the output text to speech and also modifying the rate of speech.

 3. The masking of password while typing in the terminal window using the **_pwinput_** library.
 
 4. Writing my own simple **_encryption and decryption formulas_** to store and check passwords.

 5. Handling csv files that are **_not in UTF-8_** formatting and avoiding error messages while reading the same.
 
 6. Use of **_unidecode_** to decode texts that have accents in them, converting them back to normal text.

## Implementation details

<details>

<summary><b>Libraries used</b></summary>

 - csv
 - string
 - cowsay
 - pwinput
 - pyttsx3
 - tabulate
 - unidecode

</details>

The pip install libraries required for this project are mentioned above as well as in **_requirements.txt_**. When the program is executed, the required libraries are imported and the engine for **_pyttsx3_** (text-to-speech) is initialised. **_pyttsx3_** is a text-to-speech conversion library in Python. Unlike alternative libraries, it works offline and allows customisations in the voice's characteristics. 

```python
engine = pyttsx3.init()
engine.setProperty('rate', 180)
```

Then, the **_authenticate()_** function is called which gives the user the option to either login or sign up. 

```python
if choice == 1:
    logged_in = log_in()
    break
elif choice == 2:
    signed_up = sign_up()
    break
```

If the user wants to sign up, the **_sign\_up()_** function is called, the definition of which is written in a seperate file named **_signup.py_**. This function first calls the **_get\_signup\_data()_** function to get the credentials of the user. This **_get\_signup\_data()_** function requests for the username and password, followed by password confirmation each of which is asked repeatedly until a valid input is obtained from the user. The username is checked against previously stored usernames and is considered invalid if it matches with one. The passwords are masked with **_'*'_** during input and are required to have atleast two letters, two numbers and one special character. 

```python
password = pwinput.pwinput(prompt="Password: ", mask="*")
```

The confirmation password is checked against password to make sure they match. After obtaining valid user credentials, the **_upload\_signup\_data()_** function is called which encrypts the password and stores it along with the username in **_users.csv_**. 

```python
with open("users.csv", "a") as users:
    fields = [username, password]
    writer = csv.DictWriter(users, fieldnames=fields)
    writer.writerow(
        {username: username, password: encrypt_password(username, password)}
    )
```

When the user wants to login, the **_log\_in()_** function is called, the definition of which is coded in **_login.py_**. This accepts as input the username and password and checks it against each row of username and password, calling the respective functions. The password is again masked with **_'*'_** during input and while checking, the encrypted version of the password is decrypted using the inverse of the encryption algorithm. If the user enters the wrong password for more than 3 times, he/she is given the option to sign up. 

```python
if wrong_pass > 3:
    say("Do you want to sign up?")
    choice = input("Do you want to sign up [y/n]? ").strip().lower()
    if "y" in choice:
        sign_up()
        break
```

When the credentials of one row match with entered credentials, the login is considered valid.

The algorithms used for encryption and decryption of the password were written by myself and though the algorithms are simple, they are effective in encrypting and decrypting the passwords.

The voice characteristics of the audio are set in **_voice.py_** and the function say is defined in the same file. This function contains the code that outputs the audio for whichever text is given as argument. 

```python
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 180)
def say(sentence):
    engine.say(f"{sentence}")
    engine.runAndWait()
```

This function is imported into **_project.py_**, that outputs the audio for every displayed text, taking the user experience up a notch. After successful login or signup, the **_search()_** function is called which searches for aerodromes based on the details entered by the user. 

```python
final_airports = search()
```

The user is prompted for the name of the country and a function is called to get the country code. The country code is a unique two-letter code given for each country, which is stored in **_countries.csv_**. This function searches various fields: code, name, keywords to obtain the code of the desired country form the csv file. **_Unidecode()_** helps in converting accented text back to **UTF-8** format for effective searching. If no country code is obtained the user is prompted again, with an error message, for a valid country name.

Using the obtained country code, the number of airports in that country is displayed by counting the airports whose country code matches, from **_airports.csv_**. Then same is conveyed by voice as well.

```python
airport_count = 0
with open("airports.csv", "r", errors="ignore") as airports:
    reader = csv.DictReader(airports)
    for row in reader:
        if row["iso_country"] == country_code:
            airport_count += 1

return airport_count
```

The user is now prompted to enter the specific state to search for and the state code is searched for in **_regions.csv_** by **_get\_region\_code()_**. If that state is not available or belongs to a wrong country, the user is prompted again for a valid state name. The total number of airports in that state is counted and displayed via text and audio using the **_get\_airports\_region()_** function.

```python
airport_count = get_airports_region(region_code)
say(f"There are {airport_count} aerodromes in {region_name}.")
print(f"There are {airport_count} aerodromes in {region_name}.")
```

Then, the city required is asked for from the user and the aerodromes are searched for using the region code and city name **_get\_airports\_city()_**. The required data of the airports are stored as a list of dictionaries. The count of the different types of airports are also recorded and displayed via text along with its audio output.

The user is asked to specify which type of airport to display or all of the available types based on which the required airport data: **name, type, gps code** is stored in a list of dictionaries. This list is returned and is displayed in a neatly formatted and tabulated manner using **_tabulate()_**, based on the user's needs. The user is allowed to decide if he/she wants the names to be read. 

```python
print(tabulate(final_airports, headers="keys", tablefmt="psql"))
```

I decided to split this progam into several different functions and also separate files, each performing separate tasks instead of clumping them together in one file or function as this makes the code very easy to handle, while coding as well as debugging. Also, this makes the source code easier to understand.

Finally, the user can choose to perform another search again which runs the search function once again or to exit the program which logs the user out, with a kitty thanking the user.

## External resources

The real-world datasets of the aerodromes and the country and region codes were obtained from: [OpenData](https://ourairports.com/data/)

The csv files used in this project can be downloaded using the following links: 
- [Airports](https://davidmegginson.github.io/ourairports-data/airports.csv)
- [Countries](https://davidmegginson.github.io/ourairports-data/countries.csv)
- [Regions](https://davidmegginson.github.io/ourairports-data/regions.csv)

<details>

<summary><b>Web references</b></summary> 

 - [_csv_](https://docs.python.org/3/library/csv.html)
 - [_cowsay_](https://pypi.org/project/cowsay/)
 - [_pyttsx3_](https://pypi.org/project/pyttsx3/)
 - [_unidecode_](https://pypi.org/project/Unidecode/)
 - [_tabulate_](https://pypi.org/project/tabulate/)
 - [_pwinput_](https://pypi.org/project/pwinput/)
 - [_markdown_](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/basic-writing-and-formatting-syntax)

</details>

## Future improvements

### I plan to improve this software in the following ways: 

 - Adding more flexiblity to the search allowing the user to view the more than one type of airports, instead of just one or all of them. 

 - Adding the feature of performing the reverse of this search, i.e finding the location when given the airport name.

 - Storing the user's own location during sign up, to let them search quickly for airports in their location.

 - Storing the user's search history in their own accounts and letting them view the same anytime later.
