import os

# Generate 32 random bytes and encode them as a hexadecimal string
secret_key = os.urandom(32).hex()
print(secret_key)