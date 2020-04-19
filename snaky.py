import pygame

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
                self.snake_lst.insert(0,(x,y))
        else:
            self.snake_lst=[(snake_x,snake_y)]
        self.snake_sx=0
        self.snake_sy=0
        self.direction={'l':False,'r':True,'u':False,'d':False}
    def PlotSnake(self,GameDisplay):
        y,x=self.snake_lst[-1]
        pygame.draw.rect(GameDisplay,(0,100,0),(x*20,y*20,20,20))
        for x,y in self.snake_lst[:-1]:
            GameDisplay.blit(self.img,(y*20,x*20))
    def GetData(self , grid_length ,food_x ,food_y):
        surrond = [0 for x in range(8)]
        indx = 0
        head_x = self.snake_x
        head_y = self.snake_y
        tail_x = self.snake_lst[-1][0]
        tail_y = self.snake_lst[-1][1]
        diff_x=self.snake_x-tail_x
        diff_y=self.snake_x-tail_y
        for i in range(-1 , 2) :
            for j  in range(-1,2):
                if(i==0 and j==0):continue
                if(head_x +i < 0 or head_x+i >= grid_length
                   or head_y +j <0 or head_y +j >= grid_length
                   or self.Check(head_x+i , head_y+j) ==True
                    ) :
                    surrond[indx] = 1
                indx +=1
        returnList = surrond
        returnList += [head_x / grid_length , head_y / grid_length]
        returnList += [self.snake_length/(2*grid_length), diff_x/grid_length , diff_y/grid_length]
        returnList += [(head_x-food_x) /grid_length , (head_y-food_y)/grid_length]
        return returnList

    def Check(self,x,y):
        return (x,y) in self.snake_lst
    def Move(self,move,rows):
        if move=='l' and self.direction['r']==False:
            self.direction['l']=True
            self.direction['u']=False
            self.direction['d']=False
            self.snake_sx=0
            self.snake_sy=-1
        elif move=='r' and self.direction['l']==False:
            self.direction['r']=True
            self.direction['u']=False
            self.direction['d']=False
            self.snake_sx=0
            self.snake_sy=1
        elif move=='u' and self.direction['d']==False:
            self.direction['u']=True
            self.direction['l']=False
            self.direction['r']=False
            self.snake_sy= 0
            self.snake_sx=-1
        elif move=='d' and self.direction['u']==False:
            self.direction['d']=True
            self.direction['l']=False
            self.direction['r']=False
            self.snake_sy=0
            self.snake_sx=1
        self.snake_x+=self.snake_sx
        self.snake_y+=self.snake_sy
        if self.snake_x<0 or self.snake_x>rows-1 or self.snake_y<0 or self.snake_y>rows-1:
            self.is_alive=False
        else:
            if (self.snake_x,self.snake_y) in self.snake_lst[:-1]:
                self.is_alive=False
            if not (self.snake_x,self.snake_y) == self.snake_lst[-1]:
                self.snake_lst.append((self.snake_x,self.snake_y))
            if len(self.snake_lst)>self.snake_length:
                del self.snake_lst[0]