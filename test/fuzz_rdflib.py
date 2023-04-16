#!/usr/bin/python3

import atheris

with atheris.instrument_imports():
    from rdflib import Graph, URIRef, Literal, Namespace
    from rdflib.plugins.parsers.notation3 import BadSyntax
    from rdflib.exceptions import ParserError
    from rdflib import BNode
    from pyparsing import ParseException
    import sys
    from xml.sax import SAXParseException


def test_graph_parser(data):
    # arbitrary byte 'data' created by atheris that mutates each time
    # this allows you to manipulate the 'data' into strings, integers, lists of integers etc.
    fdp = atheris.FuzzedDataProvider(data)
    format_list = ["xml", "trix", "turtle", "n3", "nt"]
    g = Graph()
    try:
        g.parse(format=fdp.PickValueInList(format_list),
                data=fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(1, 100)))
    # Data generated is not appropriate, so ignore BadSyntax, SAXParseException and ParserError
    except (BadSyntax, SAXParseException, ParserError):
        return
    g.serialize(format='ttl')
    try:
        g.query(fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(1, 100)))
    except ParseException:
        pass


def test_uriref(data):
    fdp = atheris.FuzzedDataProvider(data)
    test_uri = URIRef(fdp.ConsumeUnicodeNoSurrogates(
        fdp.ConsumeIntInRange(10, 100)))


def test_bnode(data):
    fdp = atheris.FuzzedDataProvider(data)
    bn = BNode(fdp.ConsumeUnicodeNoSurrogates(
        fdp.ConsumeIntInRange(10, 100)))


def test_literal(data):
    fdp = atheris.FuzzedDataProvider(data)
    _ = Literal(fdp.ConsumeUnicodeNoSurrogates(
        fdp.ConsumeIntInRange(1, 100)))
    _ = Literal(fdp.ConsumeIntInRange(1, 100))


def test_namespace(data):
    fdp = atheris.FuzzedDataProvider(data)
    EX = Namespace(fdp.ConsumeUnicodeNoSurrogates(
        fdp.ConsumeIntInRange(1, 100)))
    g = Graph()
    try:
        g.bind(fdp.ConsumeUnicodeNoSurrogates(
            fdp.ConsumeIntInRange(1, 100)), EX)
    except KeyError:
        return


def test_one_input(data):
   # test_uriref(data)
    test_bnode(data)
    test_literal(data)
    # test_graph_parser(data)
    test_namespace(data)


atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
