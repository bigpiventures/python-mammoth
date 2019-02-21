import cobble

from . import html


def path(elements):
    return HtmlPath(elements)


def element(names, class_names=None, fresh=None, separator=None):
    if class_names is None:
        class_names = []
    if fresh is None:
        fresh = False
    if class_names:
        attributes = {"class": " ".join(class_names)}
    else:
        attributes = {}
    return HtmlPathElement(html.tag(
        tag_names=names,
        attributes=attributes,
        collapsible=not fresh,
        separator=separator,
    ))


@cobble.data
class HtmlPath(object):
    elements = cobble.field()
    
    def wrap(self, generate_nodes, node=None):
        nodes = generate_nodes()

        for element in reversed(self.elements):
            nodes = element.wrap_nodes(nodes, source_node=node)
        
        return nodes


@cobble.data
class HtmlPathElement(object):
    tag = cobble.field()

    def wrap(self, generate_nodes, node=None):
        return self.wrap_nodes(generate_nodes(), source_node=node)

    def wrap_nodes(self, nodes, source_node=None):
        element = html.Element(self.tag, nodes, style={
            'data-indent': str((int(source_node.indent.start or 0) - int(source_node.indent.hanging or 0))),
            'style': 'margin-left: {}'.format(str((int(source_node.indent.start or 0) - int(source_node.indent.hanging or 0)) / 300) + 'em')
        } if source_node and source_node.indent else {})
        return [element]

empty = path([])


class ignore(object):
    @staticmethod
    def wrap(generate_nodes):
        return []
