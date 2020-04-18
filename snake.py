import pygame

class Snake:
    def __init__(self,path,snake_length,snake_x,snake_y):
        self.img=pygame.image.load(path)
        self.snake_length=snake_length
        self.snake_x=snake_x
        self.snake_y=snake_y
        if self.snake_length>1:
            self.snake_lst=[]
            for i in range(self.snake_length):
                x=self.snake_x-i
                y=self.snake_y
                self.snake_lst.insert(0,(x,y))
        else:
            self.snake_lst=[[self.snake_x,self.snake_y]]
        self.snake_sx=0
        self.snkae_sy=0
        self.direction={'l':False,'r':False,'u':False,'d':False}
    def PlotSnake(self,GameDisplay):
        for x,y in self.snake_lst:
            GameDisplay.blit(self.img,(x*20,y*20))
    def GetData(self):
        print(self.snake_lst)
        diff_x=self.snake_x-self.snake_lst[0][0]
        diff_y=self.snake_y-self.snake_lst[0][1]
        return self.snake_x,self.snake_y,diff_x,diff_y
    
    def Check(self,x,y):
        return [x,y] in self.snake_lst

if __name__=='__main__':
    snake=Snake(r'snakeBody.png',3,3,0)
    print(snake.GetData())
