
def main():
    fi = open("bible.txt", "r")

    for i in range(0,100):
        s =""
        for j in range(0,100):
            s  = s + fi.readline()
        filename = "file"+str(i)+".txt"
        f = open(filename, "a+")
        f.write(s)
        f.close






if __name__=="__main__":
    main()