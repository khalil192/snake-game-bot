import pygame
import random
import pandas as pd
import numpy
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

pygame.init()
GridSize=(10,10)
GameWidth=GridSize[0]*20
Gameheight=GridSize[1]*20
class Snake:
    def __init__(self , length_required):
        self.snake=pygame.image.load(r'snakeBody.PNG')
        self.snake_lst=[]
        for i in range(length_required):
            self.snake_lst.append([i*20 , 20])
        self.snake_length=length_required
        self.snake_x= (length_required-1)*20
        self.snake_y=20
        self.snake_sx=0
        self.snake_sy=0
        self.past_cell =[self.snake_x , self.snake_y]
        self.direction=dict.fromkeys(['u','d','l','r'],False)
        # self.direction['l'] = True
    def polt_snake(self,GameDisplay):
        for val in self.snake_lst:
            GameDisplay.blit(self.snake,val)
    def Check(self,x,y):
        '''Takes x,y and checks if [x,y] is in snake_lst
           If present `True` is returned else `False`'''
        if [x,y] in self.snake_lst:
            return True
        else:
            return False
    def GetData(self):
        print(self.snake_lst)
        blockage = [0 for x in range(4)]
        if(self.snake_x ==0 or self.Check(self.snake_x-20 , self.snake_y) == True):
            blockage[0] = 1
        if(self.snake_x == 180 or self.Check(self.snake_x+20 , self.snake_y) == True):
            blockage[1] = 1
        if(self.snake_y ==0 or self.Check(self.snake_x , self.snake_y-20) == True):
            blockage[2] = 1
        if(self.snake_y == 180 or self.Check(self.snake_x , self.snake_y+20) == True):
            blockage[3] = 1
        diff_x=self.snake_x-self.snake_lst[0][0]
        diff_y=self.snake_y-self.snake_lst[0][1]
        return [blockage[0] ,blockage[1],blockage[2],blockage[3],
                self.snake_x/200 , self.snake_y/200, 
                self.snake_length /(400) ,diff_x/400 , diff_y/400]
        # return [
        #     blockage[0] , blockage[1], blockage[2], blockage[3],
        #     self.snake_x,self.snake_y,diff_x,diff_y,self.snake_length]
