## Keck Keyword User Interface

### Introduction

This repository runs a web page that provides a user interface for each of the Keck Instruments.
Each page is to communicate the diagnoses of the health of the instrument.

### Install/Run

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
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```
open a browser and go to the link specified (for me that is `http://127.0.0.1:8050/`).

If there is a problem, then you are running python2, so ```python3 index.py``` should work.

### Troubleshooting

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
