import os
from flask.wrappers import Response
import requests
from os import path
from dotenv import load_dotenv
from flask import Flask, render_template, session, make_response, jsonify
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm

base_dir = path.abspath(path.dirname(__name__))
load_dotenv(path.join(base_dir, '.env'))

app = Flask(__name__)
app.secret_key = "sosecerrt"
Bootstrap(app)


class CityForm(FlaskForm):
    """Create city form."""

    city = StringField("Enter City Name:")


@app.route('/')
def index():
    """Display home page."""
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """Get the weather of a city."""
    form = CityForm()
    if form.validate_on_submit():
        city = form.city.data
        API_KEY = os.environ.get('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url).json()

        if response.get('cod') != 200:
            message = response.get('message', '')
            return render_template('weather.html', form=form, message=message, city=city)
        curr_temp = response.get('main', {}).get('temp')
        if curr_temp:
            curr_temp_in_celsius = round(curr_temp - 273.15, 2)
            humidity = response.get('main', {}).get('humidity')
            pressure = response.get('main', {}).get('pressure')
            return render_template('weather.html',
                                   form=form,
                                   city=city,
                                   curr_temp_in_celsius=curr_temp_in_celsius,
                                   humidity=humidity,
                                   pressure=pressure)

    return render_template('weather.html', form=form)

@app.route('/covid19')
def covid19_worldwide_cases():
    """Display all covid19 cases across the globe."""
    url = "https://api.caw.sh/v3/covid-19/all"
    response = requests.get(url).json()

    cases = response.get('cases')
    todayCases = response.get('todayCases')
    deaths = response.get('deaths')
    todayDeaths = response.get('todayDeaths')
    recovered = response.get('recovered')
    todayRecovered = response.get('todayRecovered')

    worldwide_cases = {
        "cases": cases,
        "todayCases": todayCases,
        "deaths": deaths,
        "todayDeaths": todayDeaths,
        "recovered": recovered,
        "todayRecovered": todayRecovered
    }

    return render_template('covid19.html', worldwide_cases=worldwide_cases)


if __name__ == '__main__':
    app.run(debug=True)
