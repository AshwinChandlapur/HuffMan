from heapq import heappush, heappop,heapify
from operator import itemgetter
import time

encoded = []
specialChar = ["!","@","#","$","%","^","&","*","(",")","{","}","|","[","]",";",":","'","<",">","?","/",",",".","/"," ","\n","\t","~","=","-","`","’","+","_",'"',"","–","°","—"]
numbers = ["1","2","3","4","5","6","7","8","9","0"]
last = ""
oneChar = ""



class Node():
    def __init__(self,char = None,freq = None):
        self.char = char
        self.freq = freq
        self.nodeLeft = None
        self.nodeRight = None

    def __str__(self):
        return "Char is %s, Freq is %s" % (self.char, self.freq)

    def __lt__(self, other):
        return self.freq > other.freq

    def noFreq(self):
        return self.freq

    def noChar(self):
        return self.char

    def getLeft(self):
        return self.nodeLeft

    def getRight(self):
        return self.nodeRight


def treePrint(root,s):
    global  encoded
    try:
        if (root.nodeLeft is None and root.nodeLeft is None):
            encoded.append((root.noChar(), s))

        treePrint(root.getLeft(),s+"0")
        treePrint(root.getRight(),s+"1")
    except:
        pass

def main():
    global encoded
    global last
    global oneChar
    # Step 1
    inputFileName = input("Enter the input File Name or a string you wan to Encode")
    try:
        f = open(inputFileName, "r")
        s = f.read()
        # Store configuration file values
    except FileNotFoundError:
        s = inputFileName

    # s = input("Enter Input")
    start = time.time()
    d = {}
    for char in s:
        if d.get(char):
            d[char]+=1
        else:
            d[char]=1

    li = []
    for key,value in d.items():
        li.append(tuple((key,value)))
    li.sort(key=itemgetter(1),reverse=True)
    print(li)

    print("---------------------Encoding--------------------------------------")
    heap = []
    for item in li:
        a = Node(item[0],item[1])
        heappush(heap,a)
    heapify(heap)

    root = None
    while(len(heap)>1):
        x = heap.pop()
        y = heap.pop()

        f = Node()
        f.freq = x.noFreq()+y.noFreq()
        f.char = "*"

        f.nodeLeft = x
        f.nodeRight = y
        root = f
        heappush(heap,f)


    if(len(s)==0):
        print("Length is 0")
        return
    if(len(d)==1):
        print("Your file has same char or only 1 char")
        oneChar = s[0]
        encodedString = ""
        for i in range(0,int(d[s[0]])):
            encodedString = encodedString+"1"
    else:
        treePrint(root,"")
        encoded = dict(encoded)
        print("After Heap Construction, Binary Value for each character is")
        print(encoded)
        print()
        encodedString =""
        for char in s:
            encodedString = encodedString + encoded[char]

    print("Encoding for the String is "+encodedString)

    output = [encodedString[i:i + 8] for i in range(0, len(encodedString), 8)]
    print("Dividing into 8 bits ->"+str(output))
    last = output[len(output)-1]

    finalEncodedBinary = []
    for item in output:
        finalEncodedBinary.append(int(item, 2))
    print("In Int Val-> "+ str(finalEncodedBinary))
    print()

    finalEncodedAscii = []
    for item in finalEncodedBinary:
        finalEncodedAscii.append(chr(item))
    print("To be Written to the File is "+str(finalEncodedAscii))

    encodeEnd = time.time() -start
    # print()


    f = open("encoded.txt", "w",encoding="utf-8")
    f.write(''.join(finalEncodedAscii))
    f.close()

    print("-------------------------Decoding--------------------------------")
    start = time.time()
    decodedString = decode()
    end = time.time()-start
    print(encodeEnd)
    print(end)
    f = open("decoded.txt", "w", encoding="utf-8")
    f.write(decodedString)
    f.close


def decode():

    f = open("encoded.txt", "r",encoding="utf-8")
    s = f.read()
    utfToInt = []
    for char in s:
        utfToInt.append(ord(char))
    print("Decoded Int Values")
    print(utfToInt)
    print()

    intToBin = []
    for item in utfToInt:
        intToBin.append("{0:{fill}8b}".format(int(item),fill='0'))

    intToBin[len(intToBin)-1] = last


    binaryString = "".join(intToBin)
    print("Decoded Binary String "+ binaryString)

    samechar = True
    for i in range(len(binaryString)-1,0,-1):
        if binaryString[i]!=binaryString[i-1]:
            samechar = False

    decodedString = ""
    if not samechar:
        inv_map = dict(zip(encoded.values(), encoded.keys()))
        # print(inv_map)
        s = ""
        for char in binaryString:
            s = s+char
            if s in inv_map:
                decodedString = decodedString+inv_map[s]
                s =""
        print()
        print("Actual String is")
        print(decodedString)
    else:
        print()
        print("Actual String is")
        decodedString = len(binaryString)*oneChar
        print(len(binaryString)*oneChar)

    return decodedString


if __name__=="__main__":
    main()