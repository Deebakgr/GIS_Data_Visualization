















# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import HeatMap, MarkerCluster, MeasureControl, Fullscreen, LocateControl, MiniMap
# from geopy.geocoders import Nominatim
# from streamlit_folium import folium_static
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Function to load data
# def load_data():
#     try:
#         # Load data from the Excel file and handle potential errors
#         Main_data = pd.read_excel('cropMain.xlsx', dtype=str)
#         Main_data = Main_data.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
#         return Main_data
#     except FileNotFoundError:
#         st.error("Error: Unable to find cropMain.xlsx file. Please make sure the file is in the correct location.")
#         return None
#     except Exception as e:
#         st.error(f"Error occurred while loading data: {e}")
#         return None

# # Function to get coordinates from location name
# def get_coordinates_from_location(location):
#     try:
#         geolocator = Nominatim(user_agent="your_app_name")
#         location_data = geolocator.geocode(location)
#         if location_data:
#             return [location_data.latitude, location_data.longitude]
#         else:
#             st.warning(f"No coordinates found for {location}.")
#     except Exception as e:
#         st.warning(f"Error occurred while getting coordinates: {e}")
#     return None

# # Function to get coordinates from pincode with retry mechanism
# def get_coordinates_from_pincode(pincode):
#     try:
#         retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#         session = requests.Session()
#         session.mount('https://', HTTPAdapter(max_retries=retries))
        
#         url = f'https://nominatim.openstreetmap.org/search?q={pincode}&format=json&limit=1&countrycodes=IN'
#         response = session.get(url, timeout=10)
        
#         if response.status_code == 200:
#             data = response.json()
#             if data:
#                 return [float(data[0]['lat']), float(data[0]['lon'])]
#         else:
#             st.warning(f"Failed to fetch coordinates for pincode: {pincode}. Status code: {response.status_code}")
#     except Exception as e:
#         st.warning(f"Error occurred while getting coordinates: {e}")
#     return None

# # Function to display overall BC details
# def display_overall_bc_details(data, state_data):
#     st.sidebar.write(f"## BC Details Count for {state_data}:")
#     state_data = data[data['State'] == state_data]
#     total_bcs = len(state_data)
#     total_male_bcs = len(state_data[state_data['Gender'].str.lower() == 'male'])
#     total_female_bcs = len(state_data[state_data['Gender'].str.lower() == 'female'])

#     st.sidebar.write(f"Total BCs: {total_bcs}")
#     st.sidebar.write(f"Total Male BCs: {total_male_bcs}")
#     st.sidebar.write(f"Total Female BCs: {total_female_bcs}")

#     bank_count = state_data['Bank Name'].value_counts()

#     st.sidebar.write("## Bank Details Count:")
#     st.sidebar.write(bank_count)

#     # Visualize BC details
#     st.sidebar.write("## BC Details Visualization:")
#     st.sidebar.info(f"Total BCs: {total_bcs}")
#     st.sidebar.info(f"Male BCs: {total_male_bcs}")
#     st.sidebar.info(f"Female BCs: {total_female_bcs}")

#     # Add icons for male and female BCs
#     st.sidebar.markdown('<i class="fas fa-male"></i> Male', unsafe_allow_html=True)
#     st.sidebar.markdown('<i class="fas fa-female"></i> Female', unsafe_allow_html=True)

#     # Visualize males and females for each bank
#     st.write("## Males and Females for Each Bank:")
#     gender_bank_count = state_data.groupby(['Bank Name', 'Gender']).size().unstack(fill_value=0)
#     st.write(gender_bank_count)

# # Function to display BC details in a popup
# def display_bc_details(row):
#     details = f"<b>Name:</b> {row['Name of BC']}<br>"
#     details += f"<b>Contact Number:</b> {row['Contact Number']}<br>"
#     details += f"<b>Gender:</b> {row['Gender']}<br>"
#     details += f"<b>Bank Name:</b> {row['Bank Name']}<br>"
#     details += f"<b>State:</b> {row['State']}<br>"
#     details += f"<b>Pincode:</b> {row['Pincode']}<br>"
#     return details

