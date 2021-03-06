# Stubs for galaxy.tools.cwl.schema (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
from .cwltool_deps import ensure_cwltool_available as ensure_cwltool_available, load_tool as load_tool, schema_salad as schema_salad, workflow as workflow
from collections import namedtuple

RawProcessReference = namedtuple('RawProcessReference', ['process_object', 'uri'])

ProcessDefinition = namedtuple('ProcessDefinition', ['process_object', 'metadata', 'document_loader', 'avsc_names', 'raw_process_reference'])

class SchemaLoader:
    def __init__(self, strict: bool = ...) -> None: ...
    @property
    def raw_document_loader(self): ...
    def raw_process_reference(self, path): ...
    def process_definition(self, raw_reference): ...
    def tool(self, **kwds): ...

schema_loader = ...  # type: Any
non_strict_schema_loader = ...  # type: Any
