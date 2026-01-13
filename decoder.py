import base64
import gzip
import json
from pathlib import Path

import blackboxprotobuf
import msgpack

# 1. SETUP: Define your input file and output file
INPUT_FILE = "test"  # The file you uploaded
OUTPUT_FILE = "test.json"

def bytes_to_string_handler(obj):
    """
    Custom handler to convert bytes to strings for JSON.
    It tries to decode as UTF-8 (readable text); if that fails, 
    it converts the binary to a Base64 string to preserve data.
    """
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            # Return as a tagged string so you know it was binary
            return f"<BINARY_BASE64: {base64.b64encode(obj).decode('ascii')}>"
    raise TypeError(f"Type {type(obj)} is not JSON serializable")

def strip_msgpack_envelope(blob: bytes) -> bytes:
    """
    Some captures arrive as a msgpack map that advertises whether the payload
    is zipped and its length. If detected, remove the envelope and optionally
    decompress the payload.
    """
    try:
        unpacker = msgpack.Unpacker()
        unpacker.feed(blob)
        envelope = next(unpacker)
    except Exception:
        return blob

    if isinstance(envelope, dict) and {"IsZip", "ZipDataLen"} <= set(envelope.keys()):
        payload_start = unpacker.tell()
        payload = blob[payload_start:]
        print(
            f"Detected msgpack envelope (IsZip={envelope['IsZip']}, "
            f"ZipDataLen={envelope['ZipDataLen']}), stripping..."
        )

        if envelope["ZipDataLen"] and envelope["ZipDataLen"] != len(payload):
            print(
                f"Warning: envelope length={envelope['ZipDataLen']} "
                f"but {len(payload)} bytes remain"
            )

        if envelope.get("IsZip"):
            try:
                payload = gzip.decompress(payload)
            except Exception as err:
                raise RuntimeError(f"Envelope indicates zip but failed to decompress: {err}")

        return payload

    return blob

try:
    print(f"Reading {INPUT_FILE}...")
    raw_data = Path(INPUT_FILE).read_bytes()

    # Some captures are full HTTP responses (status line + headers + body).
    # If so, strip the envelope so we only decode the protobuf payload.
    if raw_data.startswith(b"HTTP/"):
        print("Detected HTTP response framing, stripping headers...")
        if b"\r\n\r\n" in raw_data:
            _, raw_data = raw_data.split(b"\r\n\r\n", 1)
        elif b"\n\n" in raw_data:
            _, raw_data = raw_data.split(b"\n\n", 1)
        else:
            raise RuntimeError("HTTP-like input but no header terminator found")

    # 2. Strip msgpack envelopes that wrap the actual protobuf payload.
    data = strip_msgpack_envelope(raw_data)

    # 3. Some captures arrive as a small wrapper with a gzip blob inside.
    #    If we see gzip magic bytes, unwrap before decoding the protobuf.
    gzip_magic = b"\x1f\x8b\x08"
    magic_pos = data.find(gzip_magic)
    if magic_pos != -1:
        print(f"Detected gzip payload at offset {magic_pos}, decompressing...")
        try:
            data = gzip.decompress(data[magic_pos:])
        except Exception as gzip_err:
            raise RuntimeError(f"Gzip found but failed to decompress: {gzip_err}")

    # 4. DECODE: Reverse-engineer the protobuf structure
    msg, typedef = blackboxprotobuf.decode_message(data)

    # 5. EXPORT: Write to JSON with the custom handler
    output_data = {
        "message_content": msg,
        "schema_definition": typedef,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, default=bytes_to_string_handler)

    print(f"Success! Data saved to '{OUTPUT_FILE}'")

except FileNotFoundError:
    print(f"Error: Could not find file named '{INPUT_FILE}'. check the filename.")
except Exception as e:
    print(f"An error occurred: {e}")
