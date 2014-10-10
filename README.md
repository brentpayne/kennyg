kennyg
======

KennyG is a python SAX Handler that reduces the amount of boilerplate needed to parse data from XML.

It is written not for speed of processing (like lxml), but speed of development.  The goal is to make SAX parsers as easy to write as python dictionaries and extend the functionality with classes that implement SAX events (start, end, value).

In the first iteration of the project, the basic functionality of being able to specify a SAX parser with a dictionary object and to provide basic helper classes for capturing data.


#Installation

```sh
pip install kennyg
```

#Usage

The heart of kennyg is the **`KennyGSAXHandler`**.  It takes the schema for the the part of the XML you care about and triggers the actions you want on use.  **`KennyGSAXHandler`** is an XML SAX handler that can be used with pythons **`xml.sax`** package; it implements **`ContentHandler`**.  For completeness, we provide a **`parse`** and **`parseString`** functions that are pass throughs to the xml.sax implementation.

### KennyGSAXHandler

Parameters

* **`action_tree`**  -- *dictionary* or *classes implementing dict interface*

    This action tree defines the scheme of the XML file we care about and provides callbacks for SAX operations on each XML element. Each key of the action tree is a child element that the SAX parser should parse and its associated value is the action tree for that child element. Each action tree can implement three callbacks: `start`, `value`, and `end`.  These callbacks, if they exist, are called in the oreder listed for a specific XML element.  
    If the action tree for an element is a dictionary, then the call backs are the values keyed off.  In this case, `start`, `value`, and `end` are not allow to be child elements of the current element because their values are assumed to be callbacks.  If the action_tree for an element is represented by a class.  The call backs are assumed to be methods of the class.  If a callback is not defined it is ignored.

* **`verbose`** -- *boolean*
    
    if `True` a print statement is made for each `startElement`, `endElement`, or `character` callback as the XML is parsed.


Examples
========

The following example uses a dictionary as the action_tree
```python
from kennyg.sax_handler import KennyGSAXHandler
from kennyg.parser import parseString

office_desk_owner_xml = """
<office name="main office">
  <desk id=5>
    <owner>Carl</owner>
    <equipment>PC</equipment>
  </desk>
  <chair>
    <owner>Beelz Bub</owner>
  </chair>
  <desk>
    <owner>KennyG</owner>
  </desk>
</office>
"""

owners_names = []

office_desk_owner = {
  "office": {
    "desk": {
      "owner": {
        "value": lambda value, *attr: owners_names.append(value)
      }
    }
  }
}

kg = KennyGSAXHandler(action_tree=office_desk_owner)
parseString(xml, kg)
print owner_names

```

