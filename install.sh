echo "Step 0"
# copy to user dir
cd /home/ubuntu || exit
cp -r /home/ubuntu/Autotune123/{,.[^.]}* /home/ubuntu || exit
# and make directories
mkdir ~/myopenaps
mkdir ~/myopenaps/settings

# install dependencies
echo "STEP 1"
sudo apt-get -o Acquire::ForceIPv4=true install -y
echo "STEP 2"
sudo apt-get -o Acquire::ForceIPv4=true update && sudo apt-get -o Acquire::ForceIPv4=true -y upgrade
echo "STEP 3"
sudo apt-get -o Acquire::ForceIPv4=true install -y git python python-dev software-properties-common python-numpy python-pip nodejs-legacy npm watchdog strace tcpdump screen acpid vim locate jq lm-sensors bc
echo "STEP 4"
sudo apt-get install bc
echo "STEP 5"
sudo pip install -U openaps
echo "STEP 6"
sudo pip install -U openaps-contrib
echo "STEP 7"
sudo openaps-install-udev-rules
echo "STEP 8"
sudo activate-global-python-argcomplete
echo "STEP 9"
npm install -g json oref0
echo "step 10"
sudo apt-get install -y jq



# download javascript autotune pacakage and install node
echo "STEP 10"
mkdir ~/src
cd ~/src && git clone -b dev git://github.com/openaps/oref0.git || (cd oref0 && git checkout dev && git pull)
echo "STEP 11"
cd ~/src/oref0 || exit
sudo apt-get install -y npm
sudo npm run global-install

# upgrade operating system
cd /home/ubuntu || exit
sudo apt-get -y update
sudo apt-get -y upgrade

# install python build packages
sudo apt-get install -y python3-pip python3-venv build-essential libssl-dev libffi-dev python-dev

# activate virtual environment and install python packages
python3 -m venv venv
echo 'virtual environment created'
source venv/bin/activate
echo 'virtual environment activated'
pip3 install -r requirements.txt
echo 'installed requirements'

# install gunicorn
pip3 install gunicorn
echo 'installed gunicorn'
cd ~ || exit

