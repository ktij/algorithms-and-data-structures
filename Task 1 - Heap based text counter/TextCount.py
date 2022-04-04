# TASK 1

lstSep = [' ', '\n', '\t']
lstPunc = ['.', ',', '?', '!', ':', ';', '"']
lstArt = ['a', 'an', 'the']
lstVerbs = ['am', 'is', 'are', 'was', 'were', 'has', 'have', 'had', 'been', 'will', 'shall', 'may', 'can', 'would', 'should', 'might', 'could']

def itemInList(item, lst):
    '''
    Returns True if item in lst and returns False otherwise
    :param item: target to look for in lst
    :param lst: list to search for item
    :returns: True if item in list, False otherwise
    Time complexity: O(x) where x is number of elements in the list
    Space complexity: O(x) where x is number of elements in the list
    '''
    for i in lst:
        if i == item:
            return True
    return False

def preprocess(filename):
    '''
    Returns a list of words in the given text file excluding articles and auxiliary verbs
    :param filename: Name (path) of textfile to read
    :returns: List containing words in text file excluding articles and auxiliary verbs
    Time complexity (best and worst): O(x) where x is number of characters in the text file (Under O(mn) since input is expected to have space complexity of O(mn))
    Space complexity: O(x) where x is number of characters in the text file (Under O(mn) since input is expected to have space complexity of O(mn))
    '''
    ListOfWords = []

    f = open(filename)
    s = f.read()

    tempString = ''
    for i in s:
        if itemInList(i, lstSep) or itemInList(i, lstPunc):
            if tempString != '':
                if itemInList(tempString, lstArt) == False and itemInList(tempString, lstVerbs) == False:
                    ListOfWords.append(tempString)
                tempString = ''
        else:
            tempString += i
    
    return ListOfWords

# print(preprocess('Writing.txt'))

# TASK 2

