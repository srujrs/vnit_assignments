import os
import json
from nltk.corpus import words
import string
import matplotlib.pyplot as plt
import time



def binary_search(posting_list,low,high,current):
	while high-low > 1:

		mid = (low + high)//2
		if posting_list[mid] <= current:

			low = mid

		else:
			high = mid

	return high

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

def nextPhraseForDocument(terms,document,position,function_of_next):
	u = position
	global funcdict
	v = funcdict[function_of_next](terms[0],document,u)
	u = v
	n = len(terms)
	

	print('Searching in the document :',document)
	for i in range(1,n):
		
		prev = v
		v = funcdict[function_of_next](terms[i],document,v)
		print('Term :{} ,Previus Location :{} , Next Location :{}'.format(terms[i],prev,v))
		
	#print('v - u  : {},n-1 :{}'.format(str(v-u),n-1))
	if v == 'INF':
		return ['INF','INF'],'not_found'
	if v - u == n -1 :
		return [u,v],'found'
	elif v-n > u:
		return nextPhraseForDocument(terms,document,v-n,function_of_next)
	else:
		return ['INF','INF'],'not_found'
		
		



def nextPhraseAcrossCorpus(phrase,position,function_of_next):
	phrase = phrase.translate(phrase.maketrans('', '', string.punctuation))
	terms = phrase.strip().split(' ')

	search_terms = list()
	common_documents = list()
	occurences = dict()
	term_0 = terms[0].lower()
	if term_0 in inverted_index_data_store:
		search_terms.append(term_0)
		common_documents = inverted_index_data_store[term_0].keys()
		print('{} : {}'.format(term_0,inverted_index_data_store[term_0].keys()))
		

	for term in terms[1:]:
		if term in inverted_index_data_store:
			term = term.lower()
			print('{} : {}'.format(term,inverted_index_data_store[term].keys()))
			common_documents = intersection(common_documents,inverted_index_data_store[term].keys())
			search_terms.append(term)

	common_documents = sorted(common_documents)
	print(common_documents)

	for document in common_documents:
		location,status = nextPhraseForDocument(search_terms,document,position,function_of_next)
		print(location)
		if status =='found':
			occurences[document] = location
			

	return occurences

def next_linear_search(term,docID,current_position):
	print('Using Cached Offset Next Method')
	posting_list = inverted_index_data_store[term][docID]
	length_of_posting_list = len(posting_list)
	global CT

	if length_of_posting_list == 0 or str(current_position) == 'INF' or posting_list[length_of_posting_list-1] < current_position:
		return 'INF'
	elif posting_list[0] > current_position:
		CT = 0
		return posting_list[0]

	if CT>= length_of_posting_list or (CT > 0  and posting_list[CT-1] >= current_position):
		CT = 0
	while CT< length_of_posting_list and posting_list[CT] <= current_position:
		CT = CT + 1

	if CT>= length_of_posting_list:
		return 'INF'
	else:
		return posting_list[CT]

def next_galloping_search(term,docID,current_position):
	print('Using Galloping Search Next Method')
	global CT
	posting_list = inverted_index_data_store[term][docID]
	length_of_posting_list = len(posting_list)
	''

	if length_of_posting_list == 0 or str(current_position) == 'INF'  or posting_list[-1] < current_position:
		return 'INF'
	elif posting_list[0] > current_position:
		CT = 0
		return posting_list[0]
	if CT>0 and posting_list[CT-1] <= current_position:
		low = CT -1
	else:
		low = 0
	jump = 1 
	high = low + jump 

	while high < length_of_posting_list and posting_list[high] < current_position:
		low = high 
		jump = jump*2
		high = low + jump
	if high >= length_of_posting_list:
		high = length_of_posting_list-1

	return posting_list[binary_search(posting_list,low,high,current_position)]


def next_binary_search(term,docID,current_position):
	print('Using Ordinary Next Method')
	posting_list = inverted_index_data_store[term][docID]
	length_of_posting_list = len(posting_list)
	#print(posting_list)
	if length_of_posting_list == 0 or str(current_position) == 'INF'  or posting_list[length_of_posting_list-1] < current_position:
		return 'INF'
	elif posting_list[0] > current_position:
		return posting_list[0]
	else:
		return posting_list[binary_search(posting_list,0,length_of_posting_list-1,current_position)]

def findOccurenceOfPhrase(queries , function_of_next):

	start_time = time.time()
	search_results = dict()
	for query in queries:
		answers = nextPhraseAcrossCorpus(query ,0,function_of_next)
		search_results[query] = answers

	end_time = time.time()

	dirname = os.getcwd()
	filepath = os.path.join(dirname,'search_results')
	with open(filepath,'w') as f:
		f.write(json.dumps(search_results,indent = 4))

	dirname = os.getcwd()
	filepath = os.path.join(dirname,'time_results')
	with open(filepath,'a') as f:
		f.write(json.dumps({function_of_next:end_time - start_time},indent = 4))


	return end_time - start_time



