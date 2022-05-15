cp -R Autotune123/* ./
sudo service nginx stop
pkill gunicorn
sudo systemctl stop app
sudo systemctl daemon-reload
sudo nginx -t
sudo systemctl start app
sudo systemctl enable app
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'