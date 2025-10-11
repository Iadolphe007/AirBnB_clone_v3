# Deployment helper scripts

This project includes helper scripts to prepare an Ubuntu server with Nginx and to package/deploy the static web assets found in `web_static/`.

## 0-setup_web_static.sh

Bootstraps Nginx and creates the required folder structure under `/data`.

- Installs Nginx
- Creates `/data/web_static/releases/test` and `/data/web_static/shared`
- Writes a test `index.html`
- Creates `/data/web_static/current` symlink pointing to the latest release
- Adds an Nginx location `/hbnb_static/` that serves from `/data/web_static/current/`

Usage:

```bash
bash 0-setup_web_static.sh
# Then visit http://<server_ip>/hbnb_static/
```

## 1-pack_web_static.py

Creates a timestamped tarball of `web_static` in `versions/`.

```bash
python3 1-pack_web_static.py
# or from Python: from 1-pack_web_static import do_pack; do_pack()
```

Dependencies: Fabric 1.x API (use `fabric3` on Python 3).

## 2-do_deploy_web_static.py

Uploads a previously generated tarball to remote servers and configures the symlink.

- Hosts are configured in the script via `env.hosts`
- Uploads to `/tmp/`, extracts to `/data/web_static/releases/<timestamp>/`
- Moves content to release folder, updates `/data/web_static/current`

```bash
fab -f 2-do_deploy_web_static.py do_deploy:/path/to/web_static_YYYYmmddHHMMSS.tgz
```

## 3-deploy_web_static.py

Combines packing and deploying in one Fabric task.

```bash
fab -f 3-deploy_web_static.py deploy
```

[!NOTE]
Update `env.hosts` inside the scripts with your actual server IPs or names.
