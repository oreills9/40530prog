import random

n = 1000 
file = open('nas_SOR_large.in', 'w')
file.write(str(n) + '\n')
b = ''
for i in range(1, n+1):
    row = ''
    for j in range(1, n+1):
        if i == j and j == n:
            row  = row + str(i)        
        elif i == j:
            row  = row + str(i) + ', '
        elif j == n:
            row = row + '0'
        else:
            row = row + '0, '
    file.write(row + '\n')
 
    if i == n:
        b = b + str(random.randint(1, 20))
    else:
        b = b + str(random.randint(1, 20)) + ', '

file.write(b)
file.close()