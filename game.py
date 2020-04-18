import pygame
from snake import Snake
from food import Food
import random
pygame.init()

class Game:
    def __init__(self,path,rows):
        self.img=pygame.image.load(path)
        self.grid_size=(rows,rows)
        self.window_height=rows*20
        self.window_width=rows*20
        self.GameDisplay=pygame.display.set_mode((self.window_height,self.window_width))
        self.font=pygame.font.SysFont('monospace',6)
        self.clock=pygame.time.Clock()
        self.GameExit=False
    def DrawLines(self):
        x,y=(0,0)
        self.GameDisplay.blit(self.img,(0,0))
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
        y_pos=self.label(round(game_time/1000,2),'Game Time',x_pos,y_pos+gap)
        y_pos=self.label(score,'Score:',x_pos,y_pos+gap)
    def GameLoop(self):
        snake=Snake(r'snakeBody.png',3,3,0)
        food=Food(r'food2.png',10,10)
        game_time=0
        while not self.GameExit:
            dt=self.clock.tick(10)
            game_time+=dt
            score=0
            if not snake.is_alive:
                self.DataLabel(dt,game_time,score)
                print('Dead')
                print(snake.snake_lst)
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.GameExit=True
                        pygame.quit()
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_RETURN:
                            self.GameLoop()
            else:
                self.DrawLines()
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        self.GameExit=True
                snake.Move(random.choice(['l','r','u','d']),self.grid_size[0])
                if snake.snake_x-food.food_x==0 and snake.snake_y-food.food_y==0:
                    snake.snake_length+=1
                    score+=1
                    food.PlotFood(snake,self.GameDisplay)
                self.GameDisplay.blit(food.img,(food.food_x*20,food.food_y*20))
                snake.PlotSnake(self.GameDisplay)
            self.DataLabel(dt,game_time,score)
            pygame.display.update()


if __name__=='__main__':
    game=Game(r'SnakeBG.PNG',10)
    game.GameLoop()
