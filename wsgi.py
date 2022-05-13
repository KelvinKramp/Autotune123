from app import app
import os
from dotenv import load_dotenv

load_dotenv()


# This app contains a convulted way to run a dashapp on nginx server
# the tutorial with explanation of how this works and why it is necessary
# can be found in this link:
# https://hackersandslackers.com/plotly-dash-with-flask/

if __name__ == "__main__":
    if os.environ.get("ENV") == "development":
        app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
