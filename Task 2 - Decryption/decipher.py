
class Decipher():

    def __init__(self):
        self.message = False

    def getMessage(self):
        '''
        Returns stored message
        Time complexity: O(1)
        Space complexity: O(1)
        Error handle: None
        Return: message stored
        Parameter: None
        Pre-requisite: None
        '''
        if self.message == False:
            return ''
        else:
            return self.message

    def messageFind(self, filepath):
        '''
        Finds message from encrypted.txt
        Time complexity: O(nm)
        Space complexity: O(nm)
        Error handle: None
        Return: None
        Parameter: filepath of encrypted file
        Pre-requisite: None
        '''
        s = open(filepath).read().strip().split('\n')
        s1, s2 = s[0], s[1]
        
        # create array
        arr = []
        for i in range(len(s2)+1):  # O(m)
            arr.append( [0] * (len(s1)+1) )
        # fill out table    O(nm)
        for i in range( 0, len(s2) ):
            for o in range( 0, len(s1) ):
                if s1[o] == s2[i]:
                    arr[i+1][o+1] = arr[i][o] + 1
                else:
                    arr[i+1][o+1] = max ( arr[i][o+1] , arr[i+1][o] )
        # backtrack
        returnList = []
        i = len(arr)-2
        o = len(arr[0])-2
        while arr[i+1][o+1] != 0:   # O(n+m)
            if s1[o] == s2[i]:
                returnList.append(s1[o])
                i -= 1
                o -= 1
            else:
                if arr[i+1][o] > arr[i][o+1]:
                    o -= 1
                else:
                    i -= 1
        # reverse list and create string
        returnList = returnList[::-1]
        returnString = ''
        for i in returnList:
            returnString += i

        self.message = returnString

    def cord(self, char):
        '''
        Convert letter to corresponding number
        :param char: String containing single character
        :returns: Integer representing associated number
        Time complexity: O(1) as it does not depend on input
        Space complexity: O(1) as it does not depend on input
        '''
        if char == '0':
            return 1
        else:
            return 0

    def wordSort(self, ListOfWords):
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
                lstCount[ self.cord(word[n]) ] += 1
            #lstIndex
            runningTotal = 0
            for i in range(len(lstCount)):
                lstIndex[i] = runningTotal
                runningTotal += lstCount[i]
            #output
            for word in lst:
                o = self.cord(word[n])
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

    def wordBreak(self, filepath):
        '''
        Splits message into words
        Time complexity: O(KNM)
        Space complexity: O(NM+K)
        Error handle: None
        Return: None
        Parameter: filepath of dictionary file
        Pre-requisite: None
        '''
        if filepath == '':
            return
        
        dic = open(filepath).read().strip().split('\n')
        
        # find M (max) - O(MN)
        M = 0
        for i in dic:
            if len(i) > M:
                M = len(i)
        # make all strings in dic of size M by adding 0's at start - O(MN)
        for i in range(len(dic)):
            while len(dic[i]) < M:
                dic[i] = '0' + dic[i]
        
        # radix sort (kinda) - O(MN)
        dic = self.wordSort(dic)

        # remove 0's - O(MN)
        for i in range(len(dic)):
            while dic[i][0] == '0':
                dic[i] = dic[i][1:]

        # substring search
        strK = self.message
        K = []
        for i in strK:
            K.append(i)
        returnList = [None] * len(K)

        for word in dic:    # for each word in dic - N
            x = 0
            while x+len(word) <= len(K):    # moving word along K - K
                match = True
                for i in range(len(word)):  # compare word with K - M
                    if K[x+i] != word[i]:
                        match = False
                        break
                if match == True:   # if match is found
                    # GLOSSARY
                    # 0 = start letter
                    # 1 = middle letter/unused letter (both follow the same rules)
                    # 2 = end letter
                    # 3 = one word letter

                    # add word to returnList
                    if len(word) == 1:  # special case
                        returnList[ x+i ] = (word, 3)
                    else:
                        for i in range(len(word)):  # add word to returnList - M
                            if i == 0:  # start letter
                                returnList[ x+i ] = (word[i], 0)
                            elif i == len(word)-1:  # end letter
                                returnList[ x+i ] = (word[i], 2)
                            else:   # middle letter
                                returnList[ x+i ] = (word[i], 1)
                    # remove word from string to prevent overlap - M
                    for i in range(len(word)):
                        K[x+i] = None
                x += 1

        # fill all Nones in returnList - K
        for i in range(len(returnList)):
            if returnList[i] == None:
                returnList[i] = (K[i], 1)

        # create final string and save
        mes = ''
        for i in returnList:
            if i[1] == 0:   # if start letter
                if mes == '' or mes[-1] == ' ':
                    mes += i[0]
                else:
                    mes += ' ' + i[0]
            elif i[1] == 2: # if end letter
                mes += i[0] + ' '
            elif i[1] == 3: # if one word letter
                if mes == '' or mes[-1] == ' ':
                    mes += i[0] + ' '
                else:
                    mes += ' ' + i[0] + ' '
            else:   # if neither
                mes += i[0]

        self.message = mes.strip()


if __name__ == '__main__':
    cont = True
    while cont == True:
        enc_file = input('The name of the file, contains two encrypted texts : ')
        dic_file = input('The name of the dictionary file : ')
        try:
            d = Decipher()
            d.messageFind(enc_file)
            print('---------------------------------------------------------------------')
            print('Deciphered message is', d.getMessage())
        except:
            print('\nInvalid file input, please try again\n')
            continue
        try:    
            d.wordBreak(dic_file)
        except:
            pass
        print('True message is', d.getMessage())
        print('---------------------------------------------------------------------\nProgram end')
        cont = False
        
