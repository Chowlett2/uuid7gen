# uuid7gen

A lightweight and pure-Python implementation of UUIDv7 for Python versions < 3.11. Compatible with [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html).

## Installation

```bash
pip install uuid7gen
```

## Usage

### Generate a single UUIDv7

```python
from uuid7gen import uuid7

id = uuid7()
print(id)
```
Expected output:
```
018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7c
```

### Generate a batch of UUIDv7s

```python
from uuid7gen import batch_uuid7

ids = batch_uuid7(5)
for i, id in enumerate(ids):
    print(f"{i+1}: {id}")
```
Expected output:
```
1: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7c
2: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7d
3: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7e
4: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7f
5: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c80
```

### Visual representations of a UUIDv7

```python
id = uuid7()
print("standard string:", id)
print("bytes:", id.bytes)
print("hex:", id.hex)
print("int:", id.int)
print("urn:", id.urn)
```
Expected output:
```
standard string: 018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7c
bytes: b'\x01\x8en|{|\x7f|\xbf|||||||'
hex: 018e6e7c7b7c7f7cbf7c7c7c7c7c7c7c7c
int: 212345678901234567890123456789012345
urn: urn:uuid:018e6e7c-7b7c-7f7c-bf7c-7c7c7c7c7c7c
```

---

For more details, see the [documentation](https://github.com/yourname/uuid7gen).