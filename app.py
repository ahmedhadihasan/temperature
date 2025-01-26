import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

def filter_data(df, threshold, condition):
    """
    Filters the DataFrame based on the temperature threshold and condition.
    """
    if condition == "below":
        return df[df["Temperature"] < threshold]
    elif condition == "above":
        return df[df["Temperature"] > threshold]
    else:
        return df

def create_map(df_below, df_above):
    """
    Generates a folium map with temperature data points.
    """
    if not df_below.empty:
        center_lat = df_below["Latitude"].mean()
        center_lon = df_below["Longitude"].mean()
    else:
        center_lat = df_above["Latitude"].mean()
        center_lon = df_above["Longitude"].mean()

    folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Add below 25°C data in blue
    for _, row in df_below.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.7,
            popup=f"Temp: {row['Temperature']}°C",
        ).add_to(folium_map)

    # Add above 25°C data in red
    for _, row in df_above.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=f"Temp: {row['Temperature']}°C",
        ).add_to(folium_map)

    return folium_map

# Streamlit App UI
st.title("Temperature Data Analysis")
st.write("This app analyzes and visualizes geographical temperature data.")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel data
    df = pd.read_excel(uploaded_file)

    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Threshold selection
    threshold = st.slider("Set the temperature threshold:", min_value=-50, max_value=50, value=25)

    # Filter data
    df_below_25 = filter_data(df, threshold, "below")
    df_above_25 = filter_data(df, threshold, "above")

    # Display filtered data
    st.write(f"### Data Below {threshold}°C")
    st.dataframe(df_below_25)

    st.write(f"### Data Above {threshold}°C")
    st.dataframe(df_above_25)

    # Generate map
    st.write("### Temperature Map")
    folium_map = create_map(df_below_25, df_above_25)
    st_folium(folium_map, width=700, height=500)
