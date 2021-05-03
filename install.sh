mkdir ocr-project
cd ocr-project

apt-get update
apt-get install python3 pip3

sudo pip3 install --upgrade pip
pip install --upgrade google-cloud-vision google-cloud-storage

# Add the name of your credential file
export GOOGLE_APPLICATION_CREDENTIALS=$1