import json
import blackboxprotobuf


def restore_types(msg, typedef):
    """
    Convert JSON-loaded strings back to bytes when typedef says 'bytes'.
    Recursively processes nested message typedefs.
    """
    if not isinstance(msg, dict):
        return msg

    fixed = {}
    for key, value in msg.items():
        field_def = typedef.get(key, {})
        ftype = field_def.get('type')

        if ftype == "bytes" and isinstance(value, str):
            try:
                fixed[key] = value.encode("utf-8")
            except:
                fixed[key] = bytes.fromhex(value)
        elif ftype == "message" and isinstance(value, dict):
            # Recursively process nested messages with their typedef
            nested_typedef = field_def.get('message_typedef', {})
            fixed[key] = restore_types(value, nested_typedef)
        elif isinstance(value, list):
            fixed[key] = [restore_types(v, typedef.get(key, {})) for v in value]
        else:
            fixed[key] = value

    return fixed


# ===================== LOAD JSON =====================

input_file = "msg.json"
output_file = "room_encoded"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract message content and schema definition
msg = data["message_content"]
typedef = data["schema_definition"]

# ===================== FIX TYPES BEFORE ENCODING =====================

msg_fixed = restore_types(msg, typedef)

# ===================== ENCODE =====================

encoded_bytes = blackboxprotobuf.encode_message(msg_fixed, typedef)

with open(output_file, "wb") as f:
    f.write(encoded_bytes)

print(f"✔ Successfully encoded {input_file} to {output_file}")
