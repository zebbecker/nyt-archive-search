#!/bin/bash
set -e 
# Sets up new server to host Django app
export SERVER=159.203.178.166

DJANGO_SETTINGS_MODULE = "nyt_archive_search.settings.prod"

if [[ -z "$1" ]]
then 
    echo "Error: No value set for DJANGO_SECRET_KEY, argument required."
    echo "Usage: ./setup-server.sh [your_secret_key]"
    exit 1
else 
    DJANGO_SECRET_KEY="$1"
fi

echo -e "\n>>> Setting up $SERVER"
ssh root@$SERVER /bin/bash << EOF
    set -e 

    echo -e "\n>>> Updating apt source."
    apt-get -qq update

    echo -e "\n>>> Upgrading apt packages."
    apt-get -qq upgrade

    echo -e "\n>>> Installing apt packages."
    apt-get -qq install python3-pip tree 

    echo -e "\n>>> Installing virtualenv."
    pip3 install virtualenv

    echo -e "\n>>> Setting up project folder."
    mkdir /app/
    mkdir /app/logs

    echo -e "\n>>> Creating virtualenv."
    if [[ ! -d "/app/env" ]]
    then
        virtualenv -p python3 /app/env
    else
        echo -e "\n>>> Skipping virtualenv creation - already present."
    fi

    echo -e "\n>>> Setting system environment variables."

    if [[ "\$DJANGO_SETTINGS_MODULE" != "$DJANGO_SETTINGS_MODULE" ]]
    then
        echo "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE" >> /etc/environment
    else 
        echo -e "\n>>> Skipping DJANGO_SETTINGS_MODULE - already present"
    fi

    if [[ "\$DJANGO_SECRET_KEY" != "$DJANGO_SECRET_KEY" ]]
    then
        echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" >> /etc/environment
    else 
        echo -e "\n>>> Skipping DJANGO_SECRET_KEY - already present"
    fi

EOF

./scripts/upload-code.sh

ssh root@$SERVER /bin/bash << EOF
    set -e 
    
    echo -e "\n>>> Deleting old files." 
    rm -rf /app/config
    rm -rf /app/scripts
    rm -rf /app/gatherer
    rm -rf /app/nyt_archive_search
    rm -rf /app/staticfiles
    rm /app/requirements.txt
    rm /app/manage.py

    echo -e "\n>>> Copying new files."
    cp -r /root/deploy/config /app/
    cp -r /root/deploy/scripts /app/
    cp -r /root/deploy/gatherer /app/
    cp -r /root/deploy/nyt_archive_search /app/
    cp /root/deploy/requirements.txt /app/
    cp /root/deploy/manage.py /app/

    echo -e "\n>>> installing Python packages"
    cd /app/ 
    . env/bin/activate
    pip install -r requirements.txt

    echo -e "\n>>> Collecting static files"
    ./manage.py collectstatic

    echo -e "\n>>> Starting supervisord"
    supervisord -c config/supervisord.conf
EOF

echo -e "\n>>> Finished setting up $SERVER"