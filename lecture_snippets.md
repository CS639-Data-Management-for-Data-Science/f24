# Lecture code snippets

I will use this file to mention installation requirements for lecture demos and also any code snippets that I will be copy/pasting during the lecture demo.

## Fri, Nov 8 (dbt):

sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

docker pull ghcr.io/dbt-labs/dbt-snowflake:latest


## Fri, Oct 4 (MongoDB):

#### Installations on your VM:

```
pip3 install jupyter pandas nbformat nbconvert
pip3 install pymongo 
pip3 install geopandas matplotlib
```

#### Docker clean up

```
docker system prune
docker rm `docker ps -aq`
docker rmi -f `docker images -aq` (force removes stale images)
```
```
docker pull mongo
docker run --name <container-name> -d -p 127.0.0.1:27017:27017 mongo
```
```
docker exec -it <CONTAINER NAME> bash
```

--------------------------------

## Mon, Sept 16 (MySQL):

#### Installations on your VM:

Stop your VM, refresh your window after a few minutes, and “Start / Resume” to update kernel version

``` 
sudo apt-get update
sudo apt-get install python3-pip wget unzip
```
```
sudo pip3 install jupyter
pip3 install SQLAlchemy mysql-connector-python pandas
pip3 install pandas
```

#### Docker clean up

```
docker system prune
docker rm `docker ps -aq`
docker rmi -f `docker images -aq` (force removes stale images)
```
```
docker pull mysql
docker run -d -m "1g" -p 127.0.0.1:3306:3306 -e MYSQL_DATABASE=cs639 -e MYSQL_ROOT_PASSWORD=abc mysql
```
```
docker exec -it \<CONTAINER NAME\> bash
```

```
mysql -p cs639
help
show tables;

git pull (inside your f24 directory)
# Note: navigate to today's lecture directory within your f24 directory
jupyter notebook
```

#### Establish ssh tunnel (from your laptop to your VM):
```
ssh USER@<IP> -L localhost:8888:localhost:8888
```
