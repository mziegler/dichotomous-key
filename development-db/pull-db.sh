# copies the database from the server to your local machine

if [ "$1" != "" ]; then
  scp $1@key-mziegler.rhcloud.com:$(ssh $1@key-mziegler.rhcloud.com 'printf $OPENSHIFT_DATA_DIR')/db.sqlite3 .
else
  echo "This downloads the sqlite database from the OpenShift deployment and copies it to this folder.  (So you can run the app locally on your own machine, and modify the database locally.)  It takes the hash from the ssh command (from clicking the 'Want to log into your application?' link on the OpenShift application page) as a command-line argument."
fi
