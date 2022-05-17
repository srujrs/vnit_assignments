import os
import random

if __name__=='__main__':
	no_of_queries_per_document = 6

	queries = []

	dirname = os.getcwd()
	dirname = os.path.join(dirname,'100KB Corpus/Docs')
	for filename in os.listdir(dirname):
		filepath = os.path.join(dirname,filename)
		print(filename)
		with open(filepath,'r') as f:
			lines = f.readlines()
			modulo = len(lines)/6
			for index,line in enumerate(lines):
				if index%modulo == 0:
					words = line.strip().split(' ')
					#print(words)
					query_length = random.randint(5,10)
					r1 = random.randint(0, 6)
					queries.append(words[r1:r1+query_length])

	dirname = os.getcwd()
	filepath = os.path.join(dirname,'queries')
	with open(filepath,'w') as f:
		for words in queries:
			query = ''.join([i + " " for i in words])
			print(query)
			f.write(query+'\n')
