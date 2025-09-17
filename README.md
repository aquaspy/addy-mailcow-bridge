# Addy-Mailcow-Bridge

A simple Flask-based bridge API service that generates random email aliases and creates them via the Mailcow API. This project is designed for self-hosting enthusiasts who want to automate email alias creation connection the official Bitwarden extension with Mailcow API by using the same endpoints of Addy.io to ensure it is compatible on the Bitwarden extension. 

## Features
- **Random Alias Generation**: Creates cryptographically secure, URL-safe email aliases.
- **Mailcow Integration**: Directly interacts with the Mailcow API to add aliases.
- **Dockerized**: Fully containerized for easy deployment.
- **Lightweight**: Uses Waitress as the WSGI server for production-ready performance.

## Prerequisites
- A Mailcow instance with API access (API Admin key required).
- Bitwarden extension (you can use the official bitwarden instance of self host your own vaultwarden/Bitwarden Cloud.

## Installation without Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/addy-mailcow-bridge.git
   cd addy-mailcow-bridge
   ```

2. Create a ```.env``` file in the root directory:
   ```env
   MAILCOW_DOMAIN=https://your-mailcow-domain.com
   ```

   Replace ```https://your-mailcow-domain.com``` with your actual Mailcow domain.

4. Create an python environment and download the variables
   ```
   python3 -m venv .venv
   pip install -r requiriments.txt
   ```
5. Run the python app within the environment
   ```
   python3 app.py
   ```

## Running with Docker Compose
Docker Compose simplifies setup by handling environment variables and port mapping.

1. Download the docker-compose file from this repository.
2. Modify the file to ensure you have your domain set at the enviroment value. E.g MAILCOW_DOMAIN=https://mailcowdomain.com and start the container.
   ```bash
   docker-compose up
   ```
   - This pulls the image from Docker Hub (```theselfhostingart/addy-mailcow-bridge:v1```) and starts the container.
   - Access the API at ```http://localhost:6510```.

3. To run in the background:
   ```bash
   docker-compose up -d
   ```

4. Stop the application:
   ```bash
   docker-compose down
   ```

## Running with ```docker run```
For manual control or if you prefer not to use Compose.

1. Pull the image from Docker Hub:
   ```bash
   docker pull theselfhostingart/addy-mailcow-bridge:latest
   ```

2. Run the container:
   ```bash
   docker run -p 6510:6510 -e MAILCOW_DOMAIN=https://your-mailcow-domain.com theselfhostingart/addy-mailcow-bridge
   ```
   - Replace ```https://your-mailcow-domain.com``` with your actual Mailcow domain.
   - Access the API at ```http://localhost:6510```.

3. To run in the background, add the ```-d``` flag:
   ```bash
   docker run -d -p 6510:6510 -e MAILCOW_DOMAIN=https://your-mailcow-domain.com theselfhostingart/addy-mailcow-bridge
   ```

## Environment Variables
- **MAILCOW_DOMAIN**: The URL of your Mailcow instance (e.g., ```https://mail.example.com```). Required for API calls.

Pass additional variables via ```-e``` in ```docker run``` or add them to your ```.env``` file as needed.

## API Usage
Once your server is running, you can set the Bitwarden extension to use it at Generator -> Username - Forwarded Email Alias -> Addy.io as service -> put a domain that exists on Mailcow -> Put your MailCow API key -> Put your server URL with your destination email at the end. For example, if you want to receive your emails at mycoolemail@gmail.com, you can use something like this:
```
https://yourbridgeserver/mycoolemail@gmail.com
```

Here is a example of how it works:
<img width="368" height="428" alt="image" src="https://github.com/user-attachments/assets/ea9b0d83-ad7c-4293-b258-29d69b791772" />


Response:
```json
{
  "data": {
    "email": "random-alias@example.com"
  }
}
```

## Nginx example
```
# /etc/nginx/sites-available/addymailcowbridge
server {
    listen 80;
    server_name yourbridgedomain.com;

    location / {
        proxy_pass http://127.0.0.1:6510;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

I highly recommend using certbot to generate your SSL certificate. **Do not use plain HTTP with this bridge API**

## Cady example

```
yourdomain.com {
    reverse_proxy 127.0.0.1:6510
}

```

## Limitations
This project is really simple and direct. The goal is making it as small as possible to keep the code simple and easy to fix. The goal is not to make a complete API bridge to addy. Just the create ALIAS was covered to make it easy to use with Bitwarden extension and app.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

