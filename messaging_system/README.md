### Injections Laboratory

# injections to POST form
Arthur' -- -
a' OR 'b'='b
a' OR True LIMIT 2,1 -- - 

# boolean-based injections
// to be completed

# time-based injections
// to be completed

### SETUP
# install docker
docker stop mysql-container
docker start MySQL-container

# start MySQL
mysql -h 172.17.0.2 -u root -p

# start php Server in the server_side repo/directory
php -S 0.0.0.0:1234

# TODO:
check the last slides to perform injections on the search.php and password_recovery.php

...