from modules.encryption import *

with open("assets/default_settings", "r") as file:
    print(encode(file.read()))
