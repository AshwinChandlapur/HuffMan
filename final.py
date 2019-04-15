from heapq import heappush, heappop,heapify
from operator import itemgetter
import textwrap
import numbers

encoded = []

def numberForUniqueChar(li):
    numbering = []
    i=1
    for item in li:
        numbering.append((i,item[0]))
        i = i+1
    return numbering


def freqFinder(s):
    d = {}
    for char in s:
        if d.get(char):
            d[char] += 1
        else:
            d[char] = 1

    li = []
    for key, value in d.items():
        li.append(tuple((key, value)))
    li.sort(key=itemgetter(1), reverse=True)

    return li,d

def binary(decimal) :
    otherBase = ""
    while decimal != 0 :
        otherBase  =  str(decimal % 2) + otherBase
        decimal    //=  2
    appendBits = 8- len(otherBase)
    otherBase = '0'*appendBits+otherBase

    return otherBase

def binary2(decimal) :
    otherBase = ""
    while decimal != 0 :
        otherBase  =  str(decimal % 2) + otherBase
        decimal    //=  2
    # appendBits = 8- len(otherBase)
    # otherBase = '0'*appendBits+otherBase

    return otherBase

def binaryStringMaker(numbering,d,fileInputString):
    binaryString = ""
    numbering = dict(numbering)
    inv_map = dict(zip(numbering.values(), numbering.keys()))
    for item in fileInputString:
        convNum =  inv_map[item]
        binaryString = binaryString + binary(convNum)
    return binaryString

def eightbitdivide(binaryString):
    # binLen = len(binaryString)
    # extrabits = 0
    # if(binLen %8!=0):
    #     extrabits = 8 - (binLen%8)
    #     binaryString = extrabits*'0'+binaryString
    output = [binaryString[i:i + 8] for i in range(0, len(binaryString), 8)]
    lastgroupLength = 8 - len(output[len(output)-1])
    output[len(output) - 1] = "0" * (lastgroupLength) + output[len(output) - 1]
    return output,lastgroupLength

def asciiGenerator(output):
    intValues = []
    for item in output:
        intValues.append(int(item, 2))
    asciiValues = []
    for item in intValues:
        asciiValues.append(chr(item))
    return asciiValues


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

def heapBuilder(treeBuilderList):
    heap = []
    for item in treeBuilderList:
        a = Node(item[0], item[1])
        heappush(heap, a)
    heapify(heap)

    root = None
    while (len(heap) > 1):
        x = heap.pop()
        y = heap.pop()

        f = Node()
        f.freq = x.noFreq() + y.noFreq()
        f.char = "*"

        f.nodeLeft = x
        f.nodeRight = y
        root = f
        heappush(heap, f)

    return heap,root


def treePrint(root,s):
    global  encoded
    try:
        if (root.nodeLeft is None and root.nodeLeft is None):
            encoded.append((root.noChar(), s))

        treePrint(root.getLeft(),s+"0")
        treePrint(root.getRight(),s+"1")
    except:
        pass


def asciiDecoderString(input):
    decoderInt = []
    for char in input:
        decoderInt.append(ord(str(char)))

    decoderBinary = []
    for item in decoderInt:
        decoderBinary.append(binary(item))

    return "".join(decoderBinary)

def main():
    global encoded

    # Step 1
    inputFileName = input("Enter the input File Name or a string you wan to Encode")
    try:
        f = open(inputFileName, "r")
        fileInputString = f.read()
        # Store configuration file values
    except FileNotFoundError:
        fileInputString = inputFileName


    # fileInputString = input("Enter Input")

    # Step 2
    li,d = freqFinder(fileInputString)
    # Step 3
    numbering = numberForUniqueChar(li)

    # Step 4
    binaryString = binaryStringMaker(numbering,d,fileInputString)
    # Step 5
    output, extrabits = eightbitdivide(binaryString)
    # Step 6
    asciiValues = asciiGenerator(output)
    asciiString = "".join(asciiValues)

    #Step 7
    huffmanli,huffmand = freqFinder(asciiString)
    heap,root = heapBuilder(huffmanli)


    if (len(huffmand) == 1):
        print("Your file has same char or only 1 char")
        oneChar = asciiString[0]
        encodedString = ""
        for i in range(0, int(huffmand[asciiString[0]])):
            encodedString = encodedString + "1"
    else:
        treePrint(root, "")
        encoded = dict(encoded)
        # print("After Heap Construction, Binary Value for each character is")
        # print(encoded)
        # print()
        encodedString = ""
        for char in asciiString:
            encodedString = encodedString + encoded[char]

    second8bitDivide,extrabits = eightbitdivide(encodedString)
    secondasciiCode = asciiGenerator(second8bitDivide)
    # print(secondasciiCode)
    #Step 8
    # print("Encoding for the String is " + encodedString)
    f = open("encodedEnhanced.txt", "w", encoding="utf-8")
    f.write("".join(secondasciiCode))
    f.close()


    # print("---------------Decoding Begins--------------")

    #Step 1
    f = open("encodedEnhanced.txt", "r", encoding="utf-8")
    inputForDecode = f.read()

    inputForDecode = asciiDecoderString(inputForDecode)
    output,extrabits = eightbitdivide(inputForDecode)


    a =  output[len(output)-1]
    a = int(a,2)
    a = binary2(a)
    output[len(output) - 1] = str(a)
    inputForDecode = "".join(output)

    #Step 2
    inv_map = dict(zip(encoded.values(), encoded.keys()))
    # print(inv_map)

    decodedAscii = ""
    s = ""
    for char in inputForDecode:
        s = s + char
        if s in inv_map:
            decodedAscii = decodedAscii + inv_map[s]
            s = ""
    print()
    # print("Decoded String is "+decodedAscii)

    #step 3
    decodedInt = []
    for char in decodedAscii:
        decodedInt.append(ord(char))

    decodedBinary = ""
    for item in decodedInt:
        decodedBinary = decodedBinary+ binary(item)
    # print(decodedBinary)
    # print(decodedBinary[extrabits:])

    numbering = dict(numbering)

    decoder = textwrap.wrap(decodedBinary, 8)
    decoderInt = []
    for item in decoder:
        decoderInt.append(int(item, 2))
    # print(decoderInt)

    # inv_map = {v: k for k, v in numbering.items()}
    # print(inv_map)
    decodedString =""
    for item in decoderInt:
        decodedString = decodedString + numbering[item]

    # print(decodedString)

    f = open("decodedEnchanced.txt", "w", encoding="utf-8")
    f.write(decodedString)
    f.close


if __name__=="__main__":
    main()