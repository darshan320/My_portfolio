import bcrypt
new_hash = bcrypt.hashpw("darshan@123".encode('utf-8'), bcrypt.gensalt())
print(new_hash.decode('utf-8'))