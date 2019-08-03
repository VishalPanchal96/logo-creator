"""
Created By  : Prasad Pingle
Created At  : 26 June 2019
Description : This is sample flask application with sample API 
              to get company details and create logo
Dependancies: Data file "data/CompaniesList.json" which contains company details.
"""

from flask import Flask, request, jsonify, render_template,send_file
import json
import os
import pprint

app = Flask(__name__)
app.config["DEBUG"] = True


"Configuration for LOGO LETTERS as alphanumeric only or alphanumeric plus characters (COMMENT ONE OF THE BELOW LINE)"
CONST_COMPANY_LETTERS = "ALPHANUM"
# CONST_COMPANY_LETTERS = "ALPHANUM+SPECIAL"


# Defining the data source for the company details
data_source = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/CompaniesList.json")


# Function read_json_data() : reading the data from json file
# Created By: Prasad Pingle 30/06/2019
def read_json_data(data_source):
    try:
        fp = open(data_source, encoding="utf8") #reading the file in UTF-8 format
        data = json.loads(fp.read())
        return data
    except:
        return jsonify("Cannot read file")

# Function get_all_company_logos() : generating the company logos for all files and passing the generated file for download
# Created By: Prasad Pingle 30/06/2019
@app.route('/api/v1/resources/getCompanyLogo/<company_id>', methods=['GET'])
def get_company_logo(company_id):
    company_details = read_json_data(data_source)
    company_id = company_id.upper() #Converting to uppercase for handling as IDs are stored in uppercase format in JSON file (CONFIGURABLE)
    try:
        for company_ctr in range(len(company_details)):
            if ('Company Name' in company_details[company_ctr] and 'CompanyId' in company_details[company_ctr] 
            and company_details[company_ctr]['CompanyId'] == company_id):
                company_name = company_details[company_ctr]['Company Name'].strip().lower()
                alpha_sort = ''.join(sorted(company_name))  #Sorting the name alphabetically
                if len(alpha_sort) > 0:
                    occurence_obj = {}
                    occurence_obj = check_occurence(str(alpha_sort))
                    logo = generate_logo(occurence_obj)
                    company_details[company_ctr]['logoCharacters'] = ",".join(logo)
                    print("LOGO",company_details[company_ctr]['logoCharacters'])
                    break
        logo_details = {}
        logo_details['companyId'] = company_details[company_ctr]['CompanyId']
        logo_details['companyName'] = company_details[company_ctr]['Company Name']
        logo_details['companyLogo'] = company_details[company_ctr]['logoCharacters']

        return render_template('view_logo.html', companyDetails = logo_details)
    except:
        return "Please enter proper ID"


# Function check_occurence() : checking the occurence of each letter in the company name and returning the object
# Created By: Prasad Pingle 30/06/2019
def check_occurence(str):
    occurence = {}
    for c in str:
        try:
            if CONST_COMPANY_LETTERS == "ALPHANUM": #CONFIGURABLE 
                if c != " " and c.isalnum() == True: #Ignoring the whitespaces as well as special characters
                    occurence[c] = str.count(c)
            elif CONST_COMPANY_LETTERS == "ALPHANUM+SPECIAL": #CONFIGURABLE
                if c != " ": #Ignoring the whitespaces but allowing special characters
                    occurence[c] = str.count(c)
        except:
            continue
    return occurence

# Function generate_logo() : generating the logo for each company name
# Created By: Prasad Pingle 30/06/2019
def generate_logo(occurence_obj):
    occ_keys = []
    occ_values = []
    occ_keys = list(occurence_obj.keys()) # separating the keys from occurence_obj
    occ_values = list(occurence_obj.values()) # separating the values from occurence_obj
    logo = []
    if len(occ_values) > 0:
        for counter in range(len(occ_values)):
            try:
                max_occ = max(occ_values)
                max_element_index = occ_values.index(max_occ)
                letter = occ_keys[max_element_index]
                logo.append(letter.upper()) #capitalizing the letter
                occ_keys.pop(max_element_index) #removing the maximum element
                occ_values.pop(max_element_index)
                if counter == 2:
                    break
            except:
                continue
    return logo


# Function create_output_file() : create an output file for logo details(FUTURE SCOPE)
# Created By: Prasad Pingle 30/06/2019
def create_output_file(company_details):
    formatted_company_details = json.dumps(company_details, indent=4)
    f = open("company_logo.json", "w")
    f.write((format(formatted_company_details)))
    f.close()
    return formatted_company_details
    
# Homepage for downloading the company logo file
# Created By: Prasad Pingle 30/06/2019
@app.route('/')
def index():
   return render_template('create_logo.html')

# Running the application on localhost:8888
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

#Handling for invalid routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": "404", "data": "Page Not Found!"})