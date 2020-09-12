# Cloudflare Integration

The following procedure will enable Cloudflare integration, so that when the server boots
it automatically registers its IP address with Cloudflare:

Create /home/ubuntu/cloudflare.config:

```
cloudflare_auth_email=(Cloudflare login email address)
cloudflare_auth_key=(Cloudflare Global API Key)
```

Install cloudflare service and enable:

```
sudo cp cloudflare.service /etc/systemd/system
cd /etc/systemd/system
sudo systemctl enable cloudflare
```

