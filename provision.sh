#!/bin/bash
set -e

aptitude update
aptitude install nginx-full -y

mkdir -p /srv/data /var/run/apache2-dav
chown www-data:www-data /srv/data /var/run/apache2-dav

cat << 'EOF' > /etc/nginx/sites-available/default
server {
  listen 8000;
  root /srv/data;
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

aptitude install apache2 -y
a2enmod dav
a2enmod dav_fs

cat << 'EOF' > /etc/apache2/sites-available/default
DavLockDB /var/run/apache2-dav/davlock.db
ServerName localhost

<VirtualHost *:80>
  DocumentRoot /srv/data

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


service nginx restart
service apache2 restart