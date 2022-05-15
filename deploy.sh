rm -rf Autotune123
git clone https://github.com/KelvinKramp/Autotune123.git
cp -R Autotune123/* ./
source venv/bin/activate
pip install -R requirements.txt
sudo service nginx stop
pkill gunicorn
sudo systemctl stop app
sudo systemctl daemon-reload
sudo nginx -t
sudo systemctl start app
sudo systemctl enable app
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'