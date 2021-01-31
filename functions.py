from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys
import datetime

# Google API auth


def googleAuth():

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "cred.json", scope)

    return gspread.authorize(creds)

# Get a single day´s macros information


def getSingle(clientName, inputDate, client, sheet):

    # Date must be split in order to make the API call
    date = inputDate.split("/")

    # Api call to get requested information
    data = client.get_date(date[0], date[1], date[2], username=clientName)

    calories = data.totals["calories"]
    proteins = data.totals["protein"]
    carbs = data.totals["carbohydrates"]
    fats = data.totals["fat"]

    # Insert a single row onto google spreadsheet with requested information
    # Value_input_otion very important to be used, otherwise google inserts a single quote at the start of our date, messing up google spreadsheet formulas
    sheet.insert_row([inputDate, calories, proteins, carbs, fats],
                     index=2, value_input_option="USER_ENTERED")

# Get macros for a user defined range of dates


def getRange(clientName, dateStart, dateEnd, client, sheet):

    # Format our dates strings to python readable date
    start = datetime.datetime.strptime(dateStart, "%Y/%m/%d")

    end = datetime.datetime.strptime(dateEnd, "%Y/%m/%d")

    # Check for input error
    if start >= end:
        errorAndExit(2)

    # Increase a day to our start date aka date += 1
    step = datetime.timedelta(days=1)

    # For each day in our date range, store daily macros in a list
    macrosList = list()

    # Loop through dates
    while start <= end:

        # Split date into year, month, day to make an API call - API requires date in this separate format
        day = start.day
        month = start.month
        year = start.year

        # Api call to get requested date
        data = client.get_date(year, month, day, username=clientName)

        # macros returned from API call
        calories = data.totals["calories"]
        proteins = data.totals["protein"]
        carbs = data.totals["carbohydrates"]
        fats = data.totals["fat"]

        # Format datetime object back to a string, otherwise we get JSON error
        formatedDate = start.strftime("%d/%m/%Y")

        # temporary list to be appended to our main list
        tempList = [formatedDate, calories, proteins, carbs, fats]

        # Append list to main list
        macrosList.append(tempList)

        # Increment date by one day
        start += step

    # Update excel sheet with requested date
    sheet.insert_rows(macrosList, row=2, value_input_option="USER_ENTERED")

# Verify proper usage

def validateInput(arguments):

    if len(arguments) < 2 or len(arguments) > 4:
        errorAndExit(1)

    if len(arguments) == 3:

        if len(arguments[2]) != 10:

            errorAndExit(1)
    else:
        if len(arguments[2]) != 10 and len(arguments[3]) != 10:

            errorAndExit(1)

# Prints various logs depending on their error log ID


def errorAndExit(errorLogId):

    if errorLogId == 1:
        print("Usage: python fitnesspal.py myfitnesspalUserName year/mm/dd year/mm/dd(optional)")
    elif errorLogId == 2:
        print("Incorrect usage, second date argument must older than first date argument")

    sys.exit()
