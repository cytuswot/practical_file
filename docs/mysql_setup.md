- Install mysql server and client 

(client is optional; only required if you want to use mysql CLI to operate on DB)

```
sudo apt install default-mysql-server default-mysql-client
```


- After installing you'll have to change the default password for the 'root' user

```
sudo mysql -u root

MariaDB [(none)]> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('password_sql');
MariaDB [(none)]> FLUSH PRIVILEGES;
```

- Log in to mysql using the password 
(To prevent shoulder-surfing, password is not visible)

```
mysql -u root -p
```