import numpy as np
import copy
import time
import operator
class Node:
  def __init__(self, ide):
    self.ide = ide
    self.parent = {}
    self.count = 0
    self.child = {}

minsup = 0.08
confidence = 0.6

file = './data/pfden.dat'

start_preprocess = time.time()

transactionList = []
itemSet = set()
with open(file,'r') as f:
  for line in f:
    row = line.strip().rstrip('-2').replace(" ","").rstrip('-1').split('-1')
    row = list(dict.fromkeys(row))
    transactionList.append(row)
    for item in row:
      itemSet.add(item)

hashmap = {}
for i in range(len(transactionList)):
	for j in range(len(transactionList[i])):
		if ( hashmap.get(transactionList[i][j]) == None ):
			hashmap[transactionList[i][j]] = 0
		hashmap[transactionList[i][j]] += 1
hashmap = sorted(hashmap.items(), key=operator.itemgetter(1), reverse = True)

itemNum_map = {}
numItem_map = {}
item_node = []

for i in range(len(hashmap)):
  itemNum_map[hashmap[i][0]] = i
  numItem_map[i] = hashmap[i][0]
  item_node.append([])

transactions = []
for i in range(len(transactionList)):
  temp = []
  for j in range(len(transactionList[i])):
    temp.append(itemNum_map[transactionList[i][j]])
  temp = sorted(temp) 
  transactions.append(copy.copy(temp))
# Closed Set for the bonus part
closed_set = []

root = Node(-1)
rules = []
for i in range(len(transactions)):
  root.count=root.count+1;
  if(root.child.get(transactions[i][0]) == None):
    root.child[transactions[i][0]] = len(item_node[transactions[i][0]])
    temp = Node(transactions[i][0])
    temp.parent[root.ide] = 0
    item_node[transactions[i][0]].append(temp)
  
  current_Node = transactions[i][0]
  Node_index = root.child[transactions[i][0]]

  for j in range(len(transactions[i])):
    item_node[current_Node][Node_index].count +=1
    if(j+1 == len(transactions[i])):
      break
    if(item_node[current_Node][Node_index].child.get(transactions[i][j+1]) == None):
      item_node[current_Node][Node_index].child[transactions[i][j+1]] = len(item_node[transactions[i][j+1]])
      temp = Node(transactions[i][j+1])
      temp.parent[current_Node] = Node_index
      item_node[transactions[i][j+1]].append(temp)
    Node_index = item_node[current_Node][Node_index].child[transactions[i][j+1]]
    current_Node = transactions[i][j+1]

end_preprocess = time.time()
print("Data Pre-processing Time - ",round(end_preprocess - start_preprocess,5)," Seconds")
print()

def growth_optimized(nodes,ide):
  frequency = []
  nodeSet = []
  for i in range(len(itemSet)):
    frequency.append(0)
    nodeSet.append([])

  frequent_sets = []
  frequent_setSupport = []

  while(len(nodes) > 0):
    x = nodes[0]
    nodes.pop(0)
    frequency[x.ide]+=x.count
    for i in x.child:
      nodeSet[x.ide].append(item_node[i][x.child[i]])
      nodes.append(item_node[i][x.child[i]])

  for i in range(len(itemSet)):
    support = frequency[i]/len(transactions)
    if(support >= minsup):
      frequent_sets.append([i])
      frequent_setSupport.append(support)
      ide.append(i)
      candidate_sets, candidate_support = growth_optimized(copy.copy(nodeSet[i]),copy.copy(ide))
      for j in range(len(candidate_sets)):
        if(candidate_support[j]/support >= confidence):
          rules.append([copy.copy(ide),copy.copy(candidate_sets[j]),candidate_support[j]/support])
        if(candidate_support[j] == support):
        	closed_set.append(sorted(copy.copy(ide)))
        candidate_sets[j].append(i)
        candidate_sets[j] = sorted(candidate_sets[j])
        frequent_sets.append(candidate_sets[j])
        frequent_setSupport.append(candidate_support[j])
      ide.pop(len(ide)-1)

  return frequent_sets, frequent_setSupport

def fpGrowth_optimized(nodes,ide):
	nodeSet = []
	frequentSets = []
	setSupport = []
	frequency = 0

	for i in range(len(nodes)):
		frequency += nodes[i].count
		for j in nodes[i].child:
			nodeSet.append(item_node[j][nodes[i].child[j]])

	support = frequency/len(transactions)
	if(support >= minsup):
		frequentSets.append(ide)
		setSupport.append(support)
		candidate_sets, candidate_support = growth_optimized(copy.copy(nodeSet),copy.copy(ide))
		for i in range(len(candidate_sets)):
			if(candidate_support[i]/support >= confidence):
				rules.append([copy.copy(ide),copy.copy(candidate_sets[i]),candidate_support[i]/support])
			if(candidate_support[i] == support):
				closed_set.append(sorted(copy.copy(ide)))
			candidate_sets[i].extend(ide)
			candidate_sets[i] = sorted(candidate_sets[i])
			frequentSets.append(candidate_sets[i])
			setSupport.append(candidate_support[i])
	return frequentSets,setSupport


def num2Item(frequent_Sets):
	SetList = []
	for i in range(len(frequent_Sets)):
		temp = []
		for j in frequent_Sets[i]:
			temp.append(numItem_map[j])
		SetList.append(temp)
	return SetList

# Optimized FP-Growth

frequent_Sets = []
frequent_Supports = []
rules = []
for i in range(len(item_node)):
  can_Sets, can_Supports = fpGrowth_optimized(item_node[i],[i])
  frequent_Sets.extend(can_Sets)
  frequent_Supports.extend(can_Supports)

