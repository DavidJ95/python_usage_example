#! /bin/bash
echo $1
cd ./src
if [ -d ".venv" ]; then rm -Rf .venv; fi
echo "Danner env"
"${1}" -m venv .venv
source .venv/Scripts/activate
cp ../pip.ini .venv
echo "Installerer PyPi pakker"
python -m pip install -r ../requirements.txt