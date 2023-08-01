#!/usr/bin/env python3
"""Display the current time"""
import locale
import pytz.exceptions
from pytz import timezone
from flask import Flask,render_template,request,g
from flask_babel import Babel
from typing import Dict, Union
from datetime import timezone as tmzn
from datetime import datetime

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configure available languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

def get_user():
    """
    Returns a user dictionary or None if ID value can't be found
    or if 'login_as' URL parameter was not found
    """
    id = request.args.get('login_as', None)

    if id is not None and int(id) in users.keys():
        return users.get(int(id))
    return None

@app.before_request
def before_request():
    """Add user to flask.g"""
    user = get_user()
    g.user = user

    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))

    # set time locale
    locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))

    time_format = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(time_format)

@babel.localeselector
def get_locale():
    """Retrieves and force locale"""
    loc = request.args.get('locale')

    if loc in app.config['LANGUAGES']:
        return loc
    
    if g.user:
        loc = g.user.get('locale')
        if loc and loc in app.config['LANGUAGES']:
            return loc
        
    loc = request.headers.get('locale', None)

    if loc is not None and loc in app.config['LANGUAGES']:
        return loc
    
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Infer timezone"""
    timezn = request.args.get('timezone', None)
    if timezn:
        try:
            return timezone(timezn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            timezn = g.user.get('timezone')
            return timezone(timezn).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    tm_zone = app.config['BABEL_DEFAULT_TIMEZONE']
    return tm_zone

@app.route('/', strict_slashes=False)
def index() -> str:
    """/ route"""
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
