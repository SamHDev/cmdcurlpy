# cmdcurlpy
Command Line Curl Installer and Executor

## Install
`python3 -m pip install cmdcurlpy`

## Usage
```py
import cmdcurl
print(cmdcurl.execute("curl 'http://google.com'"))
```

Simple.

On Import, it will check if curl is installed, 
If not, it will install automagicly!
