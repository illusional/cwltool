# Stubs for rdflib.events (Python 2)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

class Event:
    def __init__(self, **kw): ...

class Dispatcher:
    def set_map(self, amap): ...
    def get_map(self): ...
    def subscribe(self, event_type, handler): ...
    def dispatch(self, event): ...
