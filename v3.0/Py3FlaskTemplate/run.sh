#!/bin/bash
echo Script has Started.
requiredpackages=("sudo python3 python3-venv")
for requiredpackage in $requiredpackages
do
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $requiredpackage|grep "install ok installed")
	echo Checking for $requiredpackage: $PKG_OK
	if [ "" = "$PKG_OK" ]; then
		echo "No $requiredpackage. Setting up $requiredpackage."
		sudo apt-get --yes install $requiredpackage
	fi
done
python3 -m venv .venv
source .venv/bin/activate
which python
pippacks=("pip flask flask_wtf")
for pippack in $pippacks
do
	python3 -m pip install --upgrade $pippack
done
python3 ./main.py
echo Script has Stopped. 
