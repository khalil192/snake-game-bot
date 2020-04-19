import pygame
import random
<<<<<<< HEAD
from snaky import Snake
=======
from snake import Snake
>>>>>>> e74f65ea9d5f7d5c0554e1e9ec2b86de46eeebdd

class Food:
    def __init__(self,path,rows,cols):
        self.img=pygame.image.load(path)
        self.boundaries=(rows,cols)
<<<<<<< HEAD
        self.rows = rows-2
        self.cols = cols-2
        self.food_x=(random.randint(2,self.rows))
        self.food_y=(random.randint(2,self.rows))
    def PlotFood(self,snake,GameDisplay):
            self.food_x=(random.randint(2,self.rows))
            self.food_y=(random.randint(2,self.cols))
            while (self.food_y,self.food_x) in snake.snake_lst:
                self.food_x=(random.randint(2,self.rows))
                self.food_y=(random.randint(2,self.cols))
    def FoodPosition(self):
        return self.food_y,self.food_x
=======
        self.food_x=(random.randint(3,self.boundaries[0]-1))
        self.food_y=(random.randint(3,self.boundaries[1]-1))
    def PlotFood(self,snake,GameDisplay):
        while True:
            self.food_x=(random.randint(0,self.boundaries[0]-1))
            self.food_y=(random.randint(0,self.boundaries[1]-1))
            if [self.food_x,self.food_y] in snake.snake_lst:
                self.food_x=(random.randint(0,(self.boundaries[0]-1)))
                self.food_y=(random.randint(0,(self.boundaries[1]-1)))
            else:
                #GameDisplay.blit(self.img,(self.food_x*20,self.food_y*20))
                break
>>>>>>> e74f65ea9d5f7d5c0554e1e9ec2b86de46eeebdd


if __name__=='__main__':
    pygame.init()
    snake=Snake(r'snakeBody.png',3,3,0)
    food=Food(r'food2.png',10,10)
