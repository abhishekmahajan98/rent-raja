import requests
import pandas as pd

# Replace 'YOUR_CENSUS_API_KEY' with your actual Census API key.
API_KEY = 'a2fc1c3c33976f55f2e714001c9eba6314ac3865'

# Define the Census API endpoint for ACS 5-year data
BASE_URL = "https://api.census.gov/data/2022/acs/acs5"

# Comprehensive list of variables with user-friendly headers
variables = [
    'B01003_001E',  # Total Population
    'B01002_001E',  # Median Age
    'B01001_002E',  # Male Population
    'B01001_026E',  # Female Population
    'B02001_002E',  # White Alone
    'B02001_003E',  # Black or African American Alone
    'B02001_005E',  # Asian Alone
    'B03003_003E',  # Hispanic or Latino
    'B11001_001E',  # Number of Households
    'B19013_001E',  # Median Household Income
    'B19301_001E',  # Per Capita Income
    'B17001_002E',  # Population Below Poverty Level
    'B23025_004E',  # Employed
    'B23025_005E',  # Unemployed
    'B19001_001E',  # Total Income Distribution
    'B25064_001E',  # Median Gross Rent
    'B25077_001E',  # Median Home Value
    'B25002_002E',  # Occupied Housing Units
    'B25002_003E',  # Vacant Housing Units
    'B25075_002E',  # Owner-Occupied Housing Units (value < $100,000)
    'B25105_001E',  # Monthly Housing Costs
    'B15003_017E',  # High School Graduate (Age 25+)
    'B15003_022E',  # Bachelor's Degree (Age 25+)
    'B15003_025E',  # Graduate or Professional Degree (Age 25+)
    'B16001_002E',  # English Only
    'B16001_003E',  # Spanish
    'B12001_003E',  # Never Married
    'B12001_004E',  # Currently Married
    'B12001_010E'   # Divorced
]

# Mapping of variable codes to user-friendly headers
headers = {
    'B01003_001E': 'Total Population',
    'B01002_001E': 'Median Age',
    'B01001_002E': 'Male Population',
    'B01001_026E': 'Female Population',
    'B02001_002E': 'White Alone',
    'B02001_003E': 'Black or African American Alone',
    'B02001_005E': 'Asian Alone',
    'B03003_003E': 'Hispanic or Latino',
    'B11001_001E': 'Number of Households',
    'B19013_001E': 'Median Household Income',
    'B19301_001E': 'Per Capita Income',
    'B17001_002E': 'Population Below Poverty Level',
    'B23025_004E': 'Employed',
    'B23025_005E': 'Unemployed',
    'B19001_001E': 'Total Income Distribution',
    'B25064_001E': 'Median Gross Rent',
    'B25077_001E': 'Median Home Value',
    'B25002_002E': 'Occupied Housing Units',
    'B25002_003E': 'Vacant Housing Units',
    'B25075_002E': 'Owner-Occupied Units (value < $100,000)',
    'B25105_001E': 'Monthly Housing Costs',
    'B15003_017E': 'High School Graduate (Age 25+)',
    'B15003_022E': 'Bachelor’s Degree (Age 25+)',
    'B15003_025E': 'Graduate or Professional Degree (Age 25+)',
    'B16001_002E': 'English Only',
    'B16001_003E': 'Spanish',
    'B12001_003E': 'Never Married',
    'B12001_004E': 'Currently Married',
    'B12001_010E': 'Divorced'
}

ny_zipcodes = [
    # Manhattan
    '10001', '10002', '10003', '10004', '10005', '10006', '10007', 
    '10008', '10009', '10010', '10011', '10012', '10013', '10014', 
    '10015', '10016', '10017', '10018', '10019', '10020', '10021', 
    '10022', '10023', '10024', '10025', '10026', '10027', '10028', 
    '10029', '10030', '10031', '10032', '10033', '10034', '10035', 
    '10036', '10037', '10038', '10039', '10040',

    # Brooklyn
    '11201', '11202', '11203', '11204', '11205', '11206', '11207', 
    '11208', '11209', '11210', '11211', '11212', '11213', '11214', 
    '11215', '11216', '11217', '11218', '11219', '11220', '11221', 
    '11222', '11223', '11224', '11225', '11226', '11228', '11229', 
    '11230', '11231', '11232', '11233', '11234', '11235', '11236', 
    '11237', '11238', '11239', '11240',

    # Queens
    '11354', '11355', '11356', '11357', '11358', '11359', '11360', 
    '11361', '11362', '11363', '11364', '11365', '11366', '11367', 
    '11368', '11369', '11370', '11371', '11372', '11373', '11374', 
    '11375', '11376', '11377', '11378', '11379', '11380', '11381', 
    '11382', '11383', '11384', '11385', '11386', '11387', '11388', 
    '11389', '11390', '11391', '11392', '11393', '11394', '11395', 
    '11396',

    # The Bronx
    '10451', '10452', '10453', '10454', '10455', '10456', '10457', 
    '10458', '10459', '10460', '10461', '10462', '10463', '10464', 
    '10465', '10466', '10467', '10468', '10469', '10470', '10471', 
    '10472', '10473', '10474', '10475',

    # Staten Island
    '10301', '10302', '10303', '10304', '10305', '10306', '10307', 
    '10308', '10309', '10310', '10311', '10312', '10313', '10314'
]


# Request parameters to get the comprehensive list of variables
params = {
    'get': ','.join(variables),  # Convert variable codes to a comma-separated string
    'for': 'zip code tabulation area:*',  # Specify all ZCTAs for geographic data
    'key': API_KEY
}

# Fetch data from the Census API
response = requests.get(BASE_URL, params=params)

# Check if the response status code is 200 and handle JSON parsing error
if response.status_code == 200:
    try:
        data = response.json()
        
        # Convert data to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])  # Use the first row for headers
        
        # Filter to only include targeted ZIP codes
        df = df[df['zip code tabulation area'].isin(ny_zipcodes)]
        
        # Rename columns using the header mapping
        df.rename(columns=headers, inplace=True)

        # Save the DataFrame to a CSV file
        output_file = 'ny_rent_prediction_data_comprehensive.csv'
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    except requests.exceptions.JSONDecodeError:
        print("Error: The response could not be decoded as JSON.")
        print(f"Response text: {response.text}")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
