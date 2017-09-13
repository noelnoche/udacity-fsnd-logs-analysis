Logs Analysis
===
<br>


Synopsis
---
This is a study of SQL query strategies using PostgreSQL and Python's
`psycopg2` database adapter. The goal is to build an internal reporting
tool that connects to a large database and filter data to present useful
information to the user.

This program answers three questions based on data from a news database:

1. What are the top three popular articles?
2. Who are the most popular authors of all time?
3. On what dates did article request errors exceed one percent? 


Result Screenshot
---
![Result Screenshot](https://github.com/noelnoche/udacity-fsnd-logs-analysis/blob/master/screenshot.png)


Requirements
---
+ Python 2.7.x
+ VirtualBox
+ Vagrant


Installation & Setup
---
1. Install VirtualBox (See Reference section for link).
2. Install Vagrant (See Reference section for link).
3. Download and extract `udacity-fsnd-logs-analysis` file.
4. Open your terminal application.
5. Run `cd vagrant`.
6. Unzip `newsdata.zip`.
7. Run the following commands:
    + `vagrant up` (Installs the virtual Linix OS)
    + `vagrant ssh`
    + `cd /vagrant` (virtual shared folder)
    + `psql -d news -f newsdata.sql` (Builds the 'news' database)
8. To disconnect and shut down Vagrant, run the following commands:
    + `exit`
    + `vagrant halt`


How to Use
---

**From main.py**  

1. Open your terminal application.
2. `cd` to `udacity-fsnd-logs-analysis/vagrant`.
3. Run the following commands: 
    + `vagrant up`
    + `vagrant ssh`
    + `cd /vagrant`
    + `python main.py`

**From psql command prompt**  

1. Run `psql` then `\c news`.
2. Run the following commands for each question:
    + `select * from top_articles limit 3`
    + `select * from top_authors`
    + `select * from error_reporter`

**clear\_views.py**  
This utility removes all the views that were created by `main.py`.

1. `cd` to `udacity-fsnd-logs-analysis/vagrant`.
2. Run `python clear_views.py`.


Credits
---
+ Database provided by [Udacity](https://www.udacity.com)


License
---
Code provided under an [MIT license](https://github.com/noelnoche/udacity-fsnd-logs-analysis-website/blob/gh-pages/LICENSE.md)


Reference
---
+ [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
+ [Vagrant](https://www.vagrantup.com/downloads.html)
+ [PostgreSQL for Development with Vagrant](https://wiki.postgresql.org/wiki/PostgreSQL_For_Development_With_Vagrant)
