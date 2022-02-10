 # save profile local
 mkdir ~/myopenaps
 mkdir ~/myopenaps/settings
 python googlecloud-autotune/get_profile.py

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
 echo "STEP 10"
 sudo apt-get install bc


 # download javascript autotune pacakage and install node
 echo "STEP 11"
 mkdir ~/src
 cd ~/src && git clone -b dev git://github.com/openaps/oref0.git || (cd oref0 && git checkout dev && git pull)
 echo "STEP 12"
 cd ~/src/oref0
 sudo apt-get install -y npm
 sudo npm run global-install
 cd ~/

# run autotune -> *** THIS IS THE STEP THATS NOT WORKING
#sudo oref0-autotune --dir=~/myopenaps  --ns-host=NS_HOST --start-date=2021-12-30
