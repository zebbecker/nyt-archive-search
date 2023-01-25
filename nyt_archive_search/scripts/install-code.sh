#!/bin/bash
# Install Django app on server
set -e 
echo -e "\n>>> Installing Django project on server."

if [[ -z "$SERVER" ]]
then 
    echo "Error: No value set for SERVER."
    exit 1
fi

ssh root@$SERVER /bin/bash << EOF
    set -e 

    echo -e "\n>>> Stopping Gunicorn."
    cd /app/ 
    . env/bin/activate
    ./scripts/super.sh stop gunicorn 

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

    echo -e "\n>>> Installing Python packages."
    pip install -r /app/requirements.txt

    echo -e "\n>>> Collecting new static files."
    ./manage.py collectstatic

    echo -e "\n>>> Re-reading supervisord config."
    ./scripts/super.sh reread

    echo -e "\n>>> Starting Gunicorn."
    ./scripts/super.sh start gunicorn
EOF

echo -e "\n>>> Finished installing Django project on server"