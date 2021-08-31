import re
import os 
import json
import math

class Indexer():
    #indexer class
    debug=False

    def process_files(self,directory_path):
        """
        coverts all files into word vectors
        for now works only on .txt files
        """
        path_to_stopwords=r"C:\Users\sachin\Desktop\text-search\stopwords.txt"
        stopwords=open(path_to_stopwords,'r').read().lower()
        stopwords=stopwords.split()

        file_to_words={}
        for file in os.listdir(directory_path):
            if self.debug:
                #to print the files in the directory
                # hekps in debugging
                print(file)
            pattern=re.compile('[\W_]+')
            file_path=os.path.join(directory_path,file)
            words_in_file=open(file_path,'r',encoding="utf8").read().lower()
            words_in_file=pattern.sub(' ',words_in_file)
            re.sub(r'[\W_]+', '', words_in_file)
            words_in_file = words_in_file.split()
            #removing all the stopwords
            file_to_words[file]=[i for i in words_in_file if i not in stopwords]
        #print(file_to_words['myData.txt'])
        return file_to_words


    def index_one_file(self,word_list):
        """
        this function returns the mapping of words to their positions
        in the document
        input is all the words in a file in list
        output is {word1:[pos1,pos2,...],word2:[pos4,...]}
        """
        file_index = {}
        
        for position in range(0,len(word_list)):
            word = word_list[position]
            if word in file_index.keys():
                file_index[word].append(position)
            else:
                file_index[word] = [position]
        return file_index


    def index_all_files(self,word_lists):
        """
        this function returns the mapping of words to their positions 
        for all the documents combined
        input is list of words for the respective documents { document1:[word1,word2....],...}
        output is {document1:{word:[pos1,pos5,...]},....}
        """
        index_all = {}
        for file in word_lists.keys():
            index_all[file] = self.index_one_file(word_lists[file])

        return index_all


    def invert_index(self,index):
        """
        this function changes the output of above function 
        with word matching to document name and their positions in the document
        """
        invert_index={}
        for file in index.keys():
            for word in index[file].keys():
                if word in invert_index.keys():
                    invert_index[word][file]=index[file][word]
                else:
                    invert_index[word]={file: index[file][word]}
        
        return invert_index


    def build_index(self,text_corpus):
        word_list=self.process_files(text_corpus)
        index=self.index_all_files(word_list)
        inverted_index=self.invert_index(index)
        with open(r"C:\Users\sachin\Desktop\text-search\indexed.json", 'w') as indexed:
            json.dump(inverted_index,indexed,indent=4)

        self.tf_idf(inverted_index)


    def tf_idf(self,inverted_index):
        number_of_unique_words = len(inverted_index)
        unique_words = {}

        tf_vector = {}
        idf_vector = [0] * number_of_unique_words
        word_vector = []
        cnt = 0
        for word in inverted_index.keys():
            unique_words[word] = cnt
            word_vector.append(word)
            for file in inverted_index[word].keys():
                if file not in tf_vector.keys():
                    tf_vector[file] = [0] * number_of_unique_words
                tf_vector[file][cnt] += len(inverted_index[word][file])
                if tf_vector[file][cnt] > 0:
                    idf_vector[cnt] += 1
            cnt += 1

        number_of_files = len(tf_vector)
        for i in range(len(idf_vector)):
            idf_vector[i] = math.log(number_of_files / idf_vector[i])

        tf_idf_vector = {}

        for file in tf_vector.keys():
            tf_idf_vector[file] = [x * y for x, y in zip (tf_vector[file], idf_vector)]

        # TODO: dump this tf_idf_vector into a .json file
        with open(r"C:\Users\sachin\Desktop\text-search\tf-idf-vector.json", 'w') as tf_idf_json:
            json.dump(tf_idf_vector, tf_idf_json, indent=4)
        # TODO: dump unique_words vector into a .json file
        with open(r"C:\Users\sachin\Desktop\text-search\unique-words.json", 'w') as unique_words_json:
            json.dump(unique_words, unique_words_json, indent=4)
        
        if self.debug:
            print(word_vector)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(tf_vector)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(idf_vector)