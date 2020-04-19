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
                x=self.snake_x-i
                y=self.snake_y
                self.snake_lst.insert(0,(x,y))
        else:
            self.snake_lst=[(self.snake_x,self.snake_y)]
        self.snake_sx=0
        self.snake_sy=0
        self.direction={'l':False,'r':True,'u':False,'d':False}
    def PlotSnake(self,GameDisplay):
        for x,y in self.snake_lst:
            GameDisplay.blit(self.img,(x*20,y*20))
    def GetData(self , grid_length):
        print(self.snake_lst)
        surrond =[]
        head_x = self.snake_y
        head_y = self.snake_x
        indx = 0
        print('head ', head_x , head_y)
        print(self.snake_lst)
        for x in range(-1,2):
            for y in range(-1,2):
                if(x==0 and y ==0 ) : continue
                if(head_x + x < 0 or head_y + y < 0  or head_x + x >= grid_length 
                    or head_y + y >= grid_length or self.Check(head_x+x , head_y+y) == True):
                        print(head_x +x , head_y+y  , 'is blocked')
                        surrond.append(1)
                else : 
                    print('not blocked = ' , head_x +x , head_y+y)
                    surrond.append(0)
                print('surrond is ',surrond)
        diff_y=self.snake_x-self.snake_lst[0][0]
        diff_x=self.snake_y-self.snake_lst[0][1]    
        returnList = []
        returnList += surrond
        returnList += [head_x / (grid_length) , head_y/(grid_length)]
        returnList += [self.snake_length / (2*grid_length) ,diff_x / grid_length , diff_y/grid_length]
        return returnList

    def Check(self,x,y):
        return (y,x) in self.snake_lst

    def Move(self,move,rows):
        if move=='l' and self.direction['r']==False:
            self.direction['l']=True
            self.direction['u']=False
            self.direction['d']=False
            self.snake_sx=-1
            self.snake_sy=0
        elif move=='r' and self.direction['l']==False:
            self.direction['r']=True
            self.direction['u']=False
            self.direction['d']=False
            self.snake_sx=1
            self.snake_sy=0
        elif move=='u' and self.direction['d']==False:
            self.direction['u']=True
            self.direction['l']=False
            self.direction['r']=False
            self.snake_sy= -1
            self.snake_sx=0
        elif move=='d' and self.direction['u']==False:
            self.direction['d']=True
            self.direction['l']=False
            self.direction['r']=False
            self.snake_sy=1
            self.snake_sx=0
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
        


if __name__=='__main__':
    snake=Snake(r'snakeBody.png',3,3,0)

    print(snake.GetData())
