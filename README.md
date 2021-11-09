# About the petfacts CLI application
Pet facts is a simple but fun application that retrieves either dog or cat facts from two different resources.

[Click here](https://catfact.ninja) to see the cat facts api.

[Click here](https://dog-facts-api.herokuapp.com) to see the dog facts api.

## Why did I write it?
I wrote this application to learn a python module called argparse, and this seemed like the perfect fun project to do this with.

## How can I get it?
You can clone the repository on [GitHub](https://github.com/CodeCanna/petfacts) or install via `pip` by running `pip install petfacts`

## How to use
This is a very simple and light program, to see a random pet fact of a dog or cat variety simply run `petfacts` with not arguments.

If you want to specify a whether you want a dog or car fact pass in the arguments like so:
* `petfacts --cat` will return a cat fact.
* `petfacts --dog` will return a dog fact.
* `petfacts --help` or `petfacts -h` of course returns a help menu and exits.

### Whats next?
* TODO: I want to get this up on PyPi so you just have to use `pip` to install.
* TODO: Give it the ability to store facts, why?  Just because I'm learning.