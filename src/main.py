import importlib

tools = ["crosshair"]

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"tools.{module_name}.worker"), function_name)

for tool in tools:
    get_function(tool)()