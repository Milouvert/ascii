# sample installation script on macos / linux

touch ./ascii
echo "#! /usr/bin/python3" > ./ascii
cat ./main.py >> ./ascii
chmod +x ./ascii

LINK_PATH="/usr/local/bin/ascii"

rm -f $LINK_PATH
ln -s "$PWD/ascii" $LINK_PATH

echo "Created symlink at ${LINK_PATH}"
