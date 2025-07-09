from uuid7gen import uuid7, batch_uuid7

# Generate a single UUIDv7
print(uuid7())

# Generate 100 UUIDv7s spaced 1 ms apart
ids = batch_uuid7(100)

# Print the first 10 UUIDv7s
for i, id in enumerate(ids[:10]):
    print(f"{i+1:2d}: {id}")