# # Main function
# def main():
#     st.set_page_config(
#         page_title="CropMain Dashboard",
#         page_icon="🌾",
#         layout="wide"
#     )

#     st.title("GIS Data Visualization Dashboard")

#     # Load data and handle failure scenarios
#     Main_data = load_data()
#     if Main_data is None:
#         return

#     st.sidebar.write("## Data Options")

#     # Dropdown for State Name
#     state_options = ['All'] + list(Main_data['State'].unique())
#     state_input = st.sidebar.selectbox("Select State Name:", state_options)

#     # Filter pincode options based on state selection
#     if state_input != 'All':
#         pincode_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Pincode'].unique())
#     else:
#         pincode_options = ['None'] + list(Main_data['Pincode'].unique())

#     pincode_input = st.sidebar.selectbox("Select Pincode:", pincode_options)

#     # Filter bank name options based on state selection
#     if state_input != 'All':
#         bank_name_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Bank Name'].unique())
#     else:
#         bank_name_options = ['None'] + list(Main_data['Bank Name'].unique())
#     bank_name_input = st.sidebar.selectbox("Select Bank Name:", bank_name_options)

#     # Dropdown for Gender
#     gender_options = ['All', 'Male', 'Female']
#     gender_input = st.sidebar.selectbox("Select Gender:", gender_options)

#     # Filter data based on selected options
#     if pincode_input != 'None':
#         is_pincode_selected = True
#         state_data = Main_data[Main_data['Pincode'] == str(pincode_input)]
#     else:
#         is_pincode_selected = False
#         if state_input and state_input != 'All':
#             state_data = Main_data[Main_data['State'] == state_input]
#             if bank_name_input != 'None':
#                 state_data = state_data[state_data['Bank Name'] == bank_name_input]
#             if gender_input != 'All':
#                 state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]
#         else:
#             state_data = Main_data
#             if bank_name_input != 'None':
#                 state_data = state_data[state_data['Bank Name'] == bank_name_input]
#             if gender_input != 'All':
#                 state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]

#     show_heatmap = st.sidebar.checkbox("Show Heatmap")
#     show_gender_markers = st.sidebar.checkbox("Show Gender Markers")
#     use_marker_cluster = st.sidebar.checkbox("Use Marker Cluster")
#     visualize_button = st.sidebar.button("Visualize Data")

#     # Ensure the button click behavior doesn't cause errors
#     if visualize_button:
#         coordinates = None

#         # Determine the initial coordinates based on selection
#         if is_pincode_selected:
#             coordinates = get_coordinates_from_pincode(str(pincode_input))
#         elif state_input and state_input != 'All':
#             coordinates = get_coordinates_from_location(state_input)

#         # Check if coordinates were successfully retrieved
#         if coordinates:
#             m = folium.Map(location=coordinates, zoom_start=6)

#             # Add Measure Control with distance in kilometers
#             m.add_child(MeasureControl(primary_length_unit='kilometers'))

#             # Add Fullscreen button
#             Fullscreen().add_to(m)

#             # Add LocateControl
#             LocateControl().add_to(m)

#             # Add MiniMap
#             minimap = MiniMap(toggle_display=True)
#             m.add_child(minimap)

#             # Process data visualization based on pincode or state
#             if is_pincode_selected:
#                 pincode_data = Main_data[(Main_data['Pincode'] == str(pincode_input)) & (Main_data['State'] == state_input)]
#                 bc_coordinates = get_coordinates_from_pincode(str(pincode_input))
#                 if bc_coordinates:
#                     marker_color = 'red' if show_gender_markers and pincode_data.iloc[0]['Gender'].lower() == 'female' else 'blue'

