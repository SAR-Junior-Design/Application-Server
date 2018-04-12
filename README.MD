# Icarus HTTP Backend

## Installation Guide for Icarus
### Pre-Requisites

Install Postgresql, see https://www.postgresql.org/download/

### Download



### Dependencies



### Build



### Installation



### Run
[still splitting this up]

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

Link nginx server: sudo ln -s /etc/nginx/sites-available/web-server /etc/nginx/sites-enabled

Link nginx server: sudo ln -s /etc/nginx/sites-available/app-server /etc/nginx/sites-enabled

## Release Notes for Icarus
### New Features

<ul>
  <li></li>
</ul> 

### Bug Fixes

<ul>
  <li></li>
</ul>

### Known Bugs

<ul>
  <li></li>
</ul> 
