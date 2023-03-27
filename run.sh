#command for me to run in cloud vm
docker run --env-file environment_variables -d -p 3306:3306 --name MepML -t mysql_mepml