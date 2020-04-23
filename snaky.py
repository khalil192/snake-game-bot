import pygame

def check(ls , cell):
    return (cell in ls or (cell[0] , cell[1]) in ls)

MOVES = ['l' , 'r', 'u' , 'd']
def center_mass(snake_queue):
    sum_x = 0
    sum_y = 0
    for pair in snake_queue:
        sum_x += pair[0]
        sum_y += pair[1]
    return [sum_x/len(snake_queue) , sum_y / len(snake_queue)]


top_left  = -3
top_right = 4
total = ((top_right - top_left)**2) -1

class Snake:
    def __init__(self,path,snake_length,snake_x,snake_y):
        self.img=pygame.image.load(path)
        self.snake_length=snake_length
        self.snake_x=snake_x
        self.snake_y=snake_y
        self.is_alive=True
        if self.snake_length>1:
            self.snake_lst=[]
            for i in range(self.snake_length):
                x=snake_x
                y=snake_y-i
                self.snake_lst.insert(0,[x,y])
        else:
            self.snake_lst=[[snake_x,snake_y]]
        self.snake_sx=0
        self.snake_sy=0
        self.direction={'l':False,'r':False,'u':False,'d':False}
    def PlotSnake(self,GameDisplay):
        y,x=self.snake_lst[-1]
        pygame.draw.rect(GameDisplay,(0,100,0),(x*20,y*20,20,20))
        for x,y in self.snake_lst[:-1]:
            GameDisplay.blit(self.img,(y*20,x*20))

    def GetData(self , grid_length ,food_x ,food_y):
        surrond = [0 for x in range(total)]
        indx = 0
        head_x = self.snake_x
        head_y = self.snake_y
        tail_x = self.snake_lst[-1][0]
        tail_y = self.snake_lst[-1][1]
        diff_x=self.snake_x-tail_x
        diff_y=self.snake_x-tail_y
        for i in range(top_left, top_right) :
            for j  in range(top_left,top_right):
                if(i==0 and j==0):continue
                if(head_x +i < 0 or head_x+i >= grid_length
                   or head_y +j <0 or head_y +j >= grid_length
                   or self.Check(head_x+i , head_y+j) ==True
                    ) :
                    surrond[indx] = 1
                    # print('for ', head_x +i , head_y + j , ' block')
                indx +=1
        # print(self.snake_lst)
        grid_width = grid_length
        returningList = surrond
        
        returningList += [head_x/grid_width , head_y/grid_width]
        returningList += [self.snake_length /(2* grid_width), tail_x/ grid_width , tail_y / grid_width]
        returningList += [ (head_x - food_x )/grid_width , (head_y - food_y) / grid_width ]

        return returningList

    def Check(self,x,y):
        return ([x,y] in self.snake_lst or (x,y) in self.snake_lst)
    def Move(self,move,rows):
        sx = 0
        sy = 0
        if move=='l':
            sy = -1
        elif move=='r':
            sy += 1
        elif move=='u':
            sx = -1
        elif move=='d':
            sx = 1
        self.snake_x+= sx
        self.snake_y+= sy
        if self.snake_x<0 or self.snake_x>=rows or self.snake_y<0 or self.snake_y>=rows:
            self.is_alive=False
        else:
            if [self.snake_x,self.snake_y] in self.snake_lst[:-1]:
                self.is_alive=False
            elif not [self.snake_x,self.snake_y] == self.snake_lst[-1]:
                self.snake_lst.append([self.snake_x,self.snake_y])
            if len(self.snake_lst)>self.snake_length:
                del self.snake_lst[0]