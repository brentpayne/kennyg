import os
from kennyg.element import ValueCollector, Value, KeyValueCollector, KeyValue
from kennyg.sax_handler import KennyGSAXHandler
from kennyg.parser import parse

__author__ = 'brent'


def get_data_filepath(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),"data",name)


def test_naive_sax_handler():
    d = []
    kg = KennyGSAXHandler(action_tree={'a':{'b':{'c':{'value':lambda x: d.append(x)}}}})
    parse(get_data_filepath('simple.xml'), kg)
    print d
    assert ''.join(d) == '123456'


def test_key_value_collector():
    d = []
    vc = KeyValueCollector(e=KeyValue('egg'), g=KeyValue('G'), h=KeyValue('H'))
    kg = KennyGSAXHandler(action_tree={'a':vc})
    parse(get_data_filepath('simple.xml'), kg)
    assert vc.collection['egg'].strip() == 'e_value'


def test_value_collector():
    d = []
    vc = ValueCollector(b=ValueCollector(c=Value()))
    kg = KennyGSAXHandler(action_tree={'a':vc})
    parse(get_data_filepath('simple.xml'), kg)
    print vc.collection
    assert ''.join(vc.collection[0]) == '123'
    assert ''.join(vc.collection[1]) == '456'

