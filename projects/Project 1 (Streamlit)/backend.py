# Programmer: Mohamed Salah
# I have imported and merged every function that were frequently used. 

import pandas as pd
import os
import uuid
from datetime import datetime
from IPython.display import display

file_csv = 'plants.csv'
photos_csv = 'plant_photos.csv'
care_history_file = "care_history.csv"
headers = ['Plant_id', 'Plant name','Location','Date Acquired','Water Frequency (in days)', 'Sunlight needs']

def load_plants():
    """
    Programmer: Meqdad Muhana
    Desc.: Using Pandas, loads data from the csv.
    """
    if not os.path.exists(file_csv):
        return pd.DataFrame(columns = headers)
    else:
        return pd.read_csv(file_csv)



def add_new_plant():
    """
    Programmer: Meqdad Muhana
    Desc.: The user will enter the data to add them in the csv.
    """
    print('Enter the details nedded to add plant: ')
    Plant_id = str(uuid.uuid4())
    name = input('The plant name/species is: ').strip()
    location = input('The plant location in home is: ').strip()
    while True:
        date_acq = input('The plant date acquired (please use the form "YYYY-MM-DD"): ').strip()
        if not date_acq:
            date_acq = datetime.now().strftime("%Y-%m-%d")
            break
        try:
            parsed_date = pd.to_datetime(date_acq)
        except (ValueError, TypeError):
            print('Could not understand that date. Please try again.')
            continue
        if parsed_date.date() > datetime.now().date():
            print('Date acquired cannot be in the future. Please try again.')
            continue
        date_acq = parsed_date.strftime("%Y-%m-%d")
        break
    while True:
        water_freq = input('The plant watering frequency (in days): ').strip()
        if water_freq.isdigit() and int(water_freq) > 0:
            break
        else:
            print('Error! Enter a valip number: ')
    while True:
        sunlight = input('The plant sunlight needs, choose (Low, Medium, High): ').strip().capitalize()
        if sunlight in ['Low', 'Medium', 'High']:
            break
        else:
            print('Error! Enter Low, Medium, or High: ')

    
    new_plant =  pd.DataFrame({
        'Plant_id': [Plant_id],'Plant name': [name], 'Location': [location],'Date Acquired': [date_acq],'Water Frequency (in days)': [water_freq], 'Sunlight needs': [sunlight]
    })

    already_exists = os.path.exists(file_csv)
    new_plant.to_csv(file_csv, mode = 'a', header=not already_exists, index = False)
    

    print (f'The plant {name} added successfully!')



def search_plants():
    """
    Programmer: Meqdad Muhana
    Desc.: The user enters plant name or location to search from csv.
    """
    df = load_plants()

    if df.empty:
        print('No plant available, please add first.')
        return

    while True:
        to_search = input('To search, enter the plant name or location: ')
        if not to_search:
            print('Searched Cancelled')
            return
            

        mask = (df['Plant name'].str.contains (to_search, case = False, na = False) | 
            df['Location'].str.contains (to_search, case = False, na = False))
        matches = df[mask]
    
        if not matches.empty:
            break
        print('No matching with what you searched for.')

    print('matching results: ')
    for _, row in matches.iterrows():
        print(f'Plant ID: {row['Plant_id']}')
        print(f'Plant Name: {row['Plant name']}')
        print(f'Location: {row['Location']}')
        print(f'Date Acquired: {row['Date Acquired']}')
        print(f'Water Frequency (in days): {row['Water Frequency (in days)']}')
        print(f'Sunlight needs: {row['Sunlight needs']}')

photos_csv = 'plant_photos.csv'

def add_photo():
    """
    Programmer: Meqdad Muhana
    Desc.: Links a photo (file path) to a plant.
    """
    plant_id = input('Enter the Plant ID: ').strip()
    photo_path = input('Enter the photo file path: ').strip()

    new_photo = pd.DataFrame({'Plant_id': [plant_id], 'Photo Path': [photo_path]})

    already_exists = os.path.exists(photos_csv)
    new_photo.to_csv(photos_csv, mode='a', header=not already_exists, index=False)

    print('Photo added successfully!')

def Watering():
    return "Watering"

def Fertilizing():
    return "Fertilizing"

def Repotting():
    return "Repotting"

def Purning():
    return "Purning"


def save_care_activity(plant, activity, date):
    """
    programmer: Hajar Marzooq
    Take the output from the care_activity function and save it to a CSV file. 
    Appends output if the file exists, creates a new CSV file with headers if it doesn't.
    """
    care_history_file = "care_history.csv"
    # convert the passed data into a DataFrame

    record = pd.DataFrame([[plant, activity, date]], columns = ["plant", "activity", "date"])
    
    # Check if the file already exists on your system using os.path.exists, if it doesn't exist, 
    #we create a new one 
    
    file_exists = os.path.exists(care_history_file)

    if file_exists:
        record.to_csv(care_history_file, mode = "a", header = False, index = False)
        print(f"File {care_history_file} has been successfully updated!")

    else:
        record.to_csv(care_history_file, mode = "w", header = True, index = False)
        print(f"File {care_history_file} has been successfully created!")
        
        
def record_care_activity():
    """
    Programmer: Hajar Marzooq
    Takes plant name and activity from user and saves the current date
    """
    if not os.path.exists("plants.csv"):
        print("No plants found. Add a plant first.")
        return

    plants = pd.read_csv("plants.csv")

    plant = input("Enter plant name: ").strip()

    # check if plant exists or not
    if plant not in plants["Plant name"].values:
        print("Error: Plant does not exist.")
        return
    while True:
        choice = int(input(("Which activity: 1. Watering 2. Fertilizing 3. Repotting 4.Purning: ")))
        if choice == 1:
            activity = Watering()
            break

        elif choice == 2:
            activity = Fertilizing()
            break

        elif choice == 3:
            activity = Repotting()
            break

        elif choice == 4:
            activity = Purning()
            break 
            
        else:
            print("Invalid choice")
            
              
    date = datetime.now().date()
    save_care_activity(plant, activity, date)
    print(f"{activity} recorded for {plant}")

def view_plants_due():

    if not os.path.exists(file_csv):
        print("No plants found.")
        return []

    plants = pd.read_csv(file_csv)

    if plants.empty:
        print("Plants file is empty.")
        return []

    if not os.path.exists(care_history_file):
        print("No care history → all plants never watered.")

        results = [
            f"{plants.loc[i, 'Plant name']} — never watered"
            for i in range(len(plants))
        ]

    
        for r in results:
            print(r)

        return results

    care = pd.read_csv(care_history_file)

    results = []

    for i in range(len(plants)):
        plant_name = plants.loc[i, "Plant name"]
        freq = plants.loc[i, "Water Frequency (in days)"]

        plant_care = care[
            (care["plant"] == plant_name) &
            (care["activity"] == "Watering")
        ]

        if plant_care.empty:
            results.append(f"{plant_name} — never watered")
            continue
    

        last_date = pd.to_datetime(plant_care["date"].max())
        days_passed = (datetime.now() - last_date).days
        due_water = (int(days_passed) - freq)

        if days_passed > freq:
            results.append(f"{plant_name} — {due_water} since it was due for watering")
        else:
            print(f"{plant_name} is not due for watering")

    for r in results:
        print(r)

    return results
