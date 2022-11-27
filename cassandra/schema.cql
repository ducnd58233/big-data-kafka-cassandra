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

CREATE TABLE twitterdata (
  tweet_date TIMESTAMP,
  location TEXT,
  tweet TEXT,
  classification TEXT,
  PRIMARY KEY (location, tweet_date)
);

CREATE TABLE twitter2data (
  tweet_date TIMESTAMP,
  location TEXT,
  tweet TEXT,
  classification TEXT,
  PRIMARY KEY (location, tweet_date)
);

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