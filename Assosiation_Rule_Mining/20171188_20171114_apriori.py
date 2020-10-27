from collections import defaultdict
from itertools import chain,combinations
from time import time
import numpy as np


class Apriori():
	def __init__(self,min_support,min_confidence):
		self.min_support = min_support
		self.min_confidence = min_confidence
		self.transactionList = []
		self.itemSet = set()
		self.freqSet = defaultdict(int)
		self.realtionItems = []
		self.realtions = []
		self.ans = dict()

	def getItemSetTransList(self,data_itr):
		for rows in data_itr:
			self.transactionList.append(rows)
			for item in rows:
				self.itemSet.add(frozenset([item]))
		self.n = len(self.transactionList)

	def ItemsWithMinSupport(self,itemSet):

		Cset = set()
		temp = defaultdict(int)

		for item in itemSet:
			for transaction in self.transactionList:
				if item.issubset(transaction):
					self.freqSet[item] = self.freqSet[item]+1
					temp[item] = temp[item]+1

		for item, count in temp.items():
			support = float(count)/self.n
			if support >= self.min_support:
				Cset.add(item)

		idx = 0
		for transaction in self.transactionList:
			has_item = False
			for item in Cset:
				if item.issubset(transaction):
					has_item = True
					break

			if has_item == False:
				del self.transactionList[idx]
			idx = idx+1

		return Cset

	def joinSet(self,itemSet,k):
		temp = []
		for i in itemSet:
			for j in itemSet:
				item = i.union(j)
				if len(item) == k:
					if not self.has_frequent_subset(item,itemSet,k-1):
						temp.append(item)

		
		return set(temp)

	def has_frequent_subset(self,c,L,k):
		''' Pruning Step '''
		for items in self.find_subsets(c,k):
			if frozenset(items) not in L:
				return True
		return False

	def nonEmptySubsets(self,X):
		return list(chain.from_iterable([combinations(X,r) for r in range(1,len(X)+1)]))


	def find_subsets(self, S, m):
		return set(combinations(S, m))
		
	def run(self,data_itr):
		self.getItemSetTransList(data_itr)
		Lset = self.ItemsWithMinSupport(self.itemSet) #### 1 - frequent
		k = 2
		
		while len(Lset) != 0:
			self.ans[k-1] = Lset
			### Create new Candidates
			Cset = self.joinSet(Lset,k)
			### Remove infrequent
			Lset = self.ItemsWithMinSupport(Cset)
			print("K = "+str(k))
			k = k+1

		for _,val in self.ans.items():
			self.realtionItems.extend([tuple(item) for item in val])

		








		






def nonEmptySubsets(X):
		return list(chain.from_iterable([combinations(X,r) for r in range(1,len(X)+1)]))	




def get_ItemSets_and_Rules_from_Global(Global_L,all_transactions,min_support,min_confidence):
	Freq_ItemSets = set()
	Rules = []
	temp = defaultdict(int)

	for item in Global_L:
		for transaction in all_transactions:
			item = frozenset(item)
			if item.issubset(transaction):
				temp[item] = temp[item]+1



	for item, count in temp.items():
		support = float(count)/len(all_transactions)

		if support >= min_support:
			Freq_ItemSets.add((tuple(item),support))

	for item in Freq_ItemSets:
		obj = frozenset(item[0])
		subsets = nonEmptySubsets(obj)
		for x in subsets:
			l = frozenset(x)
			diff = obj.difference(l)
			if len(diff) > 0:
				conf = float(temp[obj])/float(temp[l])
				if conf >= min_confidence:
					Rules.append(((tuple(l),tuple(diff)),conf))
	

	return Freq_ItemSets,Rules



def fetchData(file_name):
	with open(file_name,'r') as f:
		for line in f:
			line = line.strip().rstrip('-2').replace(" ","").rstrip('-1')
			transaction = frozenset(line.split('-1'))
			yield transaction


def printResults(items, rules):
    print("\n------------------------ FREQUENT ITEMSETS:")
    for item, support in sorted(items, key=lambda x: x[1]):
        print("ITEM: "+str(item)+" ,Support: "+str(support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        print("RULE: "+str(rule[0])+" ==> "+str(rule[1])+" , Confidence: "+str(confidence))


if __name__ == "__main__":

	print("Choose Data File: ")
	file_names = ['BMS1_spmf','BMS2.txt','LEVIATHAN.txt']

	for i in range(len(file_names)):
		print(str(i)+": "+file_names[i])

	idx = int(input())
	if idx >= len(file_names) or idx < 0:
		print("please enter valid index")
		exit()
	path = file_names[idx]


	print("Enter Minimum Support Value % (0-1): ")
	min_support = float(input())

	if min_support >= len(file_names) or min_support < 0:
		print("please enter valid min_support")
		exit()

	print("Enter Minimum Confidence Value % (0-1): ")
	min_confidence = float(input())

	if min_confidence >= len(file_names) or min_confidence < 0:
		print("please enter valid min_confidence")
		exit()

	print("Enter Number of Partitions Value: ")
	num_partitions = int(input())



	transaction = fetchData('./data/'+path)
	

	apriori = [Apriori(min_support/num_partitions,min_confidence) for i in range(num_partitions)]
	transaction = list(transaction)
	
	times = []

	for i in range(num_partitions):
		start = time()
		apriori[i].run(transaction[len(transaction)*i//num_partitions:len(transaction)*(i+1)//num_partitions])
		end = time()

		times.append(end-start)


	Global_L = set()
	for idx in range(num_partitions):
		for itemSets in apriori[idx].realtionItems:
			itemSets = tuple(sorted(itemSets))
			Global_L.add(itemSets)
	
	start = time()
	
	ItemSets, Rules = get_ItemSets_and_Rules_from_Global(Global_L,transaction,min_support,min_confidence)
	
	end = time()

	printResults(ItemSets,Rules)
	print("Total Time: ")
	print((end-start)+np.max(times))