SetList = num2Item(frequent_Sets)

frequent_Supports = np.array(frequent_Supports)
print("---------- OPTIMIZED FP-Growth OUTPUT ----------")
print("FREQUENT SETS ->")
print()
for i in np.argsort(frequent_Supports):
    print("Item : ",SetList[i]," Support -> ",round(frequent_Supports[i],5))

print("ASSOCIATION RULES ->")
print()
for i in range(len(rules)):
  x = []
  y = []
  for j in rules[i][0]:
    x.append(numItem_map[j])
  for j in rules[i][1]:
    y.append(numItem_map[j])
  print("Rule: ", x," ==> ", y," Confidence = ",round(rules[i][2],5))
end_basicFP = time.time()

print()
print("Optimised FP Growth Implementation Time - ",round(end_basicFP - end_preprocess,5)," Seconds")
print()
# Basic FP-Growth

def growth_basic(nodes,nodeFreq,ide):
  frequency = []
  nodeSet = []
  nodeSetfreq = []
  for i in range(len(itemSet)):
    frequency.append(0)
    nodeSet.append([])
    nodeSetfreq.append([])

  frequent_sets = []
  frequent_setSupport = []

  while(len(nodes) > 0):
    x = nodes[0]
    freq = nodeFreq[0]    
    frequency[x.ide]+=freq
    nodes.pop(0)
    nodeFreq.pop(0)
    for i in x.parent:
      if i != -1:
        nodeSet[x.ide].append(item_node[i][x.parent[i]])
        nodeSetfreq[x.ide].append(freq)
        nodes.append(item_node[i][x.parent[i]])
        nodeFreq.append(freq)

  for i in range(len(itemSet)):
    support = frequency[i]/len(transactions)
    if(support >= minsup):
      frequent_sets.append([i])
      frequent_setSupport.append(support)
      ide.append(i)
      candidate_sets, candidate_support = growth_basic(copy.copy(nodeSet[i]),copy.copy(nodeSetfreq[i]),copy.copy(ide))
      for j in range(len(candidate_sets)):
        if(candidate_support[j]/support >= confidence):
          rules.append([copy.copy(ide),copy.copy(candidate_sets[j]),candidate_support[j]/support])
        if(candidate_support[j] == support):
          closed_set.append(sorted(copy.copy(ide)))
        candidate_sets[j].append(i)
        frequent_sets.append(candidate_sets[j])
        frequent_setSupport.append(candidate_support[j])
      ide.pop(-1)

  return frequent_sets, frequent_setSupport

def fpGrowth_basic(nodes,ide):
  nodeSet = []
  nodeSetfreq = []
  frequentSets = []
  setSupport = []
  frequency = 0

  for i in range(len(nodes)):
    frequency += nodes[i].count
    for j in nodes[i].parent:
      if j != -1:
        nodeSet.append(item_node[j][nodes[i].parent[j]])
        nodeSetfreq.append(nodes[i].count)

  support = frequency/len(transactions)
  if(support >= minsup):
    frequentSets.append(ide)
    setSupport.append(support)
    candidate_sets, candidate_support = growth_basic(copy.copy(nodeSet),copy.copy(nodeSetfreq),copy.copy(ide))
    for i in range(len(candidate_sets)):
      if(candidate_support[i]/support >= confidence):
        rules.append([copy.copy(ide),copy.copy(candidate_sets[i]),candidate_support[i]/support])
      if(candidate_support[i] == support):
      	closed_set.append(copy.copy(ide))
      candidate_sets[i].extend(ide)
      candidate_sets[i] = sorted(candidate_sets[i])
      frequentSets.append(candidate_sets[i])
      setSupport.append(candidate_support[i])
  return frequentSets,setSupport

frequent_Sets = []
frequent_Supports = []
rules = []

for i in range(len(item_node)-1,-1,-1):
  can_Sets, can_Supports = fpGrowth_optimized(item_node[i],[i])
  frequent_Sets.extend(can_Sets)
  frequent_Supports.extend(can_Supports)

SetList = num2Item(frequent_Sets)

frequent_Supports = np.array(frequent_Supports)
print()
print("----------BASIC FP-Growth OUTPUT----------")
print()
print("FREQUENT SETS ->")
for i in np.argsort(frequent_Supports):
    print("Item : ",SetList[i]," Support -> ",round(frequent_Supports[i],5))

print()
print("ASSOCIATION RULES ->")
for i in range(len(rules)):
  x = []
  y = []
  for j in rules[i][0]:
    x.append(numItem_map[j])
  for j in rules[i][1]:
    y.append(numItem_map[j])
  print("Rule: ", x," ==> ", y," Confidence = ",round(rules[i][2],5))

end_optFP = time.time()

print()
print("Optimised FP Growth Implementation Time - ",round(end_basicFP - end_preprocess,5)," Seconds")
print("Basic FP Growth Implementation Time - ",round(end_optFP - end_basicFP,5)," Seconds")
print()
print()
print("BONUS PART ->")
print("Maximal Frequent ItemSet ->")
mfi = []
for i in range(len(frequent_Sets)):
	if frequent_Sets[i] not in closed_set:
		mfi.append(frequent_Sets[i])

mfi = num2Item(mfi)
for i in range(len(mfi)):
	print(mfi[i])

print()
print("Frequent Set Size - ",len(frequent_Sets)," Maximal Frequent ItemSet Size = ",len(mfi))
