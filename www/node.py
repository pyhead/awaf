from collections import namedtuple

class Node(namedtuple('Node', 'name title description type')):
    """
    An anonymous web application node descriptor.
    """
    __slots__ = ()


def nodehandler(cls):
    """
    Simple class decorator to provide easy access to the current node.
    """
    def inner(node):
        setattr(cls, 'node',  node)
        return cls
    
    return inner
