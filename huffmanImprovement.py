from heapq import heappush, heappop,heapify
from operator import itemgetter
import time

encoded = []
secondEncoded = []
specialChar = ["!","@","#","$","%","^","&","*","(",")","{","}","|","[","]",";",":","'","<",">","?","/",",",".","/"," ","\n","\t","~","=","-","`","’","+","_",'"',"","–","°","—"
               ,"»","\x01"]
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


def treePrint(root,s,encoded):
    try:
        if (root.nodeLeft is None and root.nodeLeft is None):
            encoded.append((root.noChar(),s))
            return
        treePrint(root.getLeft(),s+"0")
        treePrint(root.getRight(),s+"1")
    except:
        pass

    return encoded


def binary(decimal) :
    otherBase = ""
    while decimal != 0 :
        otherBase  =  str(decimal % 2) + otherBase
        decimal    //=  2
    return otherBase


def freqFinder(s):
    d = {}
    for char in s:
        if d.get(char):
            d[char] += 1
        else:
            d[char] = 1
    return d

def preencode(s):

    d = freqFinder(s)
    numericD = []
    i = 1
    for key, value in d.items():
        numericD.append((key, i))
        i = i + 1

    codeString = ""
    for item in numericD:
        codeString = codeString + str(binary(item[1]))

    output = [codeString[i:i + 8] for i in range(0, len(codeString), 8)]
    lastlen = len(output[len(output) - 1])
    output[len(output) - 1] = '0' * (8 - lastlen) + output[len(output) - 1]

    firstEncoding = []
    for item in output:
        x = chr(int(item, 2))
        firstEncoding.append(x)
    print(firstEncoding)

    newDict = {}
    for item in firstEncoding:
        if newDict.get(item):
            newDict[item] += 1
        else:
            newDict[item] = 1

    newString = ""
    newli = []
    for key, value in newDict.items():
        newString = newString + str(key)
        newli.append(tuple((key, value)))
    newli.sort(key=itemgetter(1), reverse=True)

    return newString,newli,newDict


def addingHeap(newli):
    heap = []
    for item in newli:
        a = Node(item[0], item[1])
        heappush(heap, a)
    heapify(heap)
    return heap


def main():
    # f = open("big.txt", "r")
    # s = f.read()
    s = input("Enter Your Input Text")

    print("---------------------Encoding--------------------------------------")
    newString,newli,newDict = preencode(s)
    heap = addingHeap(newli)

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


    secondEncoded = []
    if(len(newString)==0):
        print("Length is 0")
        return
    if(len(newDict)==1):
        print("Your file has same char or only 1 char")
        oneChar = newString[0]
        encodedString = ""
        for i in range(0,int(newDict[s[0]])):
            encodedString = encodedString+"1"
    else:
        secondEncoded = treePrint(root,"",secondEncoded)
        secondEncoded = dict(secondEncoded)
        print("After Heap Construction, Binary Value for each character is")
        print(secondEncoded)
        print()
        encodedString =""
        for char in newString:
            encodedString = encodedString + str(secondEncoded[char])
    #
    print("Encoding for the String is "+encodedString)
    #
    # output = [encodedString[i:i + 8] for i in range(0, len(encodedString), 8)]
    # print("Dividing into 8 bits ->"+str(output))
    # last = output[len(output)-1]
    #
    # finalEncodedBinary = []
    # for item in output:
    #     finalEncodedBinary.append(int(item, 2))
    # print("In Int Val-> "+ str(finalEncodedBinary))
    # print()
    #
    # finalEncodedAscii = []
    # for item in finalEncodedBinary:
    #     finalEncodedAscii.append(chr(item))
    # print("To be Written to the File is "+str(finalEncodedAscii))
    #
    # encodeEnd = time.time() -start
    # print()
    #
    #
    # f = open("encoded.txt", "w",encoding="utf-8")
    # f.write(''.join(finalEncodedAscii))
    # f.close()
    #
    # print("-------------------------Decoding--------------------------------")
    # start = time.time()
    # decodedString = decode()
    # end = time.time()-start
    # print(encodeEnd)
    # print(end)
    # f = open("decoded.txt", "w", encoding="utf-8")
    # f.write(decodedString)
    # f.close
    # print("-------------------------Second Decoding--------------------------------")
    # print(secondDecode(decodedString))



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

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

def secondDecode(decodedString):
    global secondEncoded
    print(decodedString)
    utfToInt = []
    for char in decodedString:
        utfToInt.append(ord(char))
    print("Decoded Int Values")
    print(utfToInt)
    print()

    intToBin = []
    for item in utfToInt:
        intToBin.append("{0:{fill}8b}".format(int(item), fill='0'))

    intToBin[len(intToBin) - 1] = last

    binaryString = "".join(intToBin)
    print("Decoded Binary String " + binaryString)

    samechar = True
    for i in range(len(binaryString) - 1, 0, -1):
        if binaryString[i] != binaryString[i - 1]:
            samechar = False

    print(secondEncoded)
    decodedString = ""
    if not samechar:
        inv_map = dict(zip(secondEncoded.values(), secondEncoded.keys()))
        # print(inv_map)
        s = ""
        for char in binaryString:
            s = s + char
            if s in inv_map:
                decodedString = decodedString + inv_map[s]
                s = ""
        print()
        print("Actual String is")
        print(decodedString)
    else:
        print()
        print("Actual String is")
        decodedString = len(binaryString) * oneChar
        print(len(binaryString) * oneChar)
    return decodedString


if __name__=="__main__":
    main()