#!/usr/bin/env python3

import random

print("Content-Type: text/html")
print()
print("<img src= '../dogs/" + str(random.randint(1, 3)) + ".jpg'>")

