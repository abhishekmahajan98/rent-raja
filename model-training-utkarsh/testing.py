import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize the geolocator
geolocator = Nominatim(user_agent="nyc_neighborhood_fetcher")

rent_df = pd.read_csv('/Users/utkarsh/Desktop/Utkarsh/NYU/Year 2/Semester 1/DS/Project/rent-raja/final_data_cleaning/final_cleaned_data.csv')

# Function to fetch neighborhood
def get_neighborhood(address):
    try:
        location = geolocator.geocode(address)
        if location:
            # Reverse geocode to get detailed address
            location_detail = geolocator.reverse((location.latitude, location.longitude), exactly_one=True)
            if location_detail:
                # Extract neighborhood from the address details
                address_components = location_detail.raw.get('address', {})
                return address_components.get('neighbourhood') or address_components.get('suburb')
    except GeocoderTimedOut:
        return None
    return None

# CSV file to save progress
output_csv = 'neighborhood_fetched.csv'

# Check if the CSV file already exists
write_header = not pd.io.common.file_exists(output_csv)  # Write header only if file does not exist

# Loop through rows with missing neighborhoods
for index, row in rent_df[rent_df['neighborhood'].isnull()].iterrows():
    # Fetch neighborhood
    address = row['street']
    neighborhood = get_neighborhood(address)

    # Append the index and neighborhood to the CSV file
    new_row = pd.DataFrame({'index': [index], 'neighborhood': [neighborhood]})
    new_row.to_csv(output_csv, mode='a', header=write_header, index=False)

    # After writing the header once, ensure it isn't written again
    write_header = False

    # Add a delay to respect rate limits
    time.sleep(1)