def cord(char):
    '''
    Convert letter to corresponding number
    :param char: String containing single character
    :returns: Integer representing associated number
    Time complexity: O(1) as it does not depend on input
    Space complexity: O(1) as it does not depend on input
    '''
    lstChar = ['0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(len(lstChar)):
        if lstChar[i] == char:
            return i

def wordSort(ListOfWords):
    '''
    Sorts a list of words
    :param ListOfWords: List containing lowercase words
    :returns: Sorted list of words
    Time complexity: O(mn)
    Space complexity: O(mn)
    '''
    # find m
    m = 0
    for i in ListOfWords:
        if len(i) > m:
            m = len(i)
    # create lst with all words of equal length (by adding zeroes at the end)
    lst = ListOfWords[:]
    for i in range(len(lst)):
        while len(lst[i]) < m:
            lst[i] = lst[i] + '0'
    
    # radix sort
    lstCount = [0]*27
    lstIndex = [0]*27
    output = [0]*len(ListOfWords)
    
    for n in range(m-1, -1, -1):
        #lstCount
        for word in lst:
            lstCount[ cord(word[n]) ] += 1
        #lstIndex
        runningTotal = 0
        for i in range(len(lstCount)):
            lstIndex[i] = runningTotal
            runningTotal += lstCount[i]
        #output
        for word in lst:
            o = cord(word[n])
            output[lstIndex[o]] = word
            lstIndex[o] += 1
        # reset values
        lstCount = [0]*27
        lstIndex = [0]*27
        lst = output[:]

    # remove all 0s once you're done
    for i in range(len(output)):
        while output[i][-1] == '0':
            output[i] = output[i][:-1]
    
    return output

# print(wordSort(preprocess('Writing.txt')))

# TASK 3

def wordCount(sortedList):
    '''
    Finds number of each item in sorted list
    :param sortedList: Sorted list containing words
    :returns: List containing total number of items along with lists with first index representing word and second index representing the numbe of time that word occurs
    Time complexity: 
    Space complexity: O(mn)
    '''
    sortedList += [False]
    returnList = [len(sortedList)-1]

    tmp = sortedList[0]
    count = 1
    for i in range(1, len(sortedList)):
        if sortedList[i] == tmp:    # next item is same as before
            count += 1
        else:   # next item is different from previous item
            returnList.append( [tmp, count] )
            count = 1
            tmp = sortedList[i]

    return returnList
            
# print(wordCount(wordSort(preprocess('Writing.txt'))))

# TASK 4

def kTopWords(wordCount, k):
    '''
    Finds k top words with highest frequency whilst maintaining stability
    :param wordCount: List containing words and their frequency
    :param k: Number of items to return
    :returns: List containing k top words with highest frequency
    Time complexity: O(nlog(k))
    Space complexity: O(km)
    '''

    wordCount = wordCount[1:]
    if k > len(wordCount):
        k = len(wordCount)

    def RearrangeRoot():
        i = 0
        leftI = i*2+1
        rightI = i*2+2
        # while i > child, swap with smaller child (or bigger index if both are equal)
        while rightI < len(minheap) and (minheap[i][1] > minheap[leftI][1] or minheap[i][1] > minheap[rightI][1]): # while right child exists and node is greater than either child
            swapI = -1  # index to swap i with
            if minheap[rightI][1] == minheap[leftI][1]:
                if minheap[rightI][2] > minheap[leftI][2]:
                    swapI = rightI
                else:
                    swapI = leftI
            elif minheap[rightI][1] > minheap[leftI][1]:
                swapI = leftI
            else:
                swapI = rightI
            minheap[i], minheap[swapI] = minheap[swapI], minheap[i]
            i = swapI
            leftI = i*2+1
            rightI = i*2+2
        # just check the left child before we exit
        if leftI < len(minheap) and minheap[i][1] > minheap[leftI][1]:
            minheap[i], minheap[leftI] = minheap[leftI], minheap[i]

    # add index values to wordcount
    for i in range(len(wordCount)):
        wordCount[i].append(i)
    
    # build minheap with first k elements in array
    minheap = []
    for index in range(k):
        minheap.append(wordCount[index])
        i = len(minheap)-1 # i = last index of nlst
        while i != 0 and minheap[i][1] <= minheap[(i-1)//2][1]: # while node <= parent: swap (this way new nodes end up on top)
            minheap[i], minheap[(i-1)//2] = minheap[(i-1)//2], minheap[i]
            i = (i-1)//2

    # fit remaining elemts in minheap
    for i in range(k, len(wordCount)):
        if wordCount[i][1] > minheap[0][1]:   # if word belongs in minheap
            minheap[0] = wordCount[i]   # replace root with next item in wordCount
            RearrangeRoot() # find appropriate position

    # now that heap of size k is formed, pop and add to returnlist in reverse order
    returnlist = [None] * k
    for i in range(k-1, -1, -1):
        returnlist[i] = minheap[0]
        minheap[0] = minheap[-1]
        minheap = minheap[:-1]
        RearrangeRoot()

    return returnlist

# print(kTopWords(wordCount(wordSort(preprocess('Writing.txt'))), 10))

def main():
    filename = 'Writing.txt'
    # task 1
    preprocessedList = preprocess(filename)
    print('Words are preprocessed..')
    b = input('Do I need to display the remaining words: ')
    yn = ['Y', 'N']
    while b not in yn:
        print('Please enter a valid input')
        b = input('Do I need to display the remaining words: ')
    if b == 'Y':
        for i in preprocessedList:
            print(i)
    print()
    # task 2
    sortedList = wordSort(preprocessedList)
    print('The remaining words are sorted in alphabetical order')
    b = input('Do you want to see: ')
    while b not in yn:
        print('Please enter a valid input (Y/N)')
        b = input('Do I need to display the remaining words: ')
    if b == 'Y':
        for i in sortedList:
            print(i)
    print()
    # task 3
    countList = wordCount(sortedList)
    print('The total number of words in the writing:', countList[0])
    print('The frequencies of each word:')
    for i in range(1, len(countList)):
        print(countList[i][0],':',countList[i][1])
    print()
    # task 4
    k = input('How many top-most frequent words do I display: ')
    while True:
        try:
            k = int(k)
            break
        except:
            print('Please enter a valid input')
            k = input('How many top-most frequent words do I display: ')
    print(k, 'top most words appear in the writing are:')
    topwords = kTopWords(countList, k)
    for i in topwords:
        print(i[0], ':', i[1])
        

try:
    main()
except:
    print('Invalid input, please try again')
    main()