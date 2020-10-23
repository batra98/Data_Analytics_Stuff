from collections import defaultdict
from itertools import chain,combinations


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
		# print("Cset")
		# print(Cset)

		### Transaction Reduction
		# print("Transactions")
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
			print(k)
			k = k+1

		for _,val in self.ans.items():
			self.realtionItems.extend([(tuple(item),float(self.freqSet[item])/self.n) for item in val])

		for k,val in self.ans.items():
			if k == 1:
				continue
			for item in val:
				subsets = self.nonEmptySubsets(item)
				for x in subsets:
					x = frozenset(x)
					diff = item.difference(x)

					if len(diff) > 0:
						conf = float(self.freqSet[item])/float(self.freqSet[x])
						if conf >= self.min_confidence:
							self.realtions.append(((tuple(x),tuple(diff)),conf))

		# print(self.realtions)








		






		







def fetchData(file_name):
	with open(file_name,'r') as f:
		for line in f:
			line = line.strip().rstrip('-2').replace(" ","").rstrip('-1')
			transaction = frozenset(line.split('-1'))
			yield transaction


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


if __name__ == "__main__":
	# transaction = fetchData('./data/test.txt')
	transaction = fetchData('./data/BMS1_spmf')
	apriori = Apriori(0.005,0.6)
	apriori.run(transaction)
	printResults(apriori.realtionItems,apriori.realtions)