from app import app

# This app contains a convulted way to run a dashapp on nginx server
# the tutorial with explanation of how this works and why it is necessary
# can be found in this link:
# https://hackersandslackers.com/plotly-dash-with-flask/

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)