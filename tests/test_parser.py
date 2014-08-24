import os
from kennyg.element import ValueCollector, Value, KeyValueCollector, KeyValue
from kennyg.sax_handler import KennyGSAXHandler
from kennyg.parser import parse, parseString

__author__ = 'brent'


def get_data_filepath(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),"data",name)


def test_naive_sax_handler():
    d = []
    kg = KennyGSAXHandler(action_tree={'a':{'b':{'c':{'value':lambda x, *args: d.append(x)}}}})
    parse(get_data_filepath('simple.xml'), kg)
    print d
    assert ''.join(d) == '123456'


def test_key_value_collector():
    d = []
    vc = KeyValueCollector(e=KeyValue('egg'), g=KeyValue('G'), h=KeyValue('H'))
    kg = KennyGSAXHandler(action_tree={'a':vc})
    xml = "<a><b><c>1</c><c/></b><e>e_value</e><b>bbbb</b><g/></a>"
    parseString(xml, kg)
    assert vc.collection['egg'].strip() == 'e_value'
    assert vc.collection['G'].strip() == ''
    exception = False
    try:
        v = vc.collection['H']
    except KeyError as _:  # noqa
        exception = True
    assert exception


def test_value_collector():
    d = []
    vc = ValueCollector(b=ValueCollector(c=Value()))
    kg = KennyGSAXHandler(action_tree={'a':vc})
    parse(get_data_filepath('simple.xml'), kg)
    print vc.collection
    assert ''.join(vc.collection[0]) == '123'
    assert ''.join(vc.collection[1]) == '456'


def test_keyvalue_list():
    xml = "<a><b><c>agent</c></b></a>"
    vc = ValueCollector({u'b':KeyValueCollector({u'c': KeyValue(key='key'),})})
    kv = KeyValueCollector({u'a': KeyValue(key=u'wrapped', obj=vc)})
    kg = KennyGSAXHandler(kv)
    parseString(xml, kg)
    print kv.collection
