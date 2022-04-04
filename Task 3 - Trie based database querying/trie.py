
def cord(letter):
    '''
    Converts letter to corresponding int
    Time complexity: O(1)
    Space complexity: O(1)
    Error handle: None
    Return: Corresponding number
    Parameter: letter
    Pre-requisite: None
    '''
    return ord(letter.lower())-96

def trieEdge():
    '''
    Returns list template that can be used to represent letter edge
    Time complexity: O(1)
    Space complexity: O(1)
    Error handle: None
    Return: Template list
    Parameter: None
    Pre-requisite: None
    '''
    return [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,[]]

def idTrieEdge():
    '''
    Returns list template that can be used to represent id edge
    Time complexity: O(1)
    Space complexity: O(1)
    Error handle: None
    Return: Template list
    Parameter: None
    Pre-requisite: None
    '''
    return [None,None,None,None,None,None,None,None,None,None,[]]

def query(filename, id_prefix, last_name_prefix):
    '''
    Querys database and gets relevant results
    Time complexity: O(NM * T + k + l + nk + nl)
    Space complexity: O(T+NM)
    Error handle: None
    Return: List of results
    Parameter: id_prefix - string containing ID prefix, last_name_prefix - string containing last name prefix
    Pre-requisite: None
    '''
    last_name_prefix = last_name_prefix.lower()
    # Create prefix trie for names
    #for each name
    file = open(filename)
    nameTrie = trieEdge()
    for line in file:   # loops N times
        l = line.split(' ') # M times
        index = int(l[0])
        name = l[3].strip()
        #create prefix trie
        list2append2 = nameTrie
        for letter in name: # iterations of this loop x iterations of outer loop = T
            i = cord(letter)
            if list2append2[i] == None:
                list2append2[i] = trieEdge()
            list2append2[i][-1].append(index)
            list2append2 = list2append2[i]
        list2append2 = nameTrie
    file.close()

    # Create prefix trie for ID's
    #for each name
    file = open(filename)
    idTrie = idTrieEdge()
    for line in file:   # loops N times
        l = line.split(' ') # M times
        index, id = int(l[0]), l[1]
        #create prefix trie
        list2append2 = idTrie
        for char in id: # # iterations of this loop x iterations of outer loop = T
            i = int(char)
            if list2append2[i] == None:
                list2append2[i] = idTrieEdge()
            list2append2[i][-1].append(index)
            list2append2 = list2append2[i]
        list2append2 = idTrie

    # Return results for name
    lst2go2 = nameTrie
    for letter in last_name_prefix: # loops l times
        i = cord(letter)
        if lst2go2[i] == None:
            resultName = []
            break
        else:
            lst2go2 = lst2go2[i]
    resultName = lst2go2[-1]

    # Return results for id
    lst2go2 = idTrie
    for char in id_prefix:  # loops k times
        i = int(char)
        if lst2go2[i] == None:
            resultID = []
            break
        else:
            lst2go2 = lst2go2[i]
    resultID = lst2go2[-1]

    # Combine results
    commonList = []
    resultName.append(None) # None marks end of the lists
    resultID.append(None)
    i,n = 0,0
    while resultName[n] != None and resultID[i] != None:    # stop once either pointer hits None, loops maximum of nk+nl times
        if resultName[n] == resultID[i]:
            commonList.append(resultName[n])
            n += 1
            i += 1
        elif resultName[n] > resultID[i]:
            i += 1
        else:
            n += 1

    return(commonList)


def reverseSubstrings(filename):
    '''
    Reverse substring search
    Time complexity: O(K^2)
    Space complexity: O(K^2 + P)
    Error handle: None
    Return: Palindromic substrings and their index in the original array
    Parameter: filename
    Pre-requisite: None
    '''
    s = open(filename).read().strip()   # k times
    rs = ''
    for i in range(len(s)-1,-1,-1): # k times
        rs += s[i]
    # create suffix array for rs
    suffix_array_rs = []
    for i in range(len(rs)):    # k times
        suffix_array_rs.append(rs[i:])
    # create suffix tree for rs 
    suffixTrie = trieEdge()
    for suffix in suffix_array_rs:  # k times
        list2append2 = suffixTrie
        for letter in suffix:       # k times
            i = cord(letter)
            if list2append2[i] == None:
                list2append2[i] = trieEdge()
            list2append2 = list2append2[i]
        list2append2 = suffixTrie
    # create suffix array for s
    suffix_array_s = []
    for i in range(len(s)):     # k times
        suffix_array_s.append(s[i:])
    # search tree
    finalResult = []
    for index in range(len(suffix_array_s)):    # k times
        word = suffix_array_s[index]
        lst2go2 = suffixTrie
        length = 1
        for letter in word: # k times
            i = cord(letter)
            if lst2go2[i] == None:
                # if length >= 2:
                #     finalResult.append([word[:length], index])
                break
            else:
                if length >= 2:
                    finalResult.append([word[:length], index])
                lst2go2 = lst2go2[i]
            length += 1
        length = 1

    return finalResult

while True:
    try:
        print('TASK-1:')
        print('---------------------------------------------------------------------')
        filename = input('Enter the file name of the query database : ')
        idPrefix = input('Enter the prefix of the identification number: ')
        namePrefix = input('Enter the prefix of the last name : ')
        print('---------------------------------------------------------------------')
        result = query(filename, idPrefix, namePrefix)
        print(len(result), 'record found')
        for i in result:
            print('Index number :', i)
        print('---------------------------------------------------------------------')
        print('TASK-2:')
        filename = input('Enter the file name for searching reverse substring: ')
        print('---------------------------------------------------------------------')
        result = reverseSubstrings(filename)
        outstr = ''
        for i in result:
            outstr += i[0] + '(' + str(i[1]) + ')' + ','
        print(outstr[:-1])
        print('---------------------------------------------------------------------')
        print('Program end')
        break
    except:
        print('Invalid input, please try again')