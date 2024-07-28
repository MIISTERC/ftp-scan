echo "---------------------------------------------------------------"
echo "Setup Script for Ftp-scan"
echo "---------------------------------------------------------------"
if [[ $(id -u) -ne 0 ]]; then
	echo "please run this script as root!"
	exit 1
else
	if [[ -e /usr/bin/ftpscan ]]; then
		echo "/usr/bin/ftpscan exists! You already ran the setup file earlier!"
		exit 1
  	else
		echo "installing essential python libraries..."
		pip3 install -r requirements.txt
		echo "Creating Symbolic link...."
		cdir=$(pwd)
		path=$cdir/ftpscan.py
		sudo ln -s "$path" /usr/bin/ftpscan 
		chmod +x /usr/bin/ftpscan
		echo "Setup Done! now execute ftpscan"
		ftpscan -h
	fi 
fi
