# Lecture code snippets

I will use this file to mention installation requirements for lecture demos and also any code snippets that I will be copy/pasting during the lecture demo.

## Fri, Sept 20 (MySQL 2):

#### Retrieve the names of all songs along with their artists.

#### Find the songs that have more than 1 million streams.
1000000

#### What are the top 10 songs by the highest charting position?

#### Find the number of songs by each artist.

#### Find the genres that have more than 100 songs.

#### What are the top 10 popular songs that have a popularity score above 80?

#### What is the average streams for songs in each genre

#### Which artist has the most followers?

#### Which songs got released after 2020?

#### Which are the top 5 longest songs?

#### Which song has the highest danceability?

#### What is the average loudness of all songs?

#### Which are the top 5 genres with the highest average energy?

#### Find songs with a valence (happiness) score above 0.8.

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