class Food:
    def __init__(self,GameWidth,Gameheight):
        self.Boundaries=(GameWidth,Gameheight)
        self.food=pygame.image.load(r'food2.PNG')
        self.food_x=(random.randint(20,self.Boundaries[0])//20)*20
        self.food_y=(random.randint(20,self.Boundaries[1])//20)*20
    def PlotFood(self,snake,GameDisplay):
        while True:
                self.food_x=(random.randint(0,self.Boundaries[0])//20)*20
                self.food_y=(random.randint(0,self.Boundaries[0])//20)*20
                if [self.food_x,self.food_y] in snake.snake_lst:
                    self.food_x=(random.randint(0,self.Boundaries[0])//20)*20
                    self.food_y=(random.randint(0,self.Boundaries[0])//20)*20
                else:
                    break

def drawLines(surface):
    x,y=(0,0)
    for _ in range(25):
        x+=20
        y+=20
        pygame.draw.line(surface,(50,205,50),(x,0),(x,GameWidth))
        pygame.draw.line(surface,(50,205,50),(0,y),(Gameheight,y))


BackGround=pygame.image.load(r'SnakeBG.PNG')
GameDets=pygame.font.SysFont('monospace',6)
clock=pygame.time.Clock()
GameDisplay=pygame.display.set_mode((GameWidth,Gameheight))

def getRandomMove(predictedMoves):
    moves = ['l', 'r', 'u', 'd']
    max1 = 0 
    max2 = 0
    predictedMoves = predictedMoves.tolist()[0]
    print('pred is',predictedMoves)
    for i in range(4):
        if (predictedMoves[i] > predictedMoves[max1]):
            max2= max1
            max1 = i
        elif (predictedMoves[i] > predictedMoves[max2]):
            max2 = i
    if(predictedMoves[max1] - predictedMoves[max2] > 0.3):
        max2 = max1
    allowedMoves = [moves[max1], moves[max2]]
    return random.choice(allowedMoves)

def label(data,title,font,x,y,gameDisplay):
    _label=font.render(f'{title} {data}',5,(0,0,0))
    gameDisplay.blit(_label,(x,y))
    return y
def data_label(gameDisplay,dt,gameTime,score,font):
    y_pos=10
    gap=10
    x_pos=10
    y_pos=label(round(1000/dt,2),'FPS',font,x_pos,y_pos+gap,gameDisplay)
    y_pos=label(round(gameTime/1000,2),'Game Time',font,x_pos,y_pos+gap,gameDisplay)
    y_pos=label(score,'Score:',font,x_pos,y_pos+gap,GameDisplay)

def GameLoop(length_required):
    GameExit=True
    snake=Snake(length_required)
    food=Food(GameWidth,Gameheight)
    fps=10
    score=0
    game_time=0
    collision=False
    moves=['r','r','d','l','u'][::-1]
    model = load_model('first_model.h5')
    # model.summary()

    while GameExit:
        dt=clock.tick(fps)
        game_time+=dt
        #GameDisplay.blit(BackGround,(0,0))
        if collision:
            data_label(GameDisplay,dt,game_time,score,GameDets)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        GameLoop(length_required)
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
            if(len(moves)==0):
                break
            x = pd.DataFrame(snake.GetData())
            x = x.transpose()
            predictedMoves =  model.predict(x[0:9])
            # print('output : ' ,(model.layers[2].output)[0][0])
            move = getRandomMove(predictedMoves)
            # print(snake.GetData())
            # print('past' ,snake.past_cell)
            # print('move is' , predictedMove, ' ', move)
            if move=='l' and snake.direction['r']==False:
                if(snake.snake_length > 1):
                    snake.direction['l']=True
                snake.direction['u']=False
                snake.direction['d']=False
                snake.snake_sx=-20
                snake.snake_sy=0

            elif move=='r' and snake.direction['l']==False:
                if(snake.snake_length > 1):
                    snake.direction['r']=True
                snake.direction['u']=False
                snake.direction['d']=False
                snake.snake_sx=20
                snake.snake_sy=0
            elif move=='u' and snake.direction['d']==False:
                if(snake.snake_length > 1):
                    snake.direction['u']=True
                snake.direction['l']=False
                snake.direction['r']=False
                snake.snake_sy= -20
                snake.snake_sx=0
            elif move=='d' and snake.direction['u']==False:
                if(snake.snake_length > 1):
                    snake.direction['d']=True
                snake.direction['l']=False
                snake.direction['r']=False
                snake.snake_sy=20
                snake.snake_sx=0    
            if snake.snake_x-food.food_x==0 and snake.snake_y-food.food_y==0:
                score+=1
                # snake.snake_length+=1
                food.PlotFood(snake,GameDisplay)
            snake.past_cell = [snake.snake_x , snake.snake_y]
            snake.snake_x+=snake.snake_sx
            snake.snake_y+=snake.snake_sy
            if [snake.snake_x,snake.snake_y] in snake.snake_lst[:-1]:
                collision=True
            if not [snake.snake_x,snake.snake_y]==snake.snake_lst[-1]:
                snake.snake_lst.append([snake.snake_x,snake.snake_y])
            if len(snake.snake_lst)>snake.snake_length:
                del snake.snake_lst[0]
            GameDisplay.blit(BackGround,(0,0))
            drawLines(GameDisplay)
            GameDisplay.blit(food.food,(food.food_x,food.food_y))
            if snake.snake_x<0 or snake.snake_x>GameWidth-20 or snake.snake_y<0 or snake.snake_y>Gameheight-20:
                collision=True
            snake.polt_snake(GameDisplay)
        
        data_label(GameDisplay,dt,game_time,score,GameDets)
        pygame.display.update()
    pygame.quit()

GameLoop(6)

# print(getRandomMove())
# print(getRandomMove())
# print(getRandomMove())