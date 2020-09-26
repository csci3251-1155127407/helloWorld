# import wordninja

# for i in range(5200):
#     print(" ".join(wordninja.split(input())))

for i in range(200):
    s = []
    t = []
    mn = 999
    for j in range(26):
        # print(input())
        s += [input()]
        t += [s[-1].split(" ")]
        mn = min(mn, len(t[-1]))

    for j in range(26):
        if (len(t[j]) == mn):
            print(s[j])

