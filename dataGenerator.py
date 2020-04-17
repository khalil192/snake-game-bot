import numpy as np
import csv


def generateAnInstance(grid_width , grid_height):
    head_x = np.random.randint(grid_width)
    head_y = np.random.randint(grid_height)
    grid_generated = [ [0 for x in range(grid_width) ] for y in range(grid_height)]
    len_req = np.random.randint((grid_height+ grid_width))
    len_generated = 0
    chk = 0
    tail_x = head_x
    tail_y = head_y
    grid_generated[head_x][head_y] = 2
    len_actually_generated = 1
    while len_generated < len_req :
        moves = []
        if (tail_x-1 >=0 and grid_generated[tail_x-1][tail_y]==0):
            moves.append('l')
        if (tail_x+1 < grid_width and grid_generated[tail_x+1][tail_y]==0):
            moves.append('r')
        if (tail_y-1 >=0 and grid_generated[tail_x][tail_y-1]==0):
            moves.append('u')
        if (tail_y+1 < grid_height and grid_generated[tail_x][tail_y+1]==0):
            moves.append('d')
        if(len(moves)==0) : break
        move = np.random.choice(moves)
        if(move == 'l') : tail_x-=1
        if(move == 'r') : tail_x+=1
        if(move == 'u') : tail_y-=1
        if(move == 'd') : tail_y+=1
        grid_generated[tail_x][tail_y] =1
        len_generated +=1
        len_actually_generated+=1
    #now check if any move leads to death .. 
    label_generated = [0,0,0,0] #l , r,  u, d
    # print('head= ', head_x ,' ',head_y)
    if(head_x -1 >=0 and grid_generated[head_x-1][head_y] == 0):
        label_generated[2] =1
    if(head_x + 1 < grid_width and grid_generated[head_x+1][head_y] == 0):
        label_generated[3] =1
    if(head_y -1 >=0 and grid_generated[head_x][head_y-1] == 0):
        label_generated[0] =1
    if(head_y + 1 < grid_height and grid_generated[head_x][head_y+1] == 0):
        label_generated[1] =1
    sum = 0
    for i in label_generated:
        sum += i
    sum = max(sum , 1)
    for i in range(4):
        label_generated[i]/=sum
    x_diff = head_x - tail_x
    y_diff = head_y - tail_y
    # for row in grid_generated :
    #     print(row)
    # print('label probabilty is :' , label_generated )
    directions = [1 for x in range(4)] #left , right , up,down ,are blocked or not
    if head_y-1 >=0 and grid_generated[head_x][head_y-1] == 0:
            directions[0] = 0
    if head_y+1 < grid_height and grid_generated[head_x][head_y+1] == 0:
            directions[1] = 0
    if head_x-1 >=0 and grid_generated[head_x-1][head_y] == 0:
            directions[2] = 0
    if head_x+1 < grid_width and grid_generated[head_x+1][head_y] == 0:
            directions[3] = 0
    return ( directions[0] , directions[1] , directions[2], directions[3],
                head_x / (grid_width) , head_y/(grid_height),
                len_actually_generated/(grid_width + grid_height),x_diff/grid_width , y_diff/grid_height, 
                label_generated[0] , label_generated[1] , label_generated[2],label_generated[3]
                            )
with open('train.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["leftB" ,"rightB","upB","downB","length", "x_diff" , "y_diff","label_l" , "label_r" , "label_u", "label_d"])
    
for i in range(10000):
    data = generateAnInstance(10,10)
    with open('train.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)