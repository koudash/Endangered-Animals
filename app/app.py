# flask toolkits
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo


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
# Define actions for "scrape" route
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

    # Data query and retrival from "temp_by_cntry" Collection
    # temp = {}
    # for cntry in nerc:
    #     temp

    # Data query and retrival from "species" Collection
    sp_facts = mongo.db.species.find_one({"Species Name":animal})
    status = sp_facts["Status"]
    population = sp_facts["Population"]
    descrip = sp_facts['Species Description']
    img_url = sp_facts['Species Image URL']    
    
    # Data query and retrival from "articles" Collection
    a_facts = mongo.db.articles.find({"Species Name":animal})

    # list to store article url data
    a_list = []

    # Append article urls to "a_list"
    for article in a_facts:
        a_list.append(article)

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
    query_in ={}
    query_in["case_completed"] = query_data    
    mongo.db.query_im.insert_one(query_in) 

    # Redirect to "/" route after data entry in MongoDB 
    return redirect("/", code=302)
# >>>>>>>>>>> I AM A ROUTE SEPARATOR <<<<<<<<<<< #

# Execute the script
if __name__ == '__main__':
    app.run(debug=True)

