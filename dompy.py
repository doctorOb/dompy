from bs4 import BeautifulSoup
from bs4.element import NavigableString
import urllib2

""" Dom node properties (stripped of some functions)

vLink
text
link
bgColor
background
aLink
spellcheck
isContentEditable
contentEditable
outerText
innerText
accessKey
hidden
webkitdropzone
draggable
tabIndex
dir
translate
lang
title
childElementCount
lastElementChild
firstElementChild
children
nextElementSibling
previousElementSibling
shadowRoot
dataset
classList
className
outerHTML
innerHTML
localName
prefix
namespaceURI
id
style
attributes
tagName
parentElement
textContent
baseURI
ownerDocument
nextSibling
previousSibling
lastChild
firstChild
childNodes
parentNode
nodeType
nodeValue
nodeName
click
getAttribute
setAttribute
removeAttribute
getAttributeNode
setAttributeNode
removeAttributeNode
getElementsByTagName
hasAttributes
getAttributeNS
setAttributeNS
removeAttributeNS
getElementsByTagNameNS
getAttributeNodeNS
setAttributeNodeNS
hasAttribute
hasAttributeNS
matches
getElementsByClassName
insertAdjacentElement
insertAdjacentText
insertAdjacentHTML
webkitMatchesSelector
createShadowRoot
getDestinationInsertionPoints
getClientRects
getBoundingClientRect
webkitRequestFullScreen
webkitRequestFullscreen
webkitRequestPointerLock
querySelector
querySelectorAll
ALLOW_KEYBOARD_INPUT
insertBefore
replaceChild
removeChild
appendChild
hasChildNodes
cloneNode
normalize
isSameNode
isEqualNode
lookupPrefix
isDefaultNamespace
lookupNamespaceURI
compareDocumentPosition
contains
ELEMENT_NODE
ATTRIBUTE_NODE
TEXT_NODE
CDATA_SECTION_NODE
ENTITY_REFERENCE_NODE
ENTITY_NODE
PROCESSING_INSTRUCTION_NODE
COMMENT_NODE
DOCUMENT_NODE
DOCUMENT_TYPE_NODE
DOCUMENT_FRAGMENT_NODE
NOTATION_NODE
DOCUMENT_POSITION_DISCONNECTED
DOCUMENT_POSITION_PRECEDING
DOCUMENT_POSITION_FOLLOWING
DOCUMENT_POSITION_CONTAINS
DOCUMENT_POSITION_CONTAINED_BY
DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC
"""


class Document:
	"""Given an html page as a string, convert it to a document model
	Aims to mimick the document variable in the browser."""
	def __init__(self,html):
		bs = BeautifulSoup(html)
		self.body = iterate_tag(bs.body) #the body node, in most cases, we start iterating from here
		#This is a collection of ALL the Nodes on the page. Just a flat array
		#We should probably build this first.
		self.all = parseTree(self.body)
		self.idMap = self._build_hashMap()


	def _build_hashMap(self):
		idMap = {}
		for node in self.all:
			if node.id:
				idMap[node.id] = node
		return idMap



	def getElementById(self,id):
		"""This is most likely implemented as a hash map on most browsers.
		We can probably build this while filling the document.all collection"""
		try:
			return self.idMap[id]
		except KeyError:
			return None

	def getElementsByTagName(self,tagName):
		return self.body.getElementsByTagName(tagName)

	def getElementsByClassName(self,className):
		return self.body.getElementsByClassName(className)


class Node:
	"""Implementation of javascript DOM nodes. I'm not really sure if 
	there's a propper name for these."""

	def __init__(self,bsTag,parentNode=None,children=[]):
		self.tagName = bsTag.name
		self.parentNode = parentNode
		self.children = children
		self.id = _getAttrSafe(bsTag.attrs,'id')
		self.className = _getAttrSafe(bsTag.attrs,'class')
		self.innerText = ""


	def appendChild(self,child):
		#print "adding {} to {}".format(child.tagName,self.tagName)
		self.children.append(child)

	def getElementsByTagName(self,tagName):
		ret = []
		if self.tagName == tagName:
			ret.append(self)

		for node in self.children:
			ret += node.getElementsByTagName(tagName)

		return ret

	def getElementsByClassName(self,className):
		ret = []
		if self.className and className in self.className:
			ret.append(self)

		for node in self.children:
			ret += node.getElementsByClassName(className)

		return ret


def _getAttrSafe(attrs,name):
	return attrs[name] if name in attrs else None

def iterate_tag(tag):
	"""
	Iterate over the children of a BStag. These may be more BStags,
	which will need to be recursively iterated over, or NavigableString
	objects, which we collect into a string and set as the node's 
	innerText
	"""
	node = Node(tag,children=[])

	text = ""

	childs = []
	for sub in tag:
		if isinstance(sub, NavigableString):
			if len(sub) > 1:
				text+=sub
		else:
			childs.append(iterate_tag(sub))
	
	for child in childs:
		node.appendChild(child)

	node.innerText = text
	return node

def parseTree(root):
	ret = [root]
	if len(root.children) < 1:
		return ret
	for node in root.children:
		ret += parseTree(node)
	return ret

if __name__ == '__main__':
	
	#html = urllib2.urlopen('http://concordma.com').read()
	html = open('test.html').read()
	document = Document(html)

	print document.getElementById('foo').innerText
	print document.getElementsByTagName('div')
	print document.getElementsByClassName('bar')





