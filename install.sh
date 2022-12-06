# sample installation script on macos

touch ./ascii
echo "#! /usr/bin/python3" > ./ascii
cat ./main.py >> ./ascii
chmod +x ./ascii

rm /usr/local/bin/ascii
ln -s "$PWD/ascii" /usr/local/bin/ascii