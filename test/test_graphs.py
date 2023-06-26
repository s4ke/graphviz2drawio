from graphviz2drawio import graphviz2drawio
import xml.etree.ElementTree as ET
import re
import html

num_cells_offset = 2


def check_xml_top(root):
    graph = root.findall(".")
    assert len(graph) == 1
    graph = graph[0]
    assert graph.tag == "mxGraphModel"
    return graph.findall("./root/*")


def check_style(e, check):
    assert check in e.attrib["style"]


def check_value(e, check):
    value = e.attrib["value"]
    match = re.match(r"<p.*>%s</p>" % check, html.unescape(value))
    assert match, "no match found for %s" % value


def check_edge(e, source, target):
    assert e.attrib.get("edge")
    assert e.attrib["source"] == source.attrib["id"]
    assert e.attrib["target"] == target.attrib["id"]


def check_edge_dir(e, dx, dy):
    style = [e.split("=") for e in e.attrib["style"].split(";")][:-1]
    style = {e[0]: e[1] for e in style if e}
    x2 = float(style["exitX"])
    x1 = float(style["entryX"])
    y2 = float(style["exitY"])
    y1 = float(style["entryY"])

    assert (x2 - x1) == dx
    assert (y2 - y1) == dy


def test_hello():
    file = "./directed/hello.gv.txt"
    xml = graphviz2drawio.convert(file)
    print(xml)

    root = ET.fromstring(xml)
    elements = check_xml_top(root)

    hello = elements[3]
    check_style(hello, "ellipse")
    check_value(hello, "Hello")

    world = elements[4]
    check_style(world, "ellipse")
    check_value(world, "World")
    edge = elements[2]
    check_edge(edge, hello, world)
    check_edge_dir(edge, dx=0, dy=1)

def test_hello_rect():
    file = "./directed/hello_rect.gv.txt"
    xml = graphviz2drawio.convert(file)
    print(xml)

    root = ET.fromstring(xml)
    elements = check_xml_top(root)

    hello = elements[3]
    check_value(hello, "Hello")
    assert "ellipse" not in hello.attrib["style"]

    world = elements[4]
    check_value(world, "World")
    assert "ellipse" not in world.attrib["style"]


def test_polylines():
    file = "./undirected/polylines.gv.txt"
    xml = graphviz2drawio.convert(file)
    print(xml)

    root = ET.fromstring(xml)
    check_xml_top(root)


# def test_runAll():
#    for f in os.listdir('undirected'):
#        xml = graphviz2drawio.convert(f)
#        print(xml)
