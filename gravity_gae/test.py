# def maxsquare(matrix):
#     if not matrix: return 0
#     row = len(matrix)
#     col = len(matrix[0])
#     dp = [[0] * col for _ in range(row)]
#     for i in range(row):
#         dp[i][0] = int(matrix[i][0])
#     for j in range(col):
#         dp[0][j] = int(matrix[0][j])
#     for i in range(1,row):
#         for j in range(1,col):
#             if int(matrix[i][j]) ==1:
#                 dp[i][j] = min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])+1
#     return max(map(max,dp))**2
#
# line = input().split()
# row = int(line[0])
# col = int(line[1])
# matrix =  [[0] * col for _ in range(row)]
# for i in range(row):
#     data = input()
#     temp = []
#     for cha in data:
#         if cha == 'M':
#             temp.append(1)
#         else:temp.append(0)
#     matrix[i] = temp
# print(maxsquare(matrix))


def findson(root,vist_list):
    if root in vist_list:
        return root,vist_list
    else:
        vist_list.append(root)
    if root in tree:
        for i in tree[root]:
            vist_list.append(i)
            root,vist_list = findson(i,vist_list)
    else:
        vist_list.append(root)
        return tree,root,vist_list

line = input().split()
nums = int(line[0])
matches = int(line[1])
tree = {}
back_tree = {}
for i in range(matches):
    data = list(map(int,input().split()))
    temp = tree.get(data[0],[])
    temp.append(data[1])
    tree[data[0]] = temp
root,vist_list = findson(1,[])
print(root)
print(vist_list)
    # build back tree
    # data = list(map(int,input().split()))
    # temp = tree.get(data[0],[])
    # temp.append(data[1])
    # tree[data[0]] = temp

#     temp = []
#     for cha in data:
#         if cha == 'M':
#             temp.append(1)
#         else:temp.append(0)
#     matrix[i] = temp
# print(maxsquare(matrix))