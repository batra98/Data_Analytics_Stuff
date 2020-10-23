import numpy as np
class Node:
  def __init__(self, id, parent, parentIndex):
    self.id = id
    self.parent = parent
    self.parentIndex = parentIndex
    self.count = 0
    self.child = {}

minsup = 0.005
confidence = 0.6
file = './data/BMS1_spmf'

def growth(nodes,id):
  if(len(nodes)==0):
    return [],[]

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
    frequency[x.id]+=x.count
    for i in x.child:
      nodeSet[x.id].append(item_node[i][x.child[i]])
      nodes.append(item_node[i][x.child[i]])

  for i in range(len(itemSet)):
    support = frequency[i]/len(transactions)
    if(support >= minsup):
      frequent_sets.append([i])
      frequent_setSupport.append(support)
      id.append(i)
      candidate_sets, candidate_support = growth(nodeSet[i],id)
      for j in range(len(candidate_sets)):
        if(candidate_support[j]/support >= confidence):
          rules.append([id,candidate_sets[j],candidate_support[j]/support])
        candidate_sets[j].append(i)
        frequent_sets.append(candidate_sets[j])
        frequent_setSupport.append(candidate_support[j])
      id.pop(len(id)-1)

  return frequent_sets, frequent_setSupport

def fpGrowth(nodes,id):
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
    frequentSets.append(id)
    setSupport.append(support)
    candidate_sets, candidate_support = growth(nodeSet,id)
    for i in range(len(candidate_sets)):
      if(candidate_support[i]/support >= confidence):
          rules.append([id,candidate_sets[i],candidate_support[i]/support])
      candidate_sets[i].extend(id)
      candidate_sets[i] = sorted(candidate_sets[i])
      frequentSets.append(candidate_sets[i])
      setSupport.append(candidate_support[i])
  return frequentSets,setSupport

rules = []
transactionList = []
itemSet = set()
with open(file,'r') as f:
  for line in f:
    row = line.strip().rstrip('-2').replace(" ","").rstrip('-1').split('-1')
    row.sort()
    transactionList.append(row)
    for item in row:
      itemSet.add(item)
itemSet = sorted(itemSet)

itemNum_map = {}
numItem_map = {}
item_node = []

for i in range(len(itemSet)):
  itemNum_map[itemSet[i]] = i
  numItem_map[i] = itemSet[i]
  item_node.append([])

transactions = []
for i in range(len(transactionList)):
  temp = []
  for j in range(len(transactionList[i])):
    temp.append(itemNum_map[transactionList[i][j]])
  transactions.append(temp)

root = Node(-1,-2,-2)
for i in range(len(transactions)):
  root.count=root.count+1;
  if(root.child.get(transactions[i][0]) == None):
    root.child[transactions[i][0]] = len(item_node[transactions[i][0]])
    temp = Node(transactions[i][0],-1,-1)
    item_node[transactions[i][0]].append(temp)
  
  current_Node = transactions[i][0]
  Node_index = root.child[transactions[i][0]]

  for j in range(len(transactions[i])):
    item_node[current_Node][Node_index].count +=1
    if(j+1 == len(transactions[i])):
      break
    if(item_node[current_Node][Node_index].child.get(transactions[i][j+1]) == None):
      item_node[current_Node][Node_index].child[transactions[i][j+1]] = len(item_node[transactions[i][j+1]])
      temp = Node(transactions[i][j+1],current_Node,Node_index)
      item_node[transactions[i][j+1]].append(temp)
    Node_index = item_node[current_Node][Node_index].child[transactions[i][j+1]]
    current_Node = transactions[i][j+1]


frequent_Sets = []
frequent_Supports = []
for i in range(len(item_node)):
  can_Sets, can_Supports = fpGrowth(item_node[i],[i])
  frequent_Sets.extend(can_Sets)
  frequent_Supports.extend(can_Supports)

SetList = []
for i in range(len(frequent_Sets)):
  temp = []
  for j in frequent_Sets[i]:
    temp.append(numItem_map[j])
  SetList.append(temp)

frequent_Supports = np.array(frequent_Supports)
print("\n------------------------ FREQUENT SETS:")
for i in np.argsort(frequent_Supports):
    print("Item : ",SetList[i]," -> ",frequent_Supports[i])

print("\n------------------------ RULES:")
for i in range(len(rules)):
    print("Rule: ", rules[i][0]," ==> ", rules[i][1]," Confidence = ",rules[i][2])
