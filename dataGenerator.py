import numpy as np
import csv
import math

#now inbuilt , the penalty of going to a blockage ..
#move the snake into said position and check if it's completely blocked
#if it's blocked , add the penalty .. 
MOVES = ['l' , 'r' , 'u' , 'd']

def find_max_depth(grid , head_x , head_y, direction , snake_queue , depth_yet):
    if(len(snake_queue) ==0 ): return 0
    if depth_yet == 3 : return depth_yet
    grid_length = len(grid)
    nhead_x = head_x
    nhead_y = head_y
    if(direction == 'l'):
        nhead_y -=1
    if(direction == 'r'):
        nhead_y +=1
    if(direction == 'u'):
        nhead_x -=1
    if(direction == 'd'):
        nhead_x +=1
    if(nhead_x <0 or nhead_x >= grid_length or nhead_y <0 or nhead_y >= grid_length
                    or grid[nhead_x][nhead_y]!=0  ):
            return 0
    tail_x = snake_queue[0][0]
    tail_y = snake_queue[0][1]
    snake_queue.pop(0)
    grid[tail_x][tail_y] = 0
    grid[nhead_x][nhead_y] = 2
    grid[head_x][head_y] = 1
    depth = [0 for x in range(4)]
    maxi = 0
    for i in range(4): 
        ngrid = grid
        squeue = snake_queue
        depth[i] = 1 + find_max_depth(ngrid , nhead_x , nhead_y , MOVES[i] , squeue , depth_yet+1)    
        maxi = max(maxi ,depth[i])
    return maxi

def dist(curr , next):
      return math.pow(abs(curr[0] - next[0]),2) + math.pow(abs(curr[1] - next[1]),2)

def is_near(curr , next , head) :
    dist1 = dist(curr , head)
    dist2 = dist(next, head)
    return True if dist2 < dist1 else False

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
    snake_queue = [[head_x , head_y]]
    while len_generated < len_req :
        moves = []
        if (tail_x-1 >=0 and grid_generated[tail_x-1][tail_y]==0):
            moves.append('u')
        if (tail_x+1 < grid_width and grid_generated[tail_x+1][tail_y]==0):
            moves.append('d')
        if (tail_y-1 >=0 and grid_generated[tail_x][tail_y-1]==0):
            moves.append('l')
        if (tail_y+1 < grid_height and grid_generated[tail_x][tail_y+1]==0):
            moves.append('r')
        if(len(moves)==0) : break
        move = np.random.choice(moves)
        if(move == 'l') : tail_y-=1
        if(move == 'r') : tail_y+=1
        if(move == 'u') : tail_x-=1
        if(move == 'd') : tail_x+=1
        grid_generated[tail_x][tail_y] =1
        snake_queue.append([tail_x , tail_y])
        len_generated +=1
        len_actually_generated+=1
    #now check if any move leads to death .. 
    label_generated = [0,0,0,0] #l , r,  u, d
    # print('head= ', head_x ,' ',head_y)
    midx = grid_height/2
    midy = grid_width/2
    grid_generated[tail_x][tail_y] = 3
    depth_each = [0 for x in range(4)]
    for i in range(4) :
        ngrid = grid_generated
        squeue = snake_queue
        depth_each[i] = find_max_depth(ngrid , head_x , head_y,MOVES[i] , squeue,0)

    near_reward = 4000
    far_penalty = 2000
    depth_reward = 2000
    if(head_x -1 >=0 and grid_generated[head_x-1][head_y] == 0):
        label_generated[2] += depth_reward
        label_generated[2] += depth_each[2] *depth_reward 
        if(is_near([head_x , head_y] , [head_x-1 , head_y] , [midx , midy])):
            label_generated[2] += near_reward
        else: label_generated[2] -=far_penalty
    if(head_x + 1 < grid_width and grid_generated[head_x+1][head_y] == 0):
        label_generated[3] += depth_each[3] * depth_reward
        label_generated[3] += depth_reward
        if(is_near([head_x , head_y] , [head_x+1 , head_y] , [midx , midy])):
            label_generated[3] += near_reward
        else :label_generated[3] -= far_penalty

    if(head_y -1 >=0 and grid_generated[head_x][head_y-1] == 0):
        label_generated[0] += (depth_each[0]*depth_reward)
        label_generated[0] += depth_reward
        if(is_near([head_x , head_y] , [head_x , head_y-1] , [midx , midy])):
            label_generated[0] += near_reward
        else: label_generated[0] -= far_penalty
      
    if(head_y + 1 < grid_height and grid_generated[head_x][head_y+1] == 0):
        label_generated[1] += (depth_each[1]* depth_reward)
        label_generated[1] += depth_reward
        if(is_near([head_x , head_y] , [head_x, head_y+1] , [midx , midy])):
            label_generated[1] += near_reward
        else :label_generated[1] -= far_penalty
    #surrondValues
    surrond = [0 for x in range(8)]
    #get surronding values now
    indx = 0
    for x in range(-1,2):
        for y in range(-1,2):
            if(x ==0 and y ==0): continue
            if(head_x+x <0 or head_x+x >= grid_width or head_y+y < 0 or head_y+y >= grid_height or grid_generated[head_x+x][head_y+y]==1):
                surrond[indx] =1     
            indx+=1
    
    sum = 0
    for i in label_generated:
        sum += max(i , 0)
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
    returningList = surrond
    returningList += [head_x / (grid_width) , head_y/(grid_height)]
    returningList += [ len_actually_generated/(grid_width + grid_height),x_diff/grid_width , y_diff/grid_height]
    returningList += [label_generated[0] , label_generated[1] , label_generated[2],label_generated[3]]
    return returningList
# with open('train.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
    # writer.writerow(["leftB" ,"rightB","upB","downB","length", "head_x" , "head_y","x_diff" , "y_diff","label_l" , "label_r" , "label_u", "label_d"])
    
def prepare_data(filename , rows):
  for i in range(rows):
      data = generateAnInstance(10,10)
      with open( filename, 'a+', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(data)


prepare_data('new.csv' , 10)

# def ll(s):
#     s.pop(0)
#     s.append(100)

# ls = [1,2,3]
# print(ls)
# ll(ls)
# print(ls)
