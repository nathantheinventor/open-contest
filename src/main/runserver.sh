cat /etc/nginx/sites-enabled/nginx.conf
ls /etc/nginx/sites-enabled/
/etc/init.d/nginx start
systemctl status nginx.service
uwsgi --http :8001 --module code
