from flask import Flask, request, make_response, render_template
from datetime import date, datetime, timedelta
import json
import requests
import re
from linkedin import linkedin
import settings

app = Flask(__name__)

# ROUTES
@app.route('/')
def index():
  # Instantiate the linkedin developer authentication class
  authentication = linkedin.LinkedInDeveloperAuthentication(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, 
                                                            settings.USER_TOKEN, settings.USER_SECRET, 
                                                            settings.RETURN_URL, linkedin.PERMISSIONS.enums.values())

  # Pass it in to the app...
  application = linkedin.LinkedInApplication(authentication)

  f = open('data/linkedin_profiles.json', 'rb')
  people_urls = json.loads(f.read())
  f.close()

  profiles = []
  selectors=['id', 'first-name', 'last-name', 'location', 'skills', 'educations']
  for person_url in people_urls:
    profiles.append(application.get_profile(member_url=person_url, 
                                            selectors=selectors))
  
  resp = make_response(json.dumps(profiles))
  resp.headers['Content-Type'] = 'application/json'
  return resp

# UTILITY
def render_app_template(template, **kwargs):
    '''Add some goodies to all templates.'''

    if 'config' not in kwargs:
        kwargs['config'] = app.config
    return render_template(template, **kwargs)

# INIT
if __name__ == "__main__":
    app.run(debug=True, port=9999)




