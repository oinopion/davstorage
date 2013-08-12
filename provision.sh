#!/bin/bash
set -e

# install web servers
aptitude update
aptitude install nginx-full apache2 -y

# enable apache module
a2enmod dav
a2enmod dav_fs

# ensure directory exists
mkdir -p /vagrant/data

# setup conf files
cat << 'EOF' > /etc/nginx/sites-available/default
server {
  listen 8000;
  root /vagrant/data;
  server_name localhost;

  location / {
    autoindex on;
    dav_methods put delete mkcol;
    create_full_put_path on;

    limit_except GET {
      auth_basic "Vagrant DAV";
      auth_basic_user_file /vagrant/htpass;
    }
  }
}
EOF

cat << 'EOF' > /etc/apache2/sites-available/default
DavLockDB /var/tmp/apache2-davlock.db
ServerName localhost

<VirtualHost *:80>
  DocumentRoot /vagrant/data

  <Location />
    Dav on
    AuthType Basic
    AuthName "Vagrant DAV"
    AuthUserFile /vagrant/htpass

    <LimitExcept GET OPTIONS>
      Require valid-user
    </LimitExcept>
  </Location>

  LogLevel warn
  CustomLog ${APACHE_LOG_DIR}/access.log combined
  ErrorLog ${APACHE_LOG_DIR}/error.log
</VirtualHost>
EOF

# change web servers users to vagrant
sed -i 's/www-data/vagrant/' /etc/apache2/envvars
sed -i 's/www-data/vagrant/' /etc/nginx/nginx.conf

chown -R vagrant /var/lock/apache2

service nginx restart
service apache2 restart