# copies the database from your local machine to the server

if [ "$1" != "" ]; then
  scp db.sqlite3 $1@key-mziegler.rhcloud.com:$(ssh $1@key-mziegler.rhcloud.com 'printf $OPENSHIFT_DATA_DIR')/db.sqlite3
else
  echo "This copies the database (db.sqlite3) from this folder to the OpenShift server.  (So you can modify the database on your own machine and then copy the changes to the server.  We want to keep the database out of the git repository.)  It takes the hash from the ssh command (from clicking the 'Want to log into your application?' link on the OpenShift application page) as a command-line argument."
fi
