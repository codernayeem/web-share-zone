# web-share-zone
A web server to share files easily made with flask


## Instructions
* Install necessary libraries :
<br> _**`pip -r install req.txt`**_

* Create database :
<br> _**`python manage.py init`**_

* Create Admin Account :
<br> _**`python manage.py createadmin`**_

* Create Normal User Account :
<br> _**`python manage.py createuser`**_

* Start Server _(auto host & port)_ :
<br> _**`python app.py`**_
<br> _**`python app.py * <port>`**_
<br> _**`python app.py * 8888`**_

* Start Server at localhost :
<br> _**`python app.py localhost`**_
<br> _**`python app.py localhost <port>`**_
<br> _**`python app.py localhost 8888`**_

* Start Server at network :
<br> _**`python app.py <network-ip> <port>`**_
<br> _**`python app.py 192.168.0.101`**_
<br> _**`python app.py 192.168.0.101 8888`**_

* Change default port, folder names, configurations:
<br> _**Edit `config.py`**_

## Share Zone
* To share text/files in share zone, you need to be logged on.

## Download Zone
* The default folder name is "DOWNLOADZONE". PLace your files at that folder to show in Download Zone.

## Upload Zone
* Just upload anything to the server folder named "UPLOADZONE" (default).