#                     # Use MarkerCluster if enabled
#                     if use_marker_cluster:
#                         marker_cluster = MarkerCluster().add_to(m)
#                         marker = folium.Marker(
#                             location=bc_coordinates,
#                             popup=display_bc_details(pincode_data.iloc[0]),
#                             icon=folium.Icon(color=marker_color)
#                         )
#                         marker_cluster.add_child(marker)
#                     else:
#                         folium.Marker(
#                             location=bc_coordinates,
#                             popup=display_bc_details(pincode_data.iloc[0]),
#                             icon=folium.Icon(color=marker_color)
#                         ).add_to(m)

#                     st.sidebar.write("### Selected Pincode Data:")
#                     st.sidebar.write(pincode_data)
#             else:
#                 if show_heatmap:
#                     heat_data = []
#                     for _, row in state_data.iterrows():
#                         bc_coordinates = get_coordinates_from_pincode(row['Pincode'])
#                         if bc_coordinates:
#                             heat_data.append(bc_coordinates)
#                     HeatMap(heat_data).add_to(m)

#                 # Add markers for each data row
#                 for _, row in state_data.iterrows():
#                     bc_coordinates = get_coordinates_from_pincode(row['Pincode'])
#                     if bc_coordinates:
#                         marker_color = 'red' if show_gender_markers and row['Gender'].lower() == 'female' else 'blue'
#                         if use_marker_cluster:
#                             marker_cluster = MarkerCluster().add_to(m)
#                             marker = folium.Marker(
#                                 location=bc_coordinates,
#                                 popup=display_bc_details(row),
#                                 icon=folium.Icon(color=marker_color)
#                             )
#                             marker_cluster.add_child(marker)
#                         else:
#                             folium.Marker(
#                                 location=bc_coordinates,
#                                 popup=display_bc_details(row),
#                                 icon=folium.Icon(color=marker_color)
#                             ).add_to(m)

#             # Render the folium map
#             folium_static(m)

#             # Display state data table and overall BC details
#             col1, col2 = st.columns([1, 1])  # Adjusted column widths

#             with col1:
#                 st.write("## BC Details:")
#                 state_data_scroll = state_data[['Name of BC', 'Contact Number', 'Gender', 'Bank Name', 'State', 'Pincode']]
#                 st.dataframe(state_data_scroll)

#             st.write("## Other Details:")
#             if state_input and state_input != 'All':
#                 display_overall_bc_details(Main_data, state_input)
#         else:
#             st.error("Unable to retrieve coordinates. Please check your inputs or try again.")

# if __name__ == "__main__":
#     main()










import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster, MeasureControl, Fullscreen, LocateControl, MiniMap
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Function to load data
def load_data():
    try:
        Main_data = pd.read_excel('cropMain.xlsx', dtype=str)
        Main_data = Main_data.applymap(lambda x: x.replace(',', '') if isinstance(x, str) else x)
        return Main_data
    except FileNotFoundError:
        st.error("Error: Unable to find cropMain.xlsx file. Please make sure the file is in the correct location.")
        return None
    except Exception as e:
        st.error(f"Error occurred while loading data: {e}")
        return None

# Function to get coordinates from location name
def get_coordinates_from_location(location):
    try:
        geolocator = Nominatim(user_agent="your_app_name")
        location_data = geolocator.geocode(location)
        if location_data:
            return [location_data.latitude, location_data.longitude]
        else:
            st.warning(f"No coordinates found for {location}.")
    except Exception as e:
        st.warning(f"Error occurred while getting coordinates: {e}")
    return None

# Function to get coordinates from pincode with retry mechanism
def get_coordinates_from_pincode(pincode):
    try:
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        url = f'https://nominatim.openstreetmap.org/search?q={pincode}&format=json&limit=1&countrycodes=IN'
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return [float(data[0]['lat']), float(data[0]['lon'])]
        else:
            st.warning(f"Failed to fetch coordinates for pincode: {pincode}. Status code: {response.status_code}")
    except Exception as e:
        st.warning(f"Error occurred while getting coordinates: {e}")
    return None

