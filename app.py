import os
from flask.wrappers import Response
import requests
from os import path
from dotenv import load_dotenv
from flask import Flask, render_template, session
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


if __name__ == '__main__':
    app.run(debug=True)
