# flask toolkits
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
import numpy as np

# Create app and pass __name__
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/EndangeredAnimalDB'
mongo = PyMongo(app)

# >>> ROUTE 1 <<< #
# Define actions for the index route
@app.route('/')
def index():

    # Retrieve queried name from "query_im" Collection
    query_data = mongo.db.query_im.find_one()

    #  Pass Mars data to 'index.html' for display
    return render_template('index.html', qdata=query_data)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #    

# >>> ROUTE 2 <<< #
# Define actions for "name_request" route
@app.route('/animal', methods=['GET', 'POST'])
def name_request():
    
    # Retrieve name of target animal
    animal = request.args.get('type')
    
    # Empty dict to store retrieved data and transfer to "query_im" Collection
    query_data = {}

    # Data query and retrival from "animal_facts" Collection
    q_facts = mongo.db.animal_facts.find_one({"Common_Name":animal})
    other_name = q_facts['Other_Name']
    sci_name = q_facts['Sci_Name']
    try:
        nerc = q_facts['Native_Extant_Resident_Cntry']
    except:
        nerc = []
    try:
        nec = q_facts['Native_Extant_Cntry']
    except:
        nec = []

    # Special character appears in "animal"
    if animal == "Galapagos Penguin":
        animal = "Galápagos Penguin"
    # Data query and retrival from "species" Collection
    q_species = mongo.db.species.find_one({"Species Name":animal})

    try:
        status = q_species["Status"]
    except:
        status = np.nan
    try:
        population = q_species["Population"]
    except:
        population = np.nan
    try:
        descrip = q_species['Species Description']
    except:
        descrip = np.nan
    try:
        img_url = q_species['Species Image URL']
    except:
        img_url = np.nan    
    
    # Data query and retrival from "articles" Collection
    q_urls = mongo.db.articles.find_one({"endagered_animal":animal})

    # list to store article url data
    a_list = []

    # Append at most 8 article urls to "a_list"
    try:
        counter = 0
        for url in q_urls['url']:
            if counter <8:
                counter += 1
                a_list.append(url)
            else:
                break
    except:
        a_list = []

    # Data storage in "query_data"
    query_data['Common_Name'] = animal
    query_data['Other_Name'] = other_name
    query_data['Sci_Name'] = sci_name
    query_data['NERC'] = nerc
    query_data['NEC'] = nec
    query_data['Status'] = status
    query_data['Population'] = population
    query_data['Description'] = descrip
    query_data['Img_url'] = img_url
    query_data['Article_url'] = a_list
      
    # Clear intermediate query Collection
    mongo.db.query_im.drop()

    # Input queried data into "query_im" Collection with the key of "case_completed"  
    mongo.db.query_im.insert_one(query_data) 

    # Redirect to "/" route after data entry in MongoDB 
    return redirect("/", code=302)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# >>> ROUTE 3 <<< #
# Define actions for "api" route
@app.route('/api/temperature')
def api():
    
    # Retrieve document in "query_im" Collection
    query_data = mongo.db.query_im.find_one()
  
    # Retrieve name and extant countries of target animal
    animal = query_data['Common_Name']
    nerc = query_data['NERC']
    nec = query_data['NEC']

    # Data query and retrival from "temp_by_cntry" Collection
    list_tavg = []
    list_tavg_u = []
    list_date = []
    cntry_temp = []

    # List to store country names for both native extant resident or native extant   
    cntry_list = nerc
    [cntry_list.append(cntry) for cntry in nec if cntry not in cntry_list]

    # Loop through "cntry_list"
    for cntry in cntry_list:
        q_temp = mongo.db.temp_by_cntry.find({"Cntry": cntry})

        # Loop through each document for iterated country in "cntry_list"
        for case in q_temp:
            list_tavg.append(case['Avg Temp'])
            list_tavg_u.append(case['Avg Temp Uncertainty'])
            list_date.append(case['Date'])

        # Data structure of final output is list of dictionaries  
        cntry_temp.append({cntry: [{'Avg_Temp': list_tavg}, {'Avg_Temp_Uncertainty': list_tavg_u},\
            {'Date': list_date}]})
   
    return jsonify(cntry_temp)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# Execute the script
if __name__ == '__main__':
    app.run(debug=True)

