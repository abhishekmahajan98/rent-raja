import pyzill
from myfunctions import execute_this
from collections import namedtuple
import json
import time
from tqdm import tqdm

BoundingBox = namedtuple("BoundingBox", ["zip_code", "ne_lat", "ne_long", "sw_lat", "sw_long"])

def bounding_box_generator(bounding_boxes):
    for zip_code, coords in bounding_boxes.items():
        ne_lat, ne_long = coords['northeast']
        sw_lat, sw_long = coords['southwest']
        yield BoundingBox(zip_code=zip_code, ne_lat=ne_lat, ne_long=ne_long, sw_lat=sw_lat, sw_long=sw_long)

def scrape():
    bounding_boxes = None
    with open('data/nyc_bounding_boxes.json', 'r') as f:
        bounding_box_data = json.load(f)
        bounding_boxes = bounding_box_generator(bounding_box_data)

    zoom_value = 1
    #pagination is for the list that you see at the right when searching
    #you don't need to iterate over all the pages because zillow sends the whole data on mapresults at once on the first page
    #however the maximum result zillow returns is 500, so if mapResults is 500
    #try playing with the zoom or moving the coordinates, pagination won't help because you will always get at maximum 500 results
    pagination = 1 

    for idx, bounding_box in tqdm(enumerate(bounding_boxes), total=1794):
        if idx < 500:
            continue
        try:
            results_rent = pyzill.for_rent(pagination, bounding_box.ne_lat,bounding_box.ne_long,bounding_box.sw_lat, bounding_box.sw_long, zoom_value, "")
        except Exception as e:
            print(f"Error at {bounding_box.zip_code}: {e}")
        else:
            with open(f"scraped_data/{bounding_box.zip_code}_rent.json", "w", encoding='utf-8') as f:
                json.dump(results_rent, f, indent=2)
            print(f"Wrote {bounding_box.zip_code}_rent.json")

        time.sleep(2)

def remove_duplicates():
    pass

@execute_this(stack_trace=True)
def main():
    scrape()

