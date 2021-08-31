import re
import math
import json
import queue


class Query:

    def __init__(self):
        """
        reading the json files of inverted_index.tf0idf-vector,unique_words
        """
        with open(r"C:\Users\sachin\Desktop\text-search\indexed.json",'r') as index:
            self.index=index.read()
            self.index=json.loads(self.index)
        with open(r"C:\Users\sachin\Desktop\text-search\unique-words.json") as unique_words:
            self.unique_words=unique_words.read()
            self.unique_words=json.loads(self.unique_words)

        with open(r"C:\Users\sachin\Desktop\text-search\tf-idf-vector.json") as tf_idf_vector:
            self.tf_idf_vector=tf_idf_vector.read()
            self.tf_idf_vector=json.loads(self.tf_idf_vector)
        
        self.k=5
        self.filter_pattern=re.compile('[\W_]+')

    def query_preprocessing(self,string):
        """
        making everything lowercase and removing punctuation
        """
        string=self.filter_pattern.sub(' ',string)
        string=string.lower()
        return string

    def cosine_similarity(self, query_string_vector, file_vector):
        score = 0
        mod_file_vector = 0
        for i in range(len(query_string_vector)):
            score += query_string_vector[i] * file_vector[i]
            mod_file_vector += file_vector[i] * file_vector[i]
        mod_file_vector = math.sqrt(mod_file_vector)
        score = score / mod_file_vector
        return score

    def query_string_to_vector(self, query_string):
        number_of_unique_words = len(self.unique_words)
        query_vector = [0] * number_of_unique_words
        
        for word in query_string.split():
            if word not in self.unique_words.keys():
                continue
            query_vector[int(self.unique_words[word])] += 1
        mod_query_vector = 0
        for x in query_vector:
            mod_query_vector += x * x
        mod_query_vector = math.sqrt(mod_query_vector)
        if mod_query_vector > 0:
            query_vector[:] = [x / mod_query_vector for x in query_vector]
        #print(query_vector)
        return query_vector

    def rank_files(self, query_string, list_of_files):
        
        query_vector = self.query_string_to_vector(query_string)
        q = []
        cnt = 0
        for file in list_of_files:
            file_vector = self.tf_idf_vector[file]
            score = self.cosine_similarity(query_vector, file_vector)
            queue.heappush(q, (score,file))
            cnt += 1
            if cnt > self.k:
                queue.heappop(q)
                cnt -= 1
        
        result = []
        while cnt > 0:
            result.append(queue.heappop(q))
            cnt -= 1

        result = reversed(result)

        return result

    def one_word_query(self,word):
        word=self.query_preprocessing(word)
        if word in self.index.keys():
            return [i for i in self.index[word].keys()]
        else:
            return []
    
    def text_query(self,query_string):
        query_string=self.query_preprocessing(query_string)
        result=[]
        for word in query_string.split():
            result += self.one_word_query(word)
        result=list(set(result))
        result=self.rank_files(query_string,result)
        print(result)
        return result

    def phrase_query(self,query_string):
        query_string=self.query_preprocessing(query_string)
        result=[]
        list_of_files=[]

        for word in query_string.split():
            list_of_files.append(self.one_word_query(word))
        list_of_files=set(list_of_files[0]).intersection(*list_of_files)

        for file in list_of_files:
            temp=[]
            for word in query_string.split():
                temp.append(self.index[word][file][:])
            
            for i in range(len(temp)):
                for ind in range(len(temp[i])):
                    temp[i][ind]=temp[i][ind]-i
                
            if set(temp[0]).intersection(*temp):
                result.append(file)
            result=(list)(set(result))

        return result