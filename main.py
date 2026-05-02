import pandas as pd
from make_pkl import make_pkl
import streamlit as st

# Run for the first time only to create the PKL file from the PDF
# make_pkl()

with open("ExamSeatingArrangement.pdf", "rb") as f:
    st.download_button(
        label="Download Seating Arrangement PDF",
        data=f,
        file_name="ExamSeatingArrangement.pdf",
        mime="application/pdf"
    )

df = pd.read_pickle("seating_arrangement.pkl")

def filter_by_location(rooms, location):
    if location == "FD-1":
        return [r for r in rooms if str(r).startswith("1")]
    elif location == "FD-2":
        return [r for r in rooms if str(r).startswith("2")]
    elif location == "LTC":
        return [r for r in rooms if str(r).startswith("5")]
    elif location == "NAB":
        return [r for r in rooms if str(r).startswith("6")]
    return rooms

df[["Date", "Time"]] = df["DATE & SESSION"].str.split(", ", expand=True)

st.title("Compre Room Finder")

date = st.selectbox("Select Date", sorted(df["Date"].dropna().unique()))
time = st.selectbox("Select Time", sorted(df["Time"].dropna().unique()))

filtered = df[(df["Date"] == date) & (df["Time"] == time)]

all_rooms = sorted(df["ROOM NO"].dropna().unique())
used_rooms = sorted(filtered["ROOM NO"].dropna().unique())
unused_rooms = sorted(set(all_rooms) - set(used_rooms))

location = st.selectbox("Select Location", ["All", "FD-1", "FD-2", "LTC", "NAB"])
used_rooms = filter_by_location(used_rooms, location)
unused_rooms = filter_by_location(unused_rooms, location)

st.subheader("Free Rooms")
if not unused_rooms:
    st.write("None")
else:
    cols = st.columns(4)
    for i, room in enumerate(unused_rooms):
        with cols[i % 4]:
            st.markdown(
                f"<div style='padding:10px; margin-bottom: 10px; border-radius:8px; background:#10b981; color:white; text-align:center;'>{room}</div>",
                unsafe_allow_html=True
            )

st.subheader("Rooms In Use")
if not used_rooms:
    st.write("None")
else:
    cols = st.columns(5)
    for i, room in enumerate(used_rooms):
        with cols[i % 5]:
            st.markdown(
                f"<div style='padding:10px; margin-bottom: 10px; border-radius:8px; background:#ef4444; color:white; text-align:center;'>{room}</div>",
                unsafe_allow_html=True
            )