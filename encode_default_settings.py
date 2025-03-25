from modules.encryption import *

with open("assets/default_settings", "r") as file:
    print(encode(file.read()))

with open("assets/settings", "r") as file:
    print(decode(file.read()))
