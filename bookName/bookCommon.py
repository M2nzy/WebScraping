def fileWrite(fname, file1, file2, file3):
    yes24 = file1.readlines()
    kyobo = file2.readlines()
    aladdin = file3.readlines()

    presult = set(yes24) & set(kyobo)
    result = presult & set(aladdin)

    fresult = open(fname, "w")
    result = list(result)

    for line in result:
        line = str(line.replace("nhn", "php"))
        fresult.write(line)


fyes = open("./yes24BS.txt", "r")
fkyobo = open("./kyoboBS.txt", "r")
faladdin = open("./aladdinBS.txt", "r")

fileWrite("./bookCommon.txt",fyes, fkyobo, faladdin)
