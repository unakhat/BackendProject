import json
from flask import Flask, render_template, json, request, Response, jsonify, flash
import queries as query
from flask_mysqldb import MySQL
import database as db
import requests



app = Flask(__name__)


app.config.update(dict(
    DATABASE='spatialforce',
    USERNAME='spatialforce',
    HOST='127.0.0.1',
    PASSWORD='09j5fgt'
))

mysql = MySQL(app)


@app.route("/")
def index():
    # return app.send_static_file("index.html")
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_default():
    houseValue = ""
    incomeValue = ""
    populationValue = ""
    educationValue = ""
    return render_template('search.html', houseValue=houseValue, incomeValue=incomeValue, populationValue=populationValue, educationValue=educationValue)

@app.route('/google', methods=['GET'])
def google_default():

    return render_template('google_zip.html')

@app.route('/google', methods=['POST'])
def google():

    zipCode = str(request.form['zipCode'])
    data = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={zipCode}&key=AIzaSyD5GiLT_Ny1Lrbad3IrMujyaTWaqMbllr4').json()
    print('-----------------------')
    print('City Geographical Features:')
    print(json.dumps(data, indent=2))
    # dataJson = json.dumps(data)
    # state = data['results'][0]['address_components'][3]['long_name']
    city_name  = data['results'][0]['address_components'][1]['long_name']

    # Enter your API key here
    api_key = "c6c29f0756c11924fedd6b244702cca4"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        print(f'\n{city_name} weather information:')
        print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))

    else:
        print(" City Not Found ")


    return "Success"


def post_json_endpoint(zipcode):

    try:
        conn = db.connect()
        cursor = conn.cursor(buffered=True)
        cursor.execute('''SELECT MAX(pid) FROM spatialforce.zipcode_log''')
        maxid = cursor.fetchone()
        cursor.execute('''INSERT INTO spatialforce.zipcode_log (pid, zip_code) VALUES (%s, %s)''', (maxid[0] + 1, zipcode))

        conn.commit()
        cursor.close()
        print("add zipcode to trend table successfully with code:" + zipcode)
        return 'success'

    except Exception as e:
        print(e)

    return 'fail'



@app.route('/search', methods=['POST'])
def search():

    zipCode = str(request.form['zipCode'])


    if(zipCode == ""):
        return jsonify({'error' : 'Missing data!'})

    # Updates zipcode logger
    post_json_endpoint(zipCode)

    housingpriceResult = query.get_avg_housingprice_by_zip(zipCode)
    totalPopulation    = query.get_population_byzip(zipCode)
    totalEduction      = query.get_number_college_grad_byzip(zipCode)
    AverageIncome      = query.get_avg_income_byzip(zipCode)

    # DEBUGGG
    if housingpriceResult[0][0]:
        print("house value: " + str(int(housingpriceResult[0][0])))
    if totalPopulation[0][0]:
        print("population: " + str(int(totalPopulation[0][0])))
    if totalEduction[0][0]:
        print("education: " + str(int(totalEduction[0][0])))
    if AverageIncome[0][0]:
        print("income: " + str(int(AverageIncome[0][0])))

    variableList = [totalPopulation, housingpriceResult,totalEduction, AverageIncome ]

    if any(elem[0][0] is None for elem in variableList):
        # data = {
        #     "houseValue": "N/A",
        #     "incomeValue": "N/A",
        #     "populationValue": "N/A",
        #     "educationValue": "N/A"
        # }
        # return jsonify(data)
        return jsonify({'error' : 'Missing data!'})

    else:
        data = {
            "houseValue": int(housingpriceResult[0][0]),
            "incomeValue": int(AverageIncome[0][0]),
            "populationValue": int(totalPopulation[0][0]),
            "educationValue": int(totalEduction[0][0])
        }
        return jsonify(data)


@app.route('/rank', methods=['GET'])
def rank_default():
    data = {
        "top": [],
        "bottom": []
      }
    return render_template('rank.html', data=data)

@app.route('/rank', methods=['POST'])
def rank():
    click_type = request.form['type']
    print(click_type)
    data = query.rank_query(click_type)

    queryValid = 1
    if queryValid:
        return jsonify(data)

    return jsonify({'error' : 'Missing data!'})

@app.route('/trend', methods=['GET'])
def trend():
    trendTableData = query.zipcode_log()
    return render_template('trend.html', data=trendTableData)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/users")
def users():
    return jsonify(query.get_data())


@app.route("/api/zipcode_log")
def zipcodeLog():
    return jsonify(query.zipcode_log())




if __name__ == "__main__":
    app.run()
