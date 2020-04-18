import pygame
import random
from snake import Snake

class Food:
    def __init__(self,path,rows,cols):
        self.img=pygame.image.load(path)
        self.boundaries=(rows,cols)
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


if __name__=='__main__'
snake=Snake(r'snakeBody.png',3,3,0)
food=Food(r'food2.png',10,10)
Win=None
food.PlotFood(snake,Win)
print(snake.snake_lst)
print(snake.GetData())
print(food.food_x,food.food_y)