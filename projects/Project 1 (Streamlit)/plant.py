# """"
# programmer:Mohamed salah, 
# Desc: this is the first thing the user is displayed with

# """"
import pandas 
import os 
import uuid
from IPython.display import display
import backend as bk
    
def display_menu():
    print("Welcome to Plant Care Tracker")
    print("1. Add new plant") 
    print("2. Record care activity") 
    print("3. View plants due for care")
    print("4. Search plants by name or location")
    print("5. load plants")
    print("6. Add_photo")
    print("7. Exit")
    
def exit_program():
    print("See you soon!")
    
def main():
  while True: 
    display_menu()
    choice = input('Choose an option: ') 
    if choice == '1':
        bk.add_new_plant()
    elif choice == '2':
        bk.record_care_activity()
    elif choice == '3':
        bk.view_plants_due()
    elif choice == '4':
        bk.search_plants()
    elif choice == '5':
        bk.display(bk.load_plants())
    elif choice  == '6':
        bk.add_photo()
    elif choice == '7' :
        exit_program()
        break
    else:
        print('Invalid choice. Please choose a number from 1 to 7.')

main() 

