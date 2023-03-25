#for me in cloud vm
docker run --env-file env -p 10.128.0.2:3306:3306 --name MepML -t mysql_mepml