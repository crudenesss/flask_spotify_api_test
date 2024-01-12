# Flask application using Spotify API

Just a simple website coded with Flask framework and Spotify API. Launched with Docker compose tool. Website is also configured with nginx and uses ssl certificates.

### Dependencies
- Docker
- OpenSSL(if you want to set up your own certificates)

### Preparations
#### 1. Getting credentials from Spotify developer website
In order to use Spotify API, sign up [here](https://developer.spotify.com/) in order to get developer account and then follow the instructions.\
After creating an instance, you will be provided with client ID and client secret.

#### 2. Setting up your docker-compose file
Provide your own credentials where needed inside `docker-compose.yml` file. Provide here credentials from previous step as well.\
Here you just have to type in your own application key:
```
      - KEY=<YOUR APPLICATION KEY>
```
#### 3. Nginx stuff (Optional)
 Place your configuration file and certificates in **nginx** directory, as shown in `docker-compose.yml`. My example configuration file for setting up nginx as reverse proxy and providing SSL certificates:
```
worker_processes  4;
events {
    worker_connections  1024;
}
http {
    server {
        listen       80;
        server_name  your-domain.com;
        return 301 https://$host$request_uri;
    }
    # HTTPS server
    server {
        listen       443 ssl;
        server_name  your-domain.com;

        ssl_certificate      /etc/nginx/cert.pem;
        ssl_certificate_key  /etc/nginx/key.pem;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
          proxy_pass          http://flask:5000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

```
### Launching
Launch with command:
```
docker compose up -d
```
### Enjoy :^)




