# file to store docker commands
docker build -t pidjango .

sleep 20

docker run -dp 8081:8000 --name djangopi pidjango