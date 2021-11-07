# About the petfacts CLI application
Pet facts is a simple but fun application that retrieves either dog or cat facts from two different resources.

[Click here](https://catfact.ninja) to see the cat facts api.

[Click here](https://dog-facts-api.herokuapp.com) to see the dog facts api.

## Why did I write it?
I wrote this application to learn a python module called argparse, and this seemed like the perfect fun project to do this with.

## How can I get it?
petfacts comes with an automated installer that will install petfacts, and remove it when you want it gone.

### Steps to install:
* First clone this repo `git clone git@github.com:CodeCanna/petfacts.git`
* `cd` into the newly cloned directory
* Once you are in the main petfacts directory you can run the installer `sudo ./install`; this will install petfacts
* Done!  You can test it by either printing out the help menu, or you can display a fact!  Try running `petfacts --cat`!

### Steps to uninstall:
* `cd` back into the cloned petfacts directory or re-clone the project to give you access to the installer.
* run `sudo ./install --uninstall` to remove petfacts.
* (Optionally) you can use `sudo rm -f /usr/bin/petfacts to remove it manually, just be careful!!`
