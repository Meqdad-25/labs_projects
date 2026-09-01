# Programmer: Mohamed Salah
# desc: importing the functions done by my fellow teamates, and convert wtv needed to be converted to st form.

import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

PLANTS_FILE = "plants.csv"
CARE_FILE = "care_history.csv"
PHOTOS_FILE = "plant_photos.csv"

HEADERS = [
    "Plant_id",
    "Plant name",
    "Location",
    "Date Acquired",
    "Water Frequency (in days)",
    "Sunlight needs"
]

st.set_page_config(page_title="Plant Care Tracker", page_icon="🌱", layout="wide")

MENU_OPTIONS = [
    "Home",
    "Add New Plant",
    "Record Care Activity",
    "View Plants Due",
    "Search Plants",
    "View All Plants",
    "Add Photo",
]

if "menu" not in st.session_state:
    st.session_state.menu = "Home"


def go_home():
    st.session_state.menu = "Home"
    st.rerun()


def load_plants():
    if not os.path.exists(PLANTS_FILE):
        return pd.DataFrame(columns=HEADERS)
    return pd.read_csv(PLANTS_FILE)


st.title("🌱 Track Your Plant")
st.write("Track your plants, care history, and watering needs.")

menu = st.sidebar.selectbox(
    "Choose an option",
    MENU_OPTIONS,
    index=MENU_OPTIONS.index(st.session_state.menu)
)

st.session_state.menu = menu


if menu == "Home":
    plants = load_plants()

    st.header("Welcome")
    st.write("Use the sidebar to manage your plants.")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌱 Total Plants", len(plants))
    col2.metric("📍 Locations", plants["Location"].nunique() if not plants.empty else 0)
    col3.metric("☀️ Sunlight Types", plants["Sunlight needs"].nunique() if not plants.empty else 0)


elif menu == "Add New Plant":
    st.header("🌱 Add New Plant")

    with st.form("add_plant_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Plant name / species")
            location = st.text_input("Location")

        with col2:
            date_acq = st.date_input("Date acquired", datetime.now().date())
            water_freq = st.number_input("Watering frequency in days", min_value=1, step=1)
            sunlight = st.selectbox("Sunlight needs", ["Low", "Medium", "High"])

        submitted = st.form_submit_button("Add plant")

        if submitted:
            if name.strip() == "" or location.strip() == "":
                st.error("Plant name and location cannot be empty.")
            else:
                new_plant = pd.DataFrame({
                    "Plant_id": [str(uuid.uuid4())],
                    "Plant name": [name.strip()],
                    "Location": [location.strip()],
                    "Date Acquired": [date_acq.strftime("%Y-%m-%d")],
                    "Water Frequency (in days)": [int(water_freq)],
                    "Sunlight needs": [sunlight]
                })

                file_exists = os.path.exists(PLANTS_FILE)
                new_plant.to_csv(PLANTS_FILE, mode="a", header=not file_exists, index=False)

                st.success(f"{name} added successfully!")
                go_home()


elif menu == "Record Care Activity":
    st.header("💧 Record Care Activity")

    plants = load_plants()

    if plants.empty:
        st.warning("No plants found. Add a plant first.")
    else:
        with st.form("care_activity_form"):
            plant = st.selectbox("Choose plant", plants["Plant name"].tolist())
            activity = st.selectbox("Choose activity", ["Watering", "Fertilizing", "Repotting", "Purning"])
            date = st.date_input("Date", datetime.now().date())

            submitted = st.form_submit_button("Save care activity")

            if submitted:
                record = pd.DataFrame({
                    "plant": [plant],
                    "activity": [activity],
                    "date": [date.strftime("%Y-%m-%d")]
                })

                file_exists = os.path.exists(CARE_FILE)
                record.to_csv(CARE_FILE, mode="a", header=not file_exists, index=False)

                st.success(f"{activity} recorded for {plant}.")
                go_home()


elif menu == "View Plants Due":
    st.header("📅 Plants Due for Care")

    plants = load_plants()

    if plants.empty:
        st.warning("No plants found.")
    elif not os.path.exists(CARE_FILE):
        st.info("No care history found. All plants may be due.")
        st.dataframe(plants)
    else:
        care = pd.read_csv(CARE_FILE)
        due = []

        for _, row in plants.iterrows():
            plant_name = row["Plant name"]
            freq = int(row["Water Frequency (in days)"])

            plant_care = care[
                (care["plant"] == plant_name) &
                (care["activity"] == "Watering")
            ]

            if plant_care.empty:
                due.append({
                    "Plant name": plant_name,
                    "Status": "Never watered"
                })
            else:
                last_date = pd.to_datetime(plant_care["date"].max())
                days_passed = (datetime.now() - last_date).days

                if days_passed > freq:
                    due.append({
                        "Plant name": plant_name,
                        "Status": f"{days_passed - freq} days overdue"
                    })

        if len(due) == 0:
            st.success("No plants are due for watering.")
        else:
            st.warning("These plants are due:")
            st.dataframe(pd.DataFrame(due))


elif menu == "Search Plants":
    st.header("🔍 Search Plants")

    plants = load_plants()

    if plants.empty:
        st.warning("No plants available.")
    else:
        search_term = st.text_input("Search by plant name or location")

        if search_term:
            results = plants[
                plants["Plant name"].str.contains(search_term, case=False, na=False) |
                plants["Location"].str.contains(search_term, case=False, na=False)
            ]

            if results.empty:
                st.error("No matching plants found.")
            else:
                st.success("Matching plants found:")
                st.dataframe(results)


elif menu == "View All Plants":
    st.header("📋 View All Plants")

    plants = load_plants()

    if plants.empty:
        st.warning("No plants found.")
    else:
        for _, row in plants.iterrows():
            with st.container(border=True):
                st.subheader(f"🌿 {row['Plant name']}")
                col1, col2, col3 = st.columns(3)
                col1.write(f"📍 **Location:** {row['Location']}")
                col2.write(f"💧 **Water every:** {row['Water Frequency (in days)']} days")
                col3.write(f"☀️ **Sunlight:** {row['Sunlight needs']}")
                st.caption(f"Plant ID: {row['Plant_id']}")


elif menu == "Add Photo":
    st.header("📸 Add Photo")

    plants = load_plants()

    if plants.empty:
        st.warning("No plants found. Add a plant first.")
    else:
        with st.form("photo_form"):
            plant_id = st.selectbox("Choose Plant ID", plants["Plant_id"].tolist())
            photo_path = st.text_input("Enter photo file path")

            submitted = st.form_submit_button("Save photo")

            if submitted:
                if photo_path.strip() == "":
                    st.error("Photo path cannot be empty.")
                else:
                    new_photo = pd.DataFrame({
                        "Plant_id": [plant_id],
                        "Photo Path": [photo_path.strip()]
                    })

                    file_exists = os.path.exists(PHOTOS_FILE)
                    new_photo.to_csv(PHOTOS_FILE, mode="a", header=not file_exists, index=False)

                    st.success("Photo added successfully!")
                    go_home()