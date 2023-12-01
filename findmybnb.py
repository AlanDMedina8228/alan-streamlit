import streamlit as st
import requests
import pandas as pd

# Function to get Airbnb listings based on user inputs
def get_airbnb_listings(querystring):
    # RapidAPI key
    rapidapi_key = "82a9236d17msh6ca88ebd6b7bf72p1bf8bfjsn71189a3e69a9"
    headers = {
        'x-rapidapi-host': "airbnb13.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    
    # API endpoint
    url = "https://airbnb13.p.rapidapi.com/search-location"

    # Making the API request
    response = requests.get(url, headers=headers, params=querystring)

    # Processing the response
    if response.status_code == 200:
        try:
            data = response.json()
            if 'error' in data and not data['error']:
                if 'results' in data:
                    listings = data['results']
                    if listings:
                        # Create lists to store data
                        names, cities, types, prices, urls, amenities, cancel_policy, sample_pictures = [], [], [], [], [], [], [], []
                        for listing in listings:
                            name = listing.get('name', 'N/A')
                            city = listing.get('city', 'N/A')
                            type_ = listing.get('type', 'N/A')
                            price = listing['price'].get('rate', 'N/A')
                            url = listing.get('url', 'N/A')
                            amenity = listing.get('previewAmenities', 'N/A')
                            cancel = listing.get('cancelPolicy', 'N/A')
                            image_url = listing.get('images', ['N/A'])[0] #multiple images


                            names.append(name)
                            cities.append(city)
                            types.append(type_)
                            prices.append(price)
                            urls.append(url)
                            amenities.append(amenity)
                            cancel_policy.append(cancel)
                            sample_pictures.append(f'<img src="{image_url}" width="100">')


                        # Create DataFrame from lists
                        df = pd.DataFrame({
                            'Name': names,
                            'City': cities,
                            'Type': types,
                            'Price (Price for your entire stay)': [f"${price}" for price in prices],
                            'AirBnB Link': urls,
                            'Amenities': amenities,
                            'Cancel Policy': cancel_policy,
                            'Sample Picture': sample_pictures
                        })

                        # Displaying the table
                        st.markdown("### Airbnb Listings")
                        
                        # Create clickable URLs in the table
                        df_with_links = df.copy()
                        df_with_links['AirBnB Link'] = df_with_links['AirBnB Link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
                        
                        # Set table text color
                        st.write(df_with_links.to_html(escape=False), unsafe_allow_html=True)
                        st.markdown(
                            """
                            <style>
                            table {
                                color: #f5385c;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown("<p style='color: #FF69B4;'>No listings found for the given criteria.</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #FF69B4;'>No results found.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #FF69B4;'>Error in fetching data. Please check your inputs and try again.</p>", unsafe_allow_html=True)
                st.write("Response content:", response.content)
        except Exception as e:
            st.markdown(f"<p style='color: #FF69B4;'>An error occurred while processing data: {e}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #FF69B4;'>Error fetching data. Please check your inputs and try again.</p>", unsafe_allow_html=True)
        st.write("Response content:", response.content)

# Display the logo, title, description, and creator information
st.image("images/FindMyBnB.jpg", width=350) #image1
st.title("FindMyBnB") #1st Streamlit Method
st.write(
    """
    FindMyBnB helps you discover the perfect accommodations for your travel needs! 
    Enter your preferences on the sidebar and click 'Search' to explore available listings. The listings
    will be in a table filled with the name, city, building type, price for your stay, a direct link to
    AirBnB, amenities, cancel policies, and a sample image.
    """,
    unsafe_allow_html=True
)
st.write("Created by: Alan D. Medina")

# Styling for the Streamlit app
st.markdown(
    """
    <style>
    body {
        margin-left: 25%; /* Adjust the percentage to shift content */
    }

    .stTextInput>div>div>input[type="text"],
    .stTextInput>div>div>input[type="number"],
    .stTextArea>div>textarea,
    .stButton {
        color: #f5385c;
        font-size: 18px;
    }
    .stTitle {
        font-size: 36px !important;
        text-align: center;
    }
    .stText {
        font-size: 24px;
        text-align: left; /* Adjust text alignment */
        margin-top: 20px;
    }
    .stHeader {
        text-align: center;
        font-size: 24px;
    </style>
    """,
    unsafe_allow_html=True
)

# UI elements for user inputs
st.sidebar.image("images/plus.jpg", width=500) #image2
st.sidebar.title("FindMyBnB")
name = st.sidebar.text_input("Please enter your name:") #2nd Streamlit Method
location = st.sidebar.text_input("Enter the city you want to travel to:")
checkin = st.sidebar.date_input("Check-in date:", format="MM/DD/YYYY") #3rd Streamlit Method
checkout = st.sidebar.date_input("Check-out date:", format="MM/DD/YYYY")
adults = st.sidebar.number_input("Number of adults:", min_value=1, max_value=10, value=1) #4th Streamlit Method
children = st.sidebar.slider("Number of children (2-12 years) (optional):", min_value=0, max_value=10, value=0) #5th Streamlit Method
infants_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
infants = st.sidebar.radio("Number of infants (under 2 years) (optional):", infants_options, index=0) #6th Streamlit Method
pets_options = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pets = st.sidebar.selectbox("Number of pets (optional):", pets_options, index=0) #7th StreamlitMethod

# Warn if any input is incomplete
if not all([name, location, checkin, checkout]):
    st.sidebar.warning("Please fill out all the information to search for listings.") #7th Streamlit Method

# Warn if more than 16 individuals total
if adults + children + infants + pets > 20:
    st.sidebar.warning("Maximum total individuals is 20. Please adjust the numbers. This cannot be a party!")

# Button to trigger fetching Airbnb listings
search_clicked = st.sidebar.button("Search") #8th Streamlit Method
if search_clicked:
    st.sidebar.empty() #9th Streamlit Method
    st.markdown(f"### Hello, {name}!")
    st.markdown(f"### Fetching Airbnb listings for {location} from {checkin} to {checkout}.", unsafe_allow_html=True)
    querystring = {
        "location": location,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "infants": infants,
        "pets": pets
    }
    get_airbnb_listings(querystring)
