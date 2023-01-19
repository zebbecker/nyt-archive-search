#!/bin/bash
set -e
echo -e "\n>>> Copying Django project files to server."

if [[ -z "$SERVER" ]]
then 
    echo "Error: No value set for SERVER."
    exit 1
fi

echo -e "\n>>> Preparing scripts locally."
rm -rf deploy
mkdir deploy
cp -r config deploy 
cp -r scripts deploy
cp -r gatherer deploy
cp -r nyt_archive_search deploy 
cp requirements.txt deploy
cp manage.py deploy

echo -e "\n>>> Copying files to the server."
ssh root@$SERVER "rm -rf /root/deploy/"
scp -r deploy root@$SERVER:/root/

echo -e "\n>>> Cleaning deployed files on server."
ssh root@$SERVER /bin/bash << EOF
    set -e
    find /root/deploy/ -name *.pyc -delete
    find /root/deploy/ -name __pycache__ -delete
EOF

echo -e "\n>>> Copied files to server: "
ssh root@$SERVER "tree deploy"

echo -e "\n>>> Finished copying Django project files to server."