## Keck Keyword User Interface

### Introduction

### Install/Run

```
  git clone https://github.com/Terry071896/KeckKeywordInterface/
  cd .../KeckKeywordInterface
  python index.py
```

### Troubleshooting

If the app is not updating or updating properly:
- First, give it a few seconds as the program could be changing modes or reading in a large amount of data.
- Second, either try refreshing the page or kill/rerun the program.

If you are getting the error
```
Error in getting data from the server
```
over and over, then there is a problem with the script "simple_server.py" should be running from "kroot".

Given that it is not running, then it can be run from the home directory "vm-history-1".
Once logged in, then
```
cd KeckKeywords/keyword_server/
kpython3 simple_server.py
```
