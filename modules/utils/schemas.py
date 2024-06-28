import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, Union

from aiocache import cached

if hasattr(sys, "_MEIPASS"):
    DEFAULT_SCHEMAS_DIR = Path(__file__).parent.parent.parent.parent
else:
    DEFAULT_SCHEMAS_DIR = Path(__file__).parent.parent.parent

DEFAULT_SCHEMAS_DIR = DEFAULT_SCHEMAS_DIR / "schemas"


class LocalFileRefCompiler:
    def __init__(self, base_path: Optional[Path] = None):
        self.path = base_path or DEFAULT_SCHEMAS_DIR
        self.ref_cache = {}

    def resolve(self, obj: Union[dict, list]) -> Union[dict, list]:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref = obj["$ref"]
                if isinstance(ref, str):
                    resolved_ref = self.load_and_resolve_ref(ref)
                    return resolved_ref

            else:
                for k, v in obj.items():
                    obj[k] = self.resolve(v)  # Update value in place

        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                obj[i] = self.resolve(value)  # Update value in place

        return obj

    def load_and_resolve_ref(self, ref: str) -> Union[dict, list]:
        if ref not in self.ref_cache:
            ref_path = self.path / ref
            try:
                with open(ref_path, "r") as ref_file:
                    referenced_schema = json.loads(ref_file.read())
                    self.ref_cache[ref] = self.resolve(
                        referenced_schema
                    )  # Cache resolved reference
            except FileNotFoundError:
                print(f"Reference file not found: {ref_path}")
                raise
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {ref_path}")
                raise

        return self.ref_cache[ref]


@cached()
async def get_compiled_schema(path: Union[Path, str]) -> Union[dict, list]:
    with open(path) as f:
        schema = json.load(f)

    compiler = LocalFileRefCompiler()
    compiled_schema = await asyncio.to_thread(compiler.resolve, schema)
    return compiled_schema
