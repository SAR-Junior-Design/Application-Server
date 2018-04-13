# Icarus HTTP Backend

## Installation Guide for Icarus 1.0

### Make

If you're running on Ubuntu, you can run the make file in the root directory and download all of the necessary dependencies. 

```make install-dependencies```

### Pre-Requisites

Install Postgresql, see https://www.postgresql.org/download/

### Download

Download repository, see https://github.com/SAR-Junior-Design/Application-Server

### Python Setup

A virtual environment is not necessary, but might be helpful if there are other projects on your server.

Install dependencies by going into the Flask/ repository, and then running:

``` pip3 install -r requirements.txt ```

### Database Setup

In the terminal type in:

``` psql postgres; ```

Once you're in the postgres terminal.

```
CREATE USER ubuntu;
CREATE DATABASE sar;
GRANT ALL PRIVILEGES ON SAR TO ubuntu;
```

### Run
[still splitting this up]

Through Postgres, setup a new user named Ubuntu. Make the password to that user "elephants_remember_1984"
(this makes sure it's consistent with the backend code).


```
type this command in;
create database sar;
Grant ubuntu all privileges;
grant all privileges on database sar to ubuntu;
```

Then in main.py, make sure that db.create_all() is not commented out. This creates the tables.

Run the code once, then turn off the server. The tables should be made in the database now.

Open the sar database with the command:

```psql sar;```

Run this sql script to create the first user:

Insert into users values ('samcrane8@gmail.com','kaan','lawrence',CURRENT_TIMESTAMP,'admin');

Now the first user exists. 

Link nginx server: sudo ln -s /etc/nginx/sites-available/web-server /etc/nginx/sites-enabled

Link nginx server: sudo ln -s /etc/nginx/sites-available/app-server /etc/nginx/sites-enabled

## Release Notes for Icarus 1.0
### New Features

<ul>
  <li>Filters for get_missions()</li>
  <li>SSL security is setup. Now HTTP is disallowed and HTTPS is the only option. </li>
  <li>Back-end API is exposed at backend.icarusmap.com, and front-end SPA is exposed at icarusmap.com </li>
</ul> 

### Bug Fixes

<ul>
  <li>Status codes for most API calls were updated and fixed to be more descriptive. Now the proper status code is sent along with a descriptive message.</li>
</ul>

### Known Bugs

<ul>
  <li>Versioning system is wrong, we need to transition to a better versioning system.</li>
  <li>Get active missions doesn't work.</li>
  <li>Get recent missions doesn't work.</li>
</ul> 
