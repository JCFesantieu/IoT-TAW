sudo apt-get install -y wget openssl python-pip
openssl genrsa -out rsa_private.pem 2048
openssl rsa -in rsa_private.pem -pubout -out rsa_cert.pem
wget https://pki.goog/roots.pem
