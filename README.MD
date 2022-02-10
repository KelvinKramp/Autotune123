# Autotune123

Autotune123 is a web application made for configuring insuline basal rates. It relies on the [OpenAPS Autotune algorithm](https://github.com/openaps/oref0)
and gets it data from [NightScout](https://nightscout.github.io/).

## Screenshot
![screenshot](https://github.com/KelvinKramp/Autotune123/blob/master/assets/screenshot.png)

## Usage
You can use online Autotune123 by going to this (link will follow) website or you can install it on your 
computer by following the installation steps beneath.



## Installation

If you run it on your own computer, you have to go through the steps written over [here](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html) to install OpenAPS Autotune. 

After that clone this repository. 
```bash
git clone https://github.com/KelvinKramp/Autotune123
```
Then use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements
```
Run the app:
```bash
python dash_app.py
```

## Contributing

If you have questions or find a bug you can also contact me on: k.h.kramp@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)