if __name__ == '__main__':
	global CT
	CT = 0 
	global funcdict
	funcdict ={
		'next_binary_search': next_binary_search,
		'next_galloping_search': next_galloping_search,
		'next_linear_search':next_linear_search
	}
	global inverted_index_data_store
	inverted_index_data_store = dict()
	
	# os.chdir('100KB Corpus')

	os.chdir('256MB Corpus')

	dirname = os.getcwd()
	dirname = os.path.join(dirname,'Docs')
	for filename in os.listdir(dirname):
		filepath = os.path.join(dirname,filename)
		print(filename)
		with open(filepath,'r') as f:
			lines = f.readlines()
			position = 0
			docID = filename
			for line in lines:
				line = line.translate(line.maketrans('', '', string.punctuation))
				for word in line.strip().split(' '):
					position = position + 1
					word = word.lower()
					# if word in DICTIONARY_NLTK:
					if word not in inverted_index_data_store:
						docPositions = dict()
						docPositions[docID] = [position]
						inverted_index_data_store[word] = docPositions
					elif docID not in inverted_index_data_store[word]:
						inverted_index_data_store[word][docID] = [position]
					else:
						inverted_index_data_store[word][docID].append(position)

	dirname = os.getcwd()
	filepath = os.path.join(dirname,'inverted_index_data_store')
	with open(filepath,'w') as f:
		f.write(json.dumps(inverted_index_data_store,indent = 4))

	filepath = os.path.join(dirname,'inverted_index_data_store')
	with open(filepath,'r') as f:
		inverted_index_data_store = json.load(f)

	timeListGallopingSearch = []
	timeListLinearSearch = []
	timeListBinarySearch = []
	queries_length = []
	for i in range(3,6):
		filepath = os.path.join(dirname,'Queries','queries'+str(i))
		with open(filepath,'r', encoding="utf8") as f:
			print(i)
			queries = f.readlines()

		queries_length.append(i)
		time_taken  = findOccurenceOfPhrase(queries,'next_galloping_search')
		timeListGallopingSearch.append(time_taken)
		print(time_taken)

		time_taken  = findOccurenceOfPhrase(queries,'next_linear_search')
		timeListLinearSearch.append(time_taken)
		print(time_taken)

		time_taken  = findOccurenceOfPhrase(queries,'next_binary_search')
		timeListBinarySearch.append(time_taken)
		print(time_taken)

	plt.title('Response Time VS Length of Queries')
	plt.plot(queries_length,timeListGallopingSearch,color='red')
	plt.plot(queries_length ,timeListLinearSearch,color = 'orange')
	plt.plot(queries_length ,timeListBinarySearch,color='green')
	
	plt.show()




	max_len_post_list = list()
	response_time_linear = list()
	response_time_binary = list()
	response_time_galloping = list()
	queries = ['Party Boy','so cool']
	for query_2 in queries:
	    query = query_2.split(' ')
	    query[0] = query[0].lower()
	    query[1] = query[1].lower()
	    longest_posting_list1 = max([ len(document) for document in inverted_index_data_store[query[0]].values()])
	    longest_posting_list2 = max([ len(document) for document in inverted_index_data_store[query[1]].values()])

	    longest_posting_list = max(longest_posting_list2,longest_posting_list1)
	    max_len_post_list.append(longest_posting_list)

	    st_time = time.time()
	    result = nextPhraseAcrossCorpus(query_2,0,'next_linear_search')
	    e_time = time.time()
	    response_time_linear.append(e_time-st_time)
	    #print(e_time-st_time)

	    st_time = time.time()
	    result = nextPhraseAcrossCorpus(query_2,0, 'next_binary_search')
	    e_time = time.time()
	    response_time_binary.append(e_time-st_time)
	    #print(e_time-st_time)

	    st_time = time.time()
	    result = nextPhraseAcrossCorpus(query_2,0, 'next_galloping_search')
	    e_time = time.time()
	    response_time_galloping.append(e_time-st_time)
	    #print(e_time-st_time)

	print("Length of Posting List: ",max_len_post_list)
	print("Response Time Linear: ",response_time_linear)
	print("Response Time Binary: ",response_time_binary)
	print("Response Time Galloping: ",response_time_galloping)
	plt.title("Phrase Length of 2: Length of Posting list vs Response Time")
	plt.plot(max_len_post_list,response_time_linear,color='blue')
	plt.plot(max_len_post_list,response_time_binary,color='green')
	plt.plot(max_len_post_list,response_time_galloping,color='red')
	plt.show()




	# dirname = os.getcwd()
	# filepath = os.path.join(dirname,'Queries','input_queries')
	# with open(filepath,'r') as f:
	# 	queries = f.readlines()

	# graph_time_vs_search = dict()

	# function_of_next,time_taken  = findOccurenceOfPhrase(queries,'next_galloping_search')
	# graph_time_vs_search[function_of_next] = time_taken
	# print(time_taken)

	# function_of_next,time_taken  = findOccurenceOfPhrase(queries,'next')
	# graph_time_vs_search[function_of_next] = time_taken
	# print(time_taken)

	# function_of_next,time_taken  = findOccurenceOfPhrase(queries,'next_using_cached_offset')
	# graph_time_vs_search[function_of_next] = time_taken
	# print(time_taken)

	# print(next('children','1',2106))
	# print(next_using_cached_offset('children','1',2166))
	# print(next_galloping_search('children','1',941))

	

	# start_time = time.time()
	# answers = nextPhraseAcrossCorpus('Things I do for love' ,0,'')
	# end_time = time.time()

	# graph_time_vs_search['next_galloping_search'] = end_time - start_time
	# print(end_time - start_time)


	# start_time = time.time()
	# answers = nextPhraseAcrossCorpus('Things I do for love' ,0,'next_using_cached_offset')
	# end_time = time.time()

	# graph_time_vs_search['next_using_cached_offset'] = end_time - start_time
	# print(end_time - start_time)


	# start_time = time.time()
	# answers = nextPhraseAcrossCorpus('Things I do for love' ,0,'next')
	# end_time = time.time()

	# graph_time_vs_search['next'] = end_time - start_time
	# print(end_time - start_time)

	# plt.title('Performance Comparison Graph')
	# plt.bar(range(len(graph_time_vs_search)), list(graph_time_vs_search.values()), align='center')
	# plt.xticks(range(len(graph_time_vs_search)), list(graph_time_vs_search.keys()))
	# plt.show()
