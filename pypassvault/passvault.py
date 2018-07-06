#passvault v0.1.1
#Description: A simple commandline password vault written in python.
#https://opensource.org/licenses/MIT
#Copyright 2018 cryptbytestech
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import shelve
from passlib.hash import argon2
from invoke import task,Collection,Program
from cryptography.fernet import Fernet, MultiFernet
from appdirs import AppDirs
import sys
import os
import logging
import getpass
import pprint
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re

# Version & AUTHOR of passvault
VERSION = "0.1.4"
AUTHOR = "cryptbytestech"

def find_version(vstr):
    m = re.findall(r'(?:(\d+\.(?:\d+\.)*\d+))', vstr)
    return m

def encode_passwd(password,salt=""):
    "Encode password to generate a symmetric key"
    password = password.encode()
    if salt == "":
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return (key,salt)

@task
def configure(c,confdir=""):
    "Set the configuration"
    base_name = os.path.basename(sys.argv[0])
    appname = str(base_name).replace(".py","")
    c.config["appname"] = appname
    c.config["version"] = VERSION
    version = VERSION
    if confdir == "":
        dirs = AppDirs(appname, AUTHOR)
        confdir = dirs.user_data_dir
        #print(confdir)

    if not os.path.isdir(confdir):
        logging.warning("Creating config dir %s"%(confdir))
        os.makedirs(confdir)
    conffile = os.path.join(confdir,"conf.db")
    c.config["confdir"] = confdir
    c.config["conffile"] = conffile

    with shelve.open(conffile) as app:
        vp = ""
        app["appname"] = c.config["appname"]
        app["version"] = c.config["version"]
        if not "app_hash" in app:
            logging.warning("Creating config file %s"%(conffile))
            logging.warning("Vault Password not set, please set now")
            np = getpass.getpass(prompt='Set a vault password: ')
            # generate new salt, hash password
            phash = argon2.using(rounds=4).hash(np)
            vp = getpass.getpass(prompt='Re-enter vault password: ')
            # verify password
            if not argon2.verify(vp, phash):
                logging.error("Vault Password verification failed. Try Again")
                exit()
            app["app_hash"] = phash
            app["apps"] = {}
            app["passwds"] = {}
            logging.warning("Please do not forget your password, the password is non recoverable")
        else:
            with shelve.open(conffile) as app:
                phash = app["app_hash"]
                vp = getpass.getpass(prompt='Enter vault password: ')
                # verify password
                if not argon2.verify(vp, phash):
                    logging.error("Password verification failed. Try Again")
                    exit()
        c.config["conffile"] = conffile
        c.config["passwd"] = vp

@task(pre=[configure])
def delete(c,user="",appname="passvault"):
    "Delete password details for a username and/or application (optional)"
    config = c.config
    with shelve.open(config["conffile"]) as tapp:
        app = {"apps":tapp["apps"],"passwds":tapp["passwds"]}
        if not appname in app["apps"]:
            logging.error("No application with name %s is present"%(appname))
            exit()
        if not appname in app["passwds"]:
            logging.error("No application with name %s is present"%(appname))
            exit()
        if user == "":
            print("Deleting all details for application %s"%(appname))
            del app["passwds"][appname]
            del app["apps"][appname]
        elif not user in app["passwds"][appname]:
            logging.error("No user with name %s is present in %s"%(user,appname))
            exit()
        else:
            print("Deleting all details of user %s for application %s"%(user ,appname))
            del app["passwds"][appname][user]
            app["apps"][appname].remove(user)

        logging.info("Deleting your password from vault")
        tapp["apps"] = app["apps"]
        tapp["passwds"] = app["passwds"]

            


@task(pre=[configure])
def list(c,appname=""):
    "List all applications and users for which password is set"
    config = c.config
    with shelve.open(config["conffile"]) as app:
        if not "apps" in app:
            logging.error("No application or password is set")
            exit()
        appnames = []
        if appname!="":
            if not appname in app["apps"].keys():
                logging.error("No application with name %s is present"%(appname))
                exit()
            appnames = [appname]
        else:
            appnames = [key for key in app["apps"].keys()]
            print("List of all applications:")
            pprint.pprint(appnames)
        for appname in appnames:
            print("Users for application %s are:"%(appname))
            pprint.pprint(app["apps"][appname])

@task(pre=[configure])
def setpasswd(c,user,appname="passvault"):
    "Set password for a username and application (optional)"
    config = c.config
    passwd = getpass.getpass(prompt='Set an app password for %s: '%(user))
    bkey1 = Fernet.generate_key()
    key1 = Fernet(bkey1)
    key2,salt = encode_passwd(c.config["passwd"])
    key2 = Fernet(key2)
    f = MultiFernet([key1, key2])
    token = f.encrypt(passwd.encode())
    with shelve.open(config["conffile"]) as tapp:
        app = {"apps":tapp["apps"],"passwds":tapp["passwds"]}
        if not appname in app["apps"]:
            app["apps"][appname] = []
        if not appname in app["passwds"]:
            app["passwds"][appname] = {}
        #print(app["apps"])
        if not user in app["apps"][appname]:
            app["apps"][appname].append(user)
        #if not user in app["passwds"][appname]:
            #print(bkey1,token,salt)
        app["passwds"][appname][user] = {
            "key":bkey1,
            "token":token,
            "salt":salt
        }
        logging.info("Saving your password to vault")
        tapp["apps"] = app["apps"]
        tapp["passwds"] = app["passwds"]

@task(pre=[configure])
def get(c,user,appname="passvault"):
    "Get password for a username and application (optional)"
    config = c.config
    with shelve.open(config["conffile"]) as app:
        logging.info("getting your password from vault")
        if not appname in app["apps"]:
            logging.error("No application with name %s is present"%(appname))
            exit()
        if not appname in app["passwds"]:
            logging.error("No application with name %s is present"%(appname))
            exit()
        if not user in app["passwds"][appname]:
            logging.error("No user with name %s is present in %s"%(user,appname))
            exit()
        bkey1, token,salt = app["passwds"][appname][user].values()
        key1 = Fernet(bkey1)
        key2 = encode_passwd(c.config["passwd"],salt)
        f = MultiFernet([key1, key2])
        passwd = f.decrypt(token)
        print(passwd.decode())

def main():
    ns = Collection()
    ns.add_task(get)
    ns.add_task(setpasswd)
    ns.add_task(configure)
    ns.add_task(list)
    ns.add_task(delete)
    program = Program(version=VERSION,namespace=ns)
    program.run()
if __name__== "__main__":
    main()