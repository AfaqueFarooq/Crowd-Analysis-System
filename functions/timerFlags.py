
def setFlag(flag):
    file = open("functions/lock.text", "w")
    file.write(flag)
    file.close()

def getFlag():
    file = open("functions/lock.text", "r")
    if file.readline() == "false":
        file.close()
        return False
    file.close()
    return True

    