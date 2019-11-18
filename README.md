## Keck Keyword User Interface

### Introduction

This repository runs a web page that provides a user interface for each of the Keck Instruments.
Each page is to communicate the diagnoses of the health of the instrument.

### From Docker

Runs from docker container

- Install
- Run Options
- Troubleshooting

#### Install

This should import the container
```
docker pull terry071896/keck_keyword_interface
```
This is also the command used to install new updates.

#### Run Options

##### Option 1- Basic Run:

```
docker run --publish 8050:8050 terry071896/keck_keyword_interface
```
This should run the container.

You should see (or similar to)

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.1:8050/ (Press CTRL+C to quit)
```

open a browser and go to the link specified (for me that is `localhost:8050/`).

##### Option 2- Start/Stop Run:

```
docker run --publish 8050:8050 --detach terry071896/keck_keyword_interface
```
This will run the container in the background without any read out.

In order to stop the container from running,
```
docker stop terry071896/keck_keyword_interface
```
and to start
```
docker start terry071896/keck_keyword_interface
```

If you are starting and stopping the container many times, it could be ideal to rename the process.
(If there are more updates to be installed, this is not recommended as you will have to remove the name)

```
docker run --publish 8050:8050 --detach --name keckUI terry071896/keck_keyword_interface
```
So then you can start stop using that name,
```
docker start keckUI
docker stop keckUI
```

#### Troubleshooting

If you are getting the error ```docker: Command not found.```, then go to the website https://www.docker.com/products/docker-desktop and follow the instructions to download docker.

If ```docker pull [...]``` or ```docker run [...]``` are not found, check for spelling errors (it's there).

If the container appears to be running, but nothing is showing up on the localhost.  Make sure that you are running from port ```8050:8050```.

If the app is not updating properly, then see the GitHub Troubleshooting section at the bottom of this page.

If you renamed the docker container (such as "keckUI" above) and you are trying to update, then
```
docker container rm --force keckUI
docker run [...]
```

If none of these are the issue that you are experiencing, then
```
  git clone https://github.com/Terry071896/KeckKeywordInterface/
  cd .../KeckKeywordInterface
  docker build -t terry071896/keck_keyword_interface .
  docker run [...]
```

### From GitHub

Runs from python3

- Install/Run
- Troubleshooting

#### Install/Run

```
  git clone https://github.com/Terry071896/KeckKeywordInterface/
  cd .../KeckKeywordInterface
  sudo pip install -r requirements.txt
```
This should import all the code and python packages necessary.

Then, to run the app
```
  python index.py
```

You should then see

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.1:8050/ (Press CTRL+C to quit)
```
open a browser and go to the link specified (for me that is `http://0.0.0.1:8050/`).

If there is a problem, then you are running python2, so ```python3 index.py``` should work.

#### Troubleshooting

If the app is not updating or updating properly:
- First, give it a few seconds as the program could be changing modes or reading in a large amount of data.
- Second, either try refreshing the page or kill/rerun the program.

If you are getting the error
```
Error in getting data from the server
```
over and over, then there is a problem with the script "simple_server.py", which should be running from "kroot".

Given that it is not running, then it can be ran from the home directory "vm-history-1".

Once logged in, then
```
cd KeckKeywords/keyword_server/
kpython3 simple_server.py
```
