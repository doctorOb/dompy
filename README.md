dompy
=====

Javascript DOM objects in python. Parse html like you would in the browser.

The goal is to implement [XML DOM Elements](http://www.w3schools.com/dom/dom_element.asp) in Python.

BeautifulSoup is a wonderfully robust library for parsing html, and navigating the document tree. However, I found it unpleasent to work with. As someone who's used to manipulating DOM elements in javascript, I wanted the ability to do the same thing in python. 

It (roughly) works as follows:

> document = dompy.Document(htmlString)
> document.getElementsByClassName('td') #get all the TDs in the document
> document.getElementById('foo').innerText #get the text in the foo element

BeautifulSoup is still used to parse the html document, but the Tags are then iterated over and converted to a Node class
which aims to closely resemble those found in javascript. So, as you'd access the body's className or tagName just as you would in javascript, like:

> document.body.className
> document.getElementsByName('idk')[0].tagName #figure out what tag has been named so vaguely

