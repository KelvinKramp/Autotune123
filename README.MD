# Autotune123

Autotune123 is a web application for type 1 diabetics to configure their insuline pump basal rate. It relies on the open source [OpenAPS Autotune algorithm](https://github.com/openaps/oref0), the 
Savitzky-Golay filter, and uses data from a personal [NightScout](https://nightscout.github.io/) websites as input to propose a 24-hour basal curve. 
You can see how it in action by going to www.autotune123.com and using the NightScout website url https://tig-diab.herokuapp.com as input.


## Screenshot
![screenshot](https://github.com/KelvinKramp/Autotune123/blob/master/assets/screenshot.png)

## Usage
You can use Autotune123 by going to www.autotune123.com and filling in your NightScout url and your API secret. Neither of the two are stored. 
If you don't want to use the website, you can install it on your 
computer by following the installation steps below.

## Installation
OpenAPS Autotune is based mainly on Javascript. This repository is written in Python. 

If you run it on your own computer, you have to follow the steps written over [here](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html) to install the Javascript OpenAPS Autotune.

After that install python, pip and git. There is an abundance of good tutorials on YouTube that guide you through the process. 
After installation of these applications run the following commands in your project directory:

```bash
git clone https://github.com/KelvinKramp/Autotune123
```


```bash
pip install -r requirements
```
and run the app:
```bash
python dash_app.py
```
It's easy to adjust the code so you don't have to fill in your NightScout url and API secret.  

## Contributing

Feature requests, suggestions and pull requests are very much appreciated and welcome!

## License
[MIT](https://choosealicense.com/licenses/mit/)
