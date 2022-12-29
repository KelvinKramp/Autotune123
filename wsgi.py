from app import app
from definitions import development


# This app contains a convuluted way to run a dashapp on nginx server
# the tutorial with explanation of how this works and why it is necessary
# can be found in this link:
# https://hackersandslackers.com/plotly-dash-with-flask/
print(development)
if __name__ == "__main__":
    if development:
        app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
