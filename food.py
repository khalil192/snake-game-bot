import pygame
import random
from snaky import Snake

class Food:
    def __init__(self,path,rows,cols):
        self.img=pygame.image.load(path)
        self.boundaries=(rows,cols)
        self.rows = rows-3
        self.cols = cols-3
        self.food_x=(random.randint(2,self.rows))
        self.food_y=(random.randint(2,self.rows))
    def PlotFood(self,snake,GameDisplay):
            self.food_x=(random.randint(2,self.rows))
            self.food_y=(random.randint(2,self.cols))
            while [self.food_y,self.food_x] in snake.snake_lst:
                self.food_x=(random.randint(2,self.rows))
                self.food_y=(random.randint(2,self.cols))
    def FoodPosition(self):
        return self.food_y,self.food_x


if __name__=='__main__':
    pygame.init()
    snake=Snake(r'snakeBody.png',3,3,0)
    food=Food(r'food2.png',10,10)
