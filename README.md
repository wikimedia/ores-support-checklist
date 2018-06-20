[![Build Status](https://travis-ci.org/wiki-ai/ores-support-checklist.svg?branch=master)](https://travis-ci.org/wiki-ai/ores-support-checklist)
ORES support checklist
=========================

This git repository contains the source code for a basic Python webservice
built to show ORES support for different wikis

Running from Tool Labs
-----

```
$ ssh tools-dev.wmflabs.org
$ become $TOOL_NAME
$ mkdir -p $HOME/www/python
$ git clone https://github.com/wiki-ai/ores-support-checklist \
  $HOME/www/python/src
$ touch $HOME/www/python/src/config.yaml
$ chmod u=rw,go= $HOME/www/python/src/config.yaml
$ webservice --backend=kubernetes python shell
$ python3 -m venv $HOME/www/python/venv
$ source $HOME/www/python/venv/bin/activate
$ pip install --upgrade pip
$ pip install -r $HOME/www/python/src/requirements.txt
$ exit
$ webservice --backend=kubernetes python start
```

Running locally
-----

```
$ pip install flask-cli
$ FLASK_APP=app.py flask run
```

License
-------
[GNU GPLv3+](//www.gnu.org/copyleft/gpl.html "GNU GPLv3+")
