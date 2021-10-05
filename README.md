# Installation

* create installation directory at `/opt/captionator`
* create a virtual env
```bash
cd /opt/captionator/
python3 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install .
```
* start with `/opt/captionator/venv/bin/captionator`

# Starting the Service
* You'll need a SQL compatible server
  * create a captionator user in the mysql db
  * cp `sample.ini` to `captionator.ini`
  * update `captionator.ini` to reference correct db server
* You'll need a local service user on your host machine
  ```bash
  useradd -M captionator
  usermod -L captionator
  chmod -R captionator:captionator /opt/captionator
  ```
* In order to use the google apis, you'll need google developer keys in `/opt/captionator/keys/*.json`
  see [cloud platform](https://console.cloud.google.com/)
* Link the Service file into systemd and reload systemd
  ```bash
  ln -s /opt/captionator/captionator.service\
        /lib/systemd/system/captionator.service
  systemctl daemon-reload
  ```