# Function to display overall BC details
def display_overall_bc_details(data, state_data):
    st.sidebar.write(f"## BC Details Count for {state_data}:")
    state_data = data[data['State'] == state_data]
    total_bcs = len(state_data)
    total_male_bcs = len(state_data[state_data['Gender'].str.lower() == 'male'])
    total_female_bcs = len(state_data[state_data['Gender'].str.lower() == 'female'])

    st.sidebar.write(f"Total BCs: {total_bcs}")
    st.sidebar.write(f"Total Male BCs: {total_male_bcs}")
    st.sidebar.write(f"Total Female BCs: {total_female_bcs}")

    bank_count = state_data['Bank Name'].value_counts()

    st.sidebar.write("## Bank Details Count:")
    st.sidebar.write(bank_count)

    st.sidebar.write("## BC Details Visualization:")
    st.sidebar.info(f"Total BCs: {total_bcs}")
    st.sidebar.info(f"Male BCs: {total_male_bcs}")
    st.sidebar.info(f"Female BCs: {total_female_bcs}")

    st.sidebar.markdown('<i class="fas fa-male"></i> Male', unsafe_allow_html=True)
    st.sidebar.markdown('<i class="fas fa-female"></i> Female', unsafe_allow_html=True)

    st.write("## Males and Females for Each Bank:")
    gender_bank_count = state_data.groupby(['Bank Name', 'Gender']).size().unstack(fill_value=0)
    st.write(gender_bank_count)

# Function to display BC details in a popup
def display_bc_details(row):
    details = f"<b>Name:</b> {row['Name of BC']}<br>"
    details += f"<b>Contact Number:</b> {row['Contact Number']}<br>"
    details += f"<b>Gender:</b> {row['Gender']}<br>"
    details += f"<b>Bank Name:</b> {row['Bank Name']}<br>"
    details += f"<b>State:</b> {row['State']}<br>"
    details += f"<b>Pincode:</b> {row['Pincode']}<br>"
    return details

