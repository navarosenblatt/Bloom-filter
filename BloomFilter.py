from BitHashcopy import BitHash
from BitVectorcopy import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.  
    # You use equation B to get the desired phi from P and d
    # You then use equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        n = numKeys
        d = numHashes
        P = maxFalsePositive
        
        phi = (1 - (P)**(1/d))
        N = d/(1 - (phi)**(1/n))
        return int(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        
        num = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        self.__bloomFilter = BitVector(size = num)
        
        self.__size = num
        
        self.__bitsSet = 0
        
        self.__numHashes = numHashes
        
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        #initialize h to the first hash 
        h = BitHash(key, 0)
        
        #loop numHash times
        for i in range(self.__numHashes):
            
            #if the bit about to be set to 1 is still 0, increase bitsSet by 1
            if self.__bloomFilter[h % (self.__size)] == 0:
                self.__bitsSet += 1    
            
            #set the correct bit to 1
            self.__bloomFilter[h % (self.__size)] = 1
            
            #rehash h 
            h = BitHash(key, h)
        
        
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        #initialize h to the first hash 
        h = BitHash(key, 0)
        
        #loop numHash times
        for i in range(self.__numHashes):
            #if it encounters a 0 at any of the hash locations, return False
            #because it has definitely not been inserted
            if self.__bloomFilter[h % (self.__size)] == 0:
                return False
            #rehash h 
            h = BitHash(key, h)
            
        #if it made it here, return True
        return True
            
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):  
        
        #phi is the proportion of bits still 0, so the number of total bits minus\
        #the number of bits set gives the number of bits still 0, divided by\
        #number of total bits gives the proportion of bits still 0
        phi = (self.__size - self.__bitsSet)/self.__size
        d = self.__numHashes
        
        P = (1 - phi)**d
        return P
            
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__bitsSet


def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    #open the file
    fin= open("wordlist.txt")
    
    # read the first numKeys words from the file and insert them into the 
    #Bloom Filter
    for i in range(numKeys):
        word = fin.readline()
        b.insert(word)
    
    #close the input file   
    fin.close() 

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("Projected false positive rate: " +str(b.falsePositiveRate()))

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    fin= open("wordlist.txt")
    
    #set missing to 0
    missing = 0
    #loop through the same numKeys words as before
    for i in range(numKeys):
        word = fin.readline() 
        #if the word is not in the Bloom Filter, increase missing by 1
        if not b.find(word):
            missing += 1
        
    print("Missing " + str(missing))

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    #set found to 0
    found = 0
    #loop through the next numKey words
    for i in range(numKeys):
        word = fin.readline()
        #if the word can be found in the Bloom Filter, increase found by 1
        if b.find(word):
            found += 1    
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    #found divided by numKeys gives the percent rate of false positives
    print("Actual false positive rate: " + str(found/numKeys))

    
if __name__ == '__main__':
    __main()       

