# API:
- Task 1: Open weather map (owm-producer):
    - This task I use United Kingdom and Singapore location
    - The table columns:
```
CREATE TABLE weatherreport (
  forecastdate TIMESTAMP,
  location TEXT,
  description TEXT,
  temp FLOAT,
  feels_like FLOAT,
  temp_min FLOAT,
  temp_max FLOAT,
  pressure FLOAT,
  humidity FLOAT,
  wind FLOAT,
  sunrise BIGINT,
  sunset BIGINT,
  PRIMARY KEY (location, forecastdate)
);
```
- Task 2: Faker API
    - The table columns:
```
CREATE TABLE IF NOT EXISTS fakerdata (
  name TEXT,
  address TEXT,
  year INT,
  job TEXT,
  phone TEXT,
  email TEXT,
  company TEXT,
  credit_card_number TEXT,
  credit_card_expire TEXT,
  credit_card_provider TEXT,
  PRIMARY KEY (name, address)
);
```
- Task 3: Twitter API (2.0)
    - This task I use United Kingdom and Singapore location
    - The table columns:
```
CREATE TABLE twitter2data (
  tweet_date TIMESTAMP,
  location TEXT,
  tweet TEXT,
  classification TEXT,
  PRIMARY KEY (location, tweet_date)
);
```

# Command
## **Notes**: after running cassandra, need to wait for a while (about 3-5 minutes) before running kafka again (including `up` or `build`)
- When this is the first time you run this repository
  - Create network
``` bash
$ docker network create kafka-network
$ docker network create cassandra-network
```
  -  Running docker-compose by the following orders
``` bash
$ docker-compose -f cassandra/docker-compose.yml up
$ docker-compose -f kafka/docker-compose.yml up
$ docker-compose -f owm-producer/docker-compose.yml up
$ docker-compose -f twitter-producer2/docker-compose.yml up
$ docker-compose -f faker-producer/docker-compose.yml up
$ docker-compose -f consumers/docker-compose.yml up
$ docker-compose -f data-vis/docker-compose.yml up
```
- When you update files, stop (`down`) containers first then `up` with `--build` flag (remember to replace 'your-folder-name'):
```
$ docker-compose -f 'your-folder-name'/docker-compose.yml down
$ docker-compose -f 'your-folder-name'/docker-compose.yml build
```
- However, with cassandra and kafka, when you want to update files, you need to stop (`down`) `containers` and delete the current `containers` and the `images` then close the `docker desktop`. **`SHUT DOWN`** (not RESTART) your device, wait for few minutes (around 5-10m) and then start your device again.
- Sometimes the kafka has problem, you just need to restart again