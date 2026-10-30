"""Generate the empty3x3 structure template NBT used by GameTests."""
import gzip
import struct

def named(name, t, payload):
    b = name.encode("utf-8")
    return bytes([t]) + struct.pack(">H", len(b)) + b + payload

def string(s):
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b

def list_tag(inner_t, items):
    return bytes([inner_t]) + struct.pack(">I", len(items)) + b"".join(items)

def int_list(vals):
    return list_tag(3, [struct.pack(">i", v) for v in vals])

def compound(d):
    out = b""
    for k, (t, v) in d.items():
        out += named(k, t, v)
    return out + bytes([0])

air_comp = compound({"Name": (8, string("minecraft:air"))})

root = compound({
    "size": (9, int_list([3, 2, 3])),
    "entities": (9, list_tag(10, [])),
    "blocks": (9, list_tag(10, [])),
    "palette": (9, list_tag(10, [air_comp])),
    "DataVersion": (3, struct.pack(">i", 3955)),
})
data = bytes([10, 0]) + struct.pack(">H", 0) + root
with open(__file__.replace("gen_structure.py", "../src/main/resources/data/steamcurios/structure/empty3x3.nbt"), "wb") as f:
    f.write(gzip.compress(data))
print("empty3x3.nbt written")
