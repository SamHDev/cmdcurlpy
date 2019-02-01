import platform
import os
import subprocess
import zipfile
import shutil
try:
    import urllib.request as urlreq
except:
    import urlib as urlreq

class curlError(Exception):
    pass
class curlInstallError(Exception):
    pass


def getOS():
    return platform.system().lower() , platform.linux_distribution()[0].lower()

def getLocalPath(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),name)

def checkInstall(install=False,slient=False):
    ostype,osversion = getOS()
    #print(getOS())
    if (ostype == "linux"):
        try:
            p = subprocess.Popen(["curl","-V"],stdout=subprocess.PIPE)
            return "curl"
        except FileNotFoundError:
            if (slient==False):
                raise curlError("Curl Not Installed. Run curlcmd.install()")
            else:
                return False
    if (ostype == "windows"):
        try:
            p = subprocess.Popen(["curl.exe","-V"],stdout=subprocess.PIPE)
            return "curl.exe"
        except FileNotFoundError:
            try:
                p = subprocess.Popen([getLocalPath("install/win32/curl/bin/curl.exe"),"-V"],stdout=subprocess.PIPE)
                return "install/win32/curl/bin/curl.exe"
            except FileNotFoundError:
                if (slient==False):
                    raise curlError("Curl Not Installed. Run curlcmd.install()")
                else:
                    return False
    
def install(verb=False):
    if (verb): print("[CURL] Checking Install")
    ins = checkInstall(slient=True)
    if (ins != False):
        if (verb): print("[CURL] Aborting Install, Already Installed")
        raise curlInstallError("CURL Already Installed")
    ostype,osversion = getOS()
    ostype = "windows"
    if (ostype == "linux"):
        distoman = {"ubuntu":["apt-get",["install","remove"],"curl","-y","sudo "]}
        if (osversion not in distoman.keys()):
            raise curlInstallError("OS Install Not Supported. Try manualy Installed")
        else:
            if (verb): print("[CURL] Installing Via: " + distoman[osversion][0])
            cmd = distoman[osversion][4] + distoman[osversion][0] + " " + distoman[osversion][1][0] + " " + distoman[osversion][2] + " " + distoman[osversion][3]
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
            p.wait()
            out = p.stdout.read()
            err = p.stderr.read()
            if (err!=b''):
                if (verb): print("[CURL] Aborting Install, " + distoman[osversion][0] + "Raised Error")
                ermsg = "Install Error from: {}. '{}'".format(distoman[osversion][0],err.decode("UTF-8").replace("\n",",  "))
                raise curlInstallError(ermsg)
            else:
                if (verb): print("[CURL] Installed")
                if (verb): print("[CURL] Checking Install")
                ins = checkInstall(slient=True)
                if (verb and not ins): print("[CURL] Install Failed, No Curl Found")
                if (not ins): raise curlInstallError("Install Failed, No Curl Install Found after Installing")
    if (ostype == "windows"):
        if (verb): print("[CURL] Downloading")
        try:
            shutil.rmtree(getLocalPath("install/"))
        except: pass
        try: os.mkdir(getLocalPath("install/"))
        except: pass
        try: os.mkdir(getLocalPath("install/zip/"))
        except : pass
        try: os.mkdir(getLocalPath("install/win32/"))
        except: pass
        urlreq.urlretrieve ("https://curl.haxx.se/windows/dl-7.63.0/curl-7.63.0-win32-mingw.zip",getLocalPath("install/zip/dlout.zip"))
        if (verb): print("[CURL] Unzipping")
        zips = zipfile.ZipFile(getLocalPath("install/zip/dlout.zip"), 'r')
        zips.extractall(getLocalPath("install/zip/out"))
        os.rename(getLocalPath("install/zip/out/curl-7.63.0-win32-mingw/"),getLocalPath("install/zip/out/curl"))
        shutil.move(getLocalPath("install/zip/out/curl/"),getLocalPath("install/win32"))
        
        
        

def execute(cmd):
    c = checkInstall()
    cmd.replace("curl",c)
    a = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    a.wait()
    out = a.stdout.read().decode("UTF-8")
    return out
    
a = checkInstall(slient=True)
if (a == False):
    install(verb=True)
    
