print("[", end="")

for i in range(200):
    print(F'"{input()}"',end="")
    if (i < 199):
        print(",")

print("]", end="")