# Main function
def main():
    st.set_page_config(
        page_title="CropMain Dashboard",
        page_icon="🌾",
        layout="wide"
    )

    st.title("GIS Data Visualization Dashboard")

    # Load data and handle failure scenarios
    Main_data = load_data()
    if Main_data is None:
        return

    st.sidebar.write("## Data Options")

    # Dropdown for State Name
    state_options = ['All'] + list(Main_data['State'].unique())
    state_input = st.sidebar.selectbox("Select State Name:", state_options)

    # Filter pincode options based on state selection
    if state_input != 'All':
        pincode_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Pincode'].unique())
    else:
        pincode_options = ['None'] + list(Main_data['Pincode'].unique())

    pincode_input = st.sidebar.selectbox("Select Pincode:", pincode_options)

    # Filter bank name options based on state selection
    if state_input != 'All':
        bank_name_options = ['None'] + list(Main_data[Main_data['State'] == state_input]['Bank Name'].unique())
    else:
        bank_name_options = ['None'] + list(Main_data['Bank Name'].unique())
    bank_name_input = st.sidebar.selectbox("Select Bank Name:", bank_name_options)

    # Dropdown for Gender
    gender_options = ['All', 'Male', 'Female']
    gender_input = st.sidebar.selectbox("Select Gender:", gender_options)

    # Filter data based on selected options
    if pincode_input != 'None':
        is_pincode_selected = True
        state_data = Main_data[Main_data['Pincode'] == str(pincode_input)]
    else:
        is_pincode_selected = False
        if state_input and state_input != 'All':
            state_data = Main_data[Main_data['State'] == state_input]
            if bank_name_input != 'None':
                state_data = state_data[state_data['Bank Name'] == bank_name_input]
            if gender_input != 'All':
                state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]
        else:
            state_data = Main_data
            if bank_name_input != 'None':
                state_data = state_data[state_data['Bank Name'] == bank_name_input]
            if gender_input != 'All':
                state_data = state_data[state_data['Gender'].str.lower() == gender_input.lower()]

    show_heatmap = st.sidebar.checkbox("Show Heatmap")
    show_gender_markers = st.sidebar.checkbox("Show Gender Markers")
    use_marker_cluster = st.sidebar.checkbox("Use Marker Cluster")
    visualize_button = st.sidebar.button("Visualize Data")

    # Ensure the button click behavior doesn't cause errors
    if visualize_button:
        coordinates = None

        # Determine the initial coordinates based on selection
        if is_pincode_selected:
            coordinates = get_coordinates_from_pincode(str(pincode_input))
        elif state_input and state_input != 'All':
            coordinates = get_coordinates_from_location(state_input)

        # Set default coordinates if none found
        if not coordinates:
            coordinates = [20.5937, 78.9629]  # Center of India as default

        m = folium.Map(location=coordinates, zoom_start=6)

        # Add Measure Control with distance in kilometers
        m.add_child(MeasureControl(primary_length_unit='kilometers'))

        # Add Fullscreen button
        Fullscreen().add_to(m)

        # Add LocateControl to identify current location
        LocateControl().add_to(m)

        # Add MiniMap
        minimap = MiniMap(toggle_display=True)
        m.add_child(minimap)

        # Add MarkerCluster if enabled
        if use_marker_cluster:
            marker_cluster = MarkerCluster().add_to(m)

        # Process data visualization based on pincode or state
        if is_pincode_selected:
            pincode_data = Main_data[(Main_data['Pincode'] == str(pincode_input)) & (Main_data['State'] == state_input)]
            bc_coordinates = get_coordinates_from_pincode(str(pincode_input))
            if bc_coordinates:
                marker_color = 'red' if show_gender_markers and pincode_data.iloc[0]['Gender'].lower() == 'female' else 'blue'

                # Use MarkerCluster if enabled
                marker = folium.Marker(
                    location=bc_coordinates,
                    popup=display_bc_details(pincode_data.iloc[0]),
                    icon=folium.Icon(color=marker_color)
                )
                if use_marker_cluster:
                    marker_cluster.add_child(marker)
                else:
                    marker.add_to(m)

                st.sidebar.write("### Selected Pincode Data:")
                st.sidebar.write(pincode_data)
        else:
            if show_heatmap:
                heat_data = []
                for _, row in state_data.iterrows():
                    bc_coordinates = get_coordinates_from_pincode(row['Pincode'])
                    if bc_coordinates:
                        heat_data.append(bc_coordinates)
                HeatMap(heat_data).add_to(m)

            # Add markers for each data row
            for _, row in state_data.iterrows():
                bc_coordinates = get_coordinates_from_pincode(row['Pincode'])
                if bc_coordinates:
                    marker_color = 'red' if show_gender_markers and row['Gender'].lower() == 'female' else 'blue'
                    marker = folium.Marker(
                        location=bc_coordinates,
                        popup=display_bc_details(row),
                        icon=folium.Icon(color=marker_color)
                    )
                    if use_marker_cluster:
                        marker_cluster.add_child(marker)
                    else:
                        marker.add_to(m)

        # Render the folium map
        folium_static(m)

        # Display state data table and overall BC details
        col1, col2 = st.columns([1, 1])  # Adjusted column widths

        with col1:
            st.write("## BC Details:")
            state_data_scroll = state_data[['Name of BC', 'Contact Number', 'Gender', 'Bank Name', 'State', 'Pincode']]
            st.dataframe(state_data_scroll)

        st.write("## Other Details:")
        if state_input and state_input != 'All':
            display_overall_bc_details(Main_data, state_input)

if __name__ == "__main__":
    main()

