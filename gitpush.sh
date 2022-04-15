#!/bin/sh
pip freeze > requirements.txt
git add .
git commit -am "update"
git push origin master