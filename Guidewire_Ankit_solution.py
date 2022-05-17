#import pandas and json libraries
# pip install pandas
# pip install phonenumbers

import argparse
import dataclasses
import json
import pandas as pd
from pprint import pprint
import phonenumbers
import re
import logging

list_entries=[]
errors=[]
processed_data={}

#Class to format the record into a standard format
@dataclasses.dataclass
class entries:
    color:str
    firstname:str
    lastname:str
    phonenumber:str
    zipcode:int

def validate_phone_number(phone_number):
    if isinstance(phone_number, float):
        logging.debug("Invalid number %s", phone_number)
        return False
    try:
        number = phonenumbers.parse(str(phone_number), "US")
    except phonenumbers.NumberParseException:
        return False

    if not phonenumbers.is_possible_number(number):
        return False
    return True

def format_phone_number(ph_number):
    ph_number = str(ph_number)
    ph_number = re.sub("[ ()-]", '', ph_number) # remove space, (), -
    ph_number = (f"{ph_number[:3]}-{ph_number[3:6]}-{ph_number[6:]}")
    logging.debug("Formatted number %s", ph_number)
    return ph_number

def clean_data(x):
    if isinstance(x, str):
        x.strip()
    if validate_phone_number(x):
        x = format_phone_number(x)
    return x

def process_data(data_file):
    # reading data from a txt file, assign column names to the file
    entry = pd.read_csv(data_file,
                        delimiter=',',
                        header=None,
                        names= ["C1","C2","C3","C4","C5"],
                        skipinitialspace=True)

    entry = entry.applymap(clean_data)

    for index, row in entry.iterrows():
        #when 3rd column is a phone number
        if (validate_phone_number(row["C3"])):
            # Instantiate a new class
            e1 = entries(row["C4"], row["C2"], row["C1"], row["C3"], row["C5"])
            list_entries.append(e1)
        #when 4th column is a phone number
        elif (validate_phone_number(row["C4"])):
            # Check of 5th column is empty
            if pd.isnull(row['C5']):
                name = row['C1'].split()
                first_name = name[0]
                last_name = name[-1]
                e1 = entries(row["C2"], first_name, last_name, row["C4"], row["C3"])
            else:
                e1 = entries(row["C5"], row["C1"], row["C2"], row["C4"], row["C3"])
            list_entries.append(e1)
        else:
            # errors records
            errors.append(index)

    #sort the correct records by lastname and firstname
    list_entries_sorted=sorted(list_entries, key=lambda row: (row.lastname, row.firstname))

    processed_data['entries']= [dataclasses.asdict(d) for d in list_entries_sorted]
    processed_data['errors']=errors
    return processed_data

if __name__=="__main__":
    # Lastname, Firstname, (703)-742-0996, color, zipcode
    # Firstname Lastname, color, zipcode, 703 955 0373
    # Firstname, Lastname, zipcode, 646 111 0101, color

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", type=str, default='C:\\Users\\amutreja\\Desktop\\Guidewire_Ankit_Arora\\data.txt', help="Data file to use")
    parser.add_argument("--output_file", type=str, default='C:\\Users\\amutreja\\Desktop\\Guidewire_Ankit_Arora\\result.out', help="Data file to use")
    parser.add_argument("--debug", default=False, action='store_true', help="Turn on debug logging.")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    processed_data = process_data(args.data_file)
    if args.debug:
        pprint(processed_data)
    with open(args.output_file, 'w') as outfile:
        json.dump(processed_data, outfile, indent=2)