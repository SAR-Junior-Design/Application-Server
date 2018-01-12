# http_backend

## How to run locally:

### Setup

First, install Postgresql (here is the site: https://www.postgresql.org/download/)

Second, setup a new user named Ubuntu. Make the password to that user "elephants_remember_1984"
(this makes sure it's consistent with the backend code). 

type this command in:
create database sar;

Grant ubuntu all privileges: 
grant all privileges on database sar to ubuntu;

Then in main.py, make sure that db.create_all() is not commented out. This creates the tables.

Run the code once, then turn off the server. The tables should be made in the database now.

Open the sar database with the command:
psql sar;

Run this sql script to create the first user:

insert into users values ('samcrane8@gmail.com','kaan','lawrence',CURRENT_TIMESTAMP,'admin');

Now the first user exists. 

### Debugging

Things may break as the database is updated and the schema changes. When in doubt, delete the database and recreate it,
following the rules described above. 
