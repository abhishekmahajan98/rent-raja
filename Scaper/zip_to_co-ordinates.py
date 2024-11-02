import geopandas as gpd
from zip_codes import nyc_zipcodes
import json
from myfunctions import execute_this

@execute_this
def zip_to_coordinates():

    gdf = gpd.read_file('data/ny_new_york_zip_codes_geo.min.json')

    bounding_boxes = {}
    for _, row in gdf.iterrows():
        zip_code = row['ZCTA5CE10']
        bounds = row['geometry'].bounds  # (minx, miny, maxx, maxy)
        bounding_boxes[zip_code] = {
            'southwest': (bounds[1], bounds[0]),  # (miny, minx)
            'northeast': (bounds[3], bounds[2])   # (maxy, maxx)
        }

    print('NYC Zip Codes:', len(bounding_boxes))
    with open('data/nyc_bounding_boxes.json', 'w') as f:
        json.dump(bounding_boxes, f, indent=2)