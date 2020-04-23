import pygame
from snaky import Snake
from food import Food
import random
from collections import defaultdict
import pandas
import time
  
import pandas as pd
import numpy
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

def getRandomMove(predictedMoves):
    moves = ['l', 'r', 'u', 'd']
    max1 = 0 
    max2 = 0
    predictedMoves = predictedMoves.tolist()[0]
    for i in range(4):
        if (predictedMoves[i] > predictedMoves[max1]):
            max2= max1
            max1 = i
        elif (predictedMoves[i] > predictedMoves[max2]):
            max2 = i
    if(predictedMoves[max1]/predictedMoves[max2] > 4):
        max2 = max1
    allowedMoves = [moves[max1], moves[max2]]
    return random.choice(allowedMoves)


class Game:
    def __init__(self,path,rows,file,episodes,render=True):
        self.grid_size=(rows,rows)
        self.window_height=rows*20
        self.window_width=rows*20
        self.GameExit=False
        self.h5=file
        self.episodes=episodes
        self.grid_length = rows
        self.render=render
        if self.render:
            pygame.init()
            self.img=pygame.image.load(path)
            self.GameDisplay=pygame.display.set_mode((self.window_height,self.window_width))
            self.font=pygame.font.SysFont('monospace',10)
            self.clock=pygame.time.Clock()
    def DrawLines(self):
        x,y=(0,0)
        self.GameDisplay.fill((255,255,255))
        for _ in range(self.grid_size[0]):
            x+=20
            y+=20
            pygame.draw.line(self.GameDisplay,(50,205,50),(x,0),(x,self.window_width))
            pygame.draw.line(self.GameDisplay,(50,205,50),(0,y),(self.window_height,y))
    def label(self,data,title,x,y):
        _label=self.font.render(f'{title} {data}',5,(0,0,0))
        self.GameDisplay.blit(_label,(x,y))
        return y
    def DataLabel(self,dt,game_time,score):
        y_pos=10
        gap=10
        x_pos=10
        y_pos=self.label(round(1000/dt,2),'FPS',x_pos,y_pos+gap)
        y_pos=self.label(game_time,'Game Time',x_pos,y_pos+gap)
        y_pos=self.label(score,'Score:',x_pos,y_pos+gap)
    def GameLoop(self):
        snake=Snake(r'snakeBody.png',2,4,2)
        food=Food(r'food2.png',*self.grid_size)
        model = load_model(self.h5)
        score=0
        data=defaultdict(list)
        start=time.time()
        while not self.GameExit and self.episodes:
            if self.render:
                dt=self.clock.tick(60)
            if not snake.is_alive:
                self.episodes-=1
                print(self.episodes)
                #self.DataLabel(dt,game_time,score)
                data['Game_Time'].append(time.time()-start)
                data['Score_achieved'].append(score)
                if self.render:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            self.GameExit=True
                            pygame.quit()
                snake=Snake(r'snakeBody.png',2,4,2)
                food=Food(r'food2.png',*self.grid_size)
                score=0
                start=time.time()    
            else:
                if self.render:
                    self.DrawLines()
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            self.GameExit=True
                        if event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_RETURN:
                                self.GameLoop()
                snake_instance = pd.DataFrame(snake.GetData(self.grid_length , food.food_y , food.food_x))
                snake_instance = snake_instance.transpose()
                moves = ['l', 'r' , 'u' , 'd']


                predictedMove = moves[model.predict_classes(snake_instance)[0]]
                # predictedMoves = model.predict(snake_instance)
                # predictedMove = getRandomMove(predictedMoves)
                # print(predictedMoves)
                #print('move is ', predictedMove)
                # print('snake lst' , snake.snake_lst)
                snake.Move(predictedMove,self.grid_size[0])
                if snake.snake_y-food.food_x==0 and snake.snake_x-food.food_y==0:
                    snake.snake_length+=1
                    score+=1
                    if self.render:
                        food.PlotFood(snake,self.GameDisplay)
                if self.render:
                    self.GameDisplay.blit(food.img,(food.food_x*20,food.food_y*20))
                    snake.PlotSnake(self.GameDisplay)
            if self.render:
                self.DataLabel(dt,time.time()-start,score)
                pygame.display.update()
        df=pd.DataFrame(data)
        df.index.name='episodes'
        df.index+=1
        #df.Game_Time*=scaling factor to save scaled values
        df.to_csv(self.h5.replace('.h5','.csv'))
        


if __name__=='__main__':
    game=Game(r'SnakeBG.PNG',30,'42_750_1.h5',30,render=False)
    game.GameLoop()
