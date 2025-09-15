import json
import uuid
import base64
import datetime

# ==============================
# Atom types
# ==============================
class Date:
    def __init__(self, value):
        if isinstance(value, str):
            self.value = datetime.date.fromisoformat(value)
        elif isinstance(value, datetime.date):
            self.value = value
        else:
            raise TypeError("Date must be str or datetime.date")
    def __repr__(self):
        return f"@date(\"{self.value.isoformat()}\")"

class DateTime:
    def __init__(self, value):
        if isinstance(value, str):
            self.value = datetime.datetime.fromisoformat(value)
        elif isinstance(value, datetime.datetime):
            self.value = value
        else:
            raise TypeError("DateTime must be str or datetime.datetime")
    def __repr__(self):
        return f"@datetime(\"{self.value.isoformat()}\")"

class Binary:
    def __init__(self, data: bytes):
        self.data = data
    def __repr__(self):
        b64 = base64.b64encode(self.data).decode('utf-8')
        return f"@binary(\"{b64}\")"

class UUID:
    def __init__(self, value=None):
        self.value = uuid.uuid4() if value is None else uuid.UUID(str(value))
    def __repr__(self):
        return f"@uuid(\"{self.value}\")"

# ==============================
# Structural types
# ==============================
class Set:
    def __init__(self, values):
        self.values = set(values)
    def __repr__(self):
        return f"@set({list(self.values)})"

class Map:
    def __init__(self, mapping):
        self.mapping = dict(mapping)
    def __repr__(self):
        return f"@map({self.mapping})"

class Tuple:
    def __init__(self, *values):
        self.values = tuple(values)
    def __repr__(self):
        return f"@tuple({self.values})"

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.nodes = []
        self.edges = []
    def add_node(self, node_id, label=None):
        self.nodes.append({"id": node_id, "label": label})
    def add_edge(self, source, target, weight=None):
        edge = {"from": source, "to": target}
        if weight is not None:
            edge["weight"] = weight
        self.edges.append(edge)
    def __repr__(self):
        return f"@graph(directed={self.directed}, nodes={self.nodes}, edges={self.edges})"

# ==============================
# Mathematical formats
# ==============================
def s_expr(obj):
    if isinstance(obj, dict):
        return "(" + " ".join(f"({k} {s_expr(v)})" for k,v in obj.items()) + ")"
    elif isinstance(obj, list):
        return "(" + " ".join(s_expr(v) for v in obj) + ")"
    else:
        return str(obj)

class Node:
    def __init__(self, label, props=None):
        self.label = label
        self.props = props or {}
    def __repr__(self):
        return f"@node(\"{self.label}\", {self.props})"

# ==============================
# Serializer / Parser
# ==============================
def dumps(obj, fmt="ilyas"):
    if fmt == "ilyas":
        return repr(obj)
    elif fmt == "s_expr":
        return s_expr(obj)
    elif fmt == "node":
        if isinstance(obj, Node):
            return repr(obj)
        raise TypeError("Only Node supported for node format")
    else:
        raise ValueError("Unknown format")

def loads(text):
    # very naive parser for demo purposes
    if text.startswith("@date"):
        return Date(text[text.find("\"")+1:text.rfind("\"")])
    elif text.startswith("@datetime"):
        return DateTime(text[text.find("\"")+1:text.rfind("\"")])
    elif text.startswith("@uuid"):
        return UUID(text[text.find("\"")+1:text.rfind("\"")])
    elif text.startswith("@binary"):
        data = base64.b64decode(text[text.find("\"")+1:text.rfind("\"")])
        return Binary(data)
    else:
        return text

# ==============================
# File helpers for .ifamily
# ==============================
def dump_file(obj, path, fmt="ilyas"):
    if not path.endswith(".ifamily"):
        raise ValueError("File must have .ifamily extension")
    with open(path, "w", encoding="utf-8") as f:
        f.write(dumps(obj, fmt))

def load_file(path):
    if not path.endswith(".ifamily"):
        raise ValueError("File must have .ifamily extension")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    return loads(text)

# ==============================
# Example usage
# ==============================
if __name__ == "__main__":
    person = Node("Person", {
        "Name": "Nazwa",
        "Age": 21,
        "Address": Node("Address", {"City": "Bandung", "Code": 40123})
    })

    dump_file(person, "person.ifamily")
    loaded = load_file("person.ifamily")
    print("Loaded:", loaded)
