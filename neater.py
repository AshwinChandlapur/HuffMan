from heapq import heappush, heappop,heapify
from operator import itemgetter

specialChar = ["!","@","#","$","%","^","&","*","(",")","{","}","|","[","]",";",":","'","<",">","?","/",",",".","/"," ","\n","\t","~","=","-","`","’","+","_",'"',"","–","°","—"]
numbers = ["1","2","3","4","5","6","7","8","9","0"]
encoded = []
encoded2 = []

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

    return li

def numberForUniqueChar(li):
    numbering = []
    i=1
    for item in li:
        numbering.append((i,item[0]))
        i = i+1
    return numbering


def binary(decimal) :
    otherBase = ""
    while decimal != 0 :
        otherBase  =  str(decimal % 2) + otherBase
        decimal    //=  2
    return otherBase

def binaryStringMaker(numbering):
    binaryString = ""
    for item in numbering:
        binaryString = binaryString + binary(int(item[0]))
    return binaryString

def eightbitdivide(binaryString):
    binLen = len(binaryString)
    extrabits = 0
    if(binLen %8!=0):
        extrabits = 8 - (binLen%8)
        binaryString = extrabits*'0'+binaryString
    output = [binaryString[i:i + 8] for i in range(0, len(binaryString), 8)]
    # lastgroupLength = 8 - len(output[len(output)-1])
    # output[len(output)-1] = "0"*(lastgroupLength) + output[len(output)-1]
    return output,extrabits

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
    global encoded
    try:
        if (root.nodeLeft is None and root.nodeLeft is None):
            encoded.append((root.noChar(), s))
        treePrint(root.getLeft(),s+"0")
        treePrint(root.getRight(),s+"1")
    except:
        pass

def treePrint2(root,s):
    global encoded2
    try:
        if (root.nodeLeft is None and root.nodeLeft is None):
            encoded2.append((root.noChar(), s))
        treePrint(root.getLeft(),s+"0")
        treePrint(root.getRight(),s+"1")
    except:
        pass

def utfToInt(input):
    utfToInt = []
    for char in input:
        utfToInt.append(ord(char))
    return utfToInt


def intToBins(intValOfEncodedFile):
    intToBin = []
    for item in intValOfEncodedFile:
        intToBin.append("{0:{fill}8b}".format(int(item), fill='0'))
    return intToBin


def main():
    global encoded
    fileInputString = input("Enter Input")
    # f = open("big.txt", "r", encoding="utf-8")
    # fileInputString = f.read()
    # First Huffman Tree
    usage = firstEncoder(fileInputString)

    li = freqFinder(fileInputString)
    numbering = numberForUniqueChar(li)
    binaryString = binaryStringMaker(numbering)
    output,extrabits = eightbitdivide(binaryString)
    print(output)
    print(extrabits)
    asciiValues = asciiGenerator(output)

    treeBuilderDict = freqFinder("".join(asciiValues))
    print(treeBuilderDict)
    treeBuilderString = "".join(asciiValues)
    heap,root = heapBuilder(treeBuilderDict)
    treePrint(root,"")
    encoded = dict(encoded)
    encodedString = ""
    for char in treeBuilderString:
        encodedString = encodedString + encoded[char]
    compressString,extrabits2 = eightbitdivide(encodedString)
    writethistoFile = asciiGenerator(compressString)

    print("Writing this to file")
    print(writethistoFile)
    f = open("encoded.txt", "w", encoding="utf-8")
    f.write("".join(writethistoFile))
    f.close
    print("---------Encoding Done Right---------------")


    print()
    print("Decoding Starting......")
    f = open("encoded.txt", "r", encoding="utf-8")
    sentencefromEncoded = f.read()
    intValOfEncodedFile = utfToInt(sentencefromEncoded)
    intToBinOfEncodedFile = intToBins(intValOfEncodedFile)

    binaryString = "".join(intToBinOfEncodedFile)
    print("Decoded Binary String " + binaryString)
    binaryString = binaryString[extrabits2:]
    print("Decoded Binary String " + binaryString)

    firstlevelDecoder = ""
    inv_map = dict(zip(encoded.values(), encoded.keys()))
    print(inv_map)
    internalString = ""
    for char in binaryString:
        internalString = internalString + char
        if internalString in inv_map:
            firstlevelDecoder = firstlevelDecoder + inv_map[internalString]
            internalString = ""
    print()
    print("Actual String is")
    print(firstlevelDecoder)

    intOfFirstDecoder = utfToInt(firstlevelDecoder)
    print(intOfFirstDecoder)

    binOfFirstDecoder =""
    for item in intOfFirstDecoder:
         binOfFirstDecoder= binOfFirstDecoder+binary(item)

    print(binOfFirstDecoder)


def firstEncoder(fileInputString):
    global encoded2
    d = {}
    li = []
    print(fileInputString)
    for char in fileInputString:
        if d.get(char):
            d[char] += 1
        else:
            d[char] = 1
    for key, value in d.items():
        li.append(tuple((key, value)))
    li.sort(key=itemgetter(1), reverse=True)
    print(li)
    print("-----------------First Encoder---------------")
    heap = []
    for item in li:
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

    treePrint2(root, "")
    encoded2 = dict(encoded2)
    print("After Heap Construction, Binary Value for each character is")
    print(encoded2)
    print()


if __name__=="__main__":
    main()
