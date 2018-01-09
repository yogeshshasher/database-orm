# database-orm

## Prerequisite
- Install Mysql 5.6 server or latest

## Django Project setup
```bash
$ git clone git@github.com:hashedin/database-orm.git
$ cd database-orm
$ virtualenv -p python .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```

## Database Setup
```bash
$ mysql -uroot -p
mysql> create datatbase database_orm;
```