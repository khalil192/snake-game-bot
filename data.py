import numpy as np
import csv
import math
def dist(curr , next):
      return math.pow(abs(curr[0] - next[0]),2) + math.pow(abs(curr[1] - next[1]),2)

def is_near(curr , next , head) :
    dist1 = dist(curr , head)
    dist2 = dist(next, head)
    return True if dist2 < dist1 else False


def check(ls , cell):
    return cell in ls

MOVES = ['l' , 'r', 'u' , 'd']



def calc_depth(snake_queue , depth_yet , direction , grid_len):
    #snake queue = head , body , tail
    #move head to another pos , remove tail - insert new at begining , pop tail
    if(depth_yet == 4): return 0
    head_x = snake_queue[0][0]
    head_y = snake_queue[0][1]
    nhead_x = head_x
    nhead_y = head_y
    if(direction =='l'):
        nhead_y -=1
    if(direction =='r'):
        nhead_y +=1
    if(direction == 'u'):
        nhead_x -=1
    if(direction == 'd'):
        nhead_x +=1
    #check for fail cases , if any return 0
    if(nhead_x <0 or nhead_x >= grid_len or nhead_y <0 
      or  nhead_y>=grid_len or check(snake_queue , [nhead_x , nhead_y])):
            return 0
    # print(head_x , head_y , ' dir = ', direction , 'no penalty' , nhead_x , nhead_y)
    depth_list = [0 for x in range(4)]
    snake_queue.pop(len(snake_queue)-1)
    snake_queue.insert(0,[nhead_x , nhead_y])
    maxi = 0
    for i in range(4):
        depth_list[i] = calc_depth(snake_queue[:] , 1+depth_yet , MOVES[i] , grid_len)
        maxi = max(maxi , depth_list[i])
    return 1+maxi


# snake_q = [[4,5] ,[5,5], [5,4] , [5,3] , [4,3] , [3,3] , [3,4] , [3,5]]

# print(calc_depth(snake_q[:] , 0,'l' , 10))
# print(calc_depth(snake_q[:] , 0,'r' , 10))
# print(calc_depth(snake_q[:] , 0,'u' ,10))
# print(calc_depth(snake_q[:] , 0,'d' , 10))

near_reward = 3000
far_penalty = 2000
depth_reward = 1000


def generateAnInstance(grid_width , grid_height):
    head_x = np.random.randint(grid_width)
    head_y = np.random.randint(grid_height)
    # grid_generated = [ [0 for x in range(grid_width) ] for y in range(grid_height)]
    len_req = np.random.randint((grid_height+ grid_width))
    len_generated = 0
    chk = 0
    tail_x = head_x
    tail_y = head_y
    len_actually_generated = 1
    snake_queue = [[head_x , head_y]]
    while len_generated < len_req :
        allowed_moves = []
        if (tail_x-1 >=0 and check(snake_queue,[tail_x-1 , tail_y]) == False):
            allowed_moves.append('u')
        if (tail_x+1 < grid_width and check(snake_queue,[tail_x+1 , tail_y]) == False):
            allowed_moves.append('d')
        if (tail_y-1 >=0 and check(snake_queue,[tail_x , tail_y-1]) == False):
            allowed_moves.append('l')
        if (tail_y+1 < grid_height and check(snake_queue,[tail_x , tail_y+1]) == False):
            allowed_moves.append('r')
        if(len(allowed_moves)==0) : break
        move = np.random.choice(allowed_moves)
        if(move == 'l') : tail_y-=1
        if(move == 'r') : tail_y+=1
        if(move == 'u') : tail_x-=1
        if(move == 'd') : tail_x+=1
        # grid_generated[tail_x][tail_y] =1
        snake_queue.append([tail_x , tail_y])
        len_generated +=1
        len_actually_generated+=1
    #now check if any move leads to death .. 
    label_generated = [0,0,0,0] #l , r,  u, d
    # print('head= ', head_x ,' ',head_y)
    food_x = np.random.randint(grid_width)
    food_y = np.random.randint(grid_height)
    while(check(snake_queue , [food_x , food_y])==True):
        food_x = np.random.randint(grid_width)
        food_y = np.random.randint(grid_height)
    midx = grid_width/2
    midy = grid_height/2
    if(head_x -1 >=0 and check(snake_queue , [head_x-1,head_y])==False): #up
        label_generated[2] = 2000
        label_generated [2] += (calc_depth(snake_queue[:] , 0,'u',grid_height)*depth_reward)
        if(is_near([head_x , head_y] , [head_x-1 , head_y] , [food_x , food_y])):
            label_generated[2] += near_reward
        else: label_generated[2] -= far_penalty
    if(head_x + 1 < grid_width and check(snake_queue,[head_x+1 , head_y]) == False):#down
        label_generated[3] =2000
        label_generated [3] += (calc_depth(snake_queue[:] , 0,'d',grid_height)*depth_reward)
        if(is_near([head_x , head_y] , [head_x+1 , head_y] , [food_x , food_y])):
            label_generated[3] += near_reward
        else :label_generated[3] -=far_penalty

    if(head_y -1 >=0 and check(snake_queue , [head_x , head_y-1]) == False): #Left
        label_generated[0] = 2000
        label_generated [0] += (calc_depth(snake_queue[:] , 0,'l',grid_height)*depth_reward)
        if(is_near([head_x , head_y] , [head_x , head_y-1] , [food_x , food_y])):
            label_generated[0] += near_reward
        else: label_generated[0] -=far_penalty
      
    if(head_y + 1 < grid_height and check(snake_queue , [head_x ,head_y+1]) == False):#right
        label_generated[1] = 2000
        label_generated [1] += (calc_depth(snake_queue[:] , 0,'r',grid_height)*depth_reward)
        if(is_near([head_x , head_y] , [head_x, head_y+1] , [food_x , food_y])):
            label_generated[1] += near_reward
        else :label_generated[1] -=far_penalty
    #surrondValues
    surrond = [0 for x in range(8)]
    #get surronding values now
    indx = 0
    for x in range(-1,2):
        for y in range(-1,2):
            if(x ==0 and y ==0): continue
            if(head_x+x <0 or head_x+x >= grid_width or head_y+y < 0 or head_y+y >= grid_height or 
                check(snake_queue , [head_x+x,head_y+y])==True):
                surrond[indx] =1     
            indx+=1
    sum = 0
    for i in label_generated:
        sum += i
    sum = max(sum , 1)
    for i in range(4):
        label_generated[i]/=sum
    x_diff = head_x - tail_x
    y_diff = head_y - tail_y


    returningList = surrond
    returningList += [head_x / (grid_width) , head_y/(grid_height)]
    returningList += [ len_actually_generated/(grid_width + grid_height),x_diff/grid_width , y_diff/grid_height]
    returningList += [food_x , food_y]
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