import pygame
import random
pygame.init()
class Snake:
    def __init__(self):
        self.snake=pygame.image.load(r'C:\Users\jagat\Desktop\SnakeGame\snakeBody.PNG')
        self.snake_lst=[]
        self.snake_length=1
        self.snake_x=20
        self.snake_y=20
        self.snake_sx=0
        self.snake_sy=0
        self.direction=dict.fromkeys(['u','d','l','r'],False)
        #self.snake_lst.append([self.snake_x,self.snake_y])
    def polt_snake(self,GameDisplay):
        for val in self.snake_lst:
            GameDisplay.blit(self.snake,val)
class Food:
    def __init__(self):
        self.food=pygame.image.load(r'C:\Users\jagat\Desktop\SnakeGame\food2.PNG')
        self.food_x=(random.randint(20,500)//20)*20
        self.food_y=(random.randint(20,500)//20)*20
    def PlotFood(self,snake,GameDisplay):
        while True:
                self.food_x=(random.randint(0,500)//20)*20
                self.food_y=(random.randint(0,500)//20)*20
                if [self.food_x,self.food_y] in snake.snake_lst:
                    self.food_x=(random.randint(0,500)//20)*20
                    self.food_y=(random.randint(0,500)//20)*20
                else:
                    break
        #GameDisplay.blit(self.food,(self.food_x,self.food_y))

def drawLines(surface):
    #surface.fill((255,255,255))
    x,y=(0,0)
    for _ in range(25):
        x+=20
        y+=20
        pygame.draw.line(surface,(50,205,50),(x,0),(x,500))
        pygame.draw.line(surface,(50,205,50),(0,y),(500,y))


BackGround=pygame.image.load(r'C:\Users\jagat\Desktop\Snakegame\SnakeBG.PNG')
#font=pygame.font.SysFont(None,55)
GameDets=pygame.font.SysFont('monospace',10)
clock=pygame.time.Clock()
GameDisplay=pygame.display.set_mode((500,500))

def label(data,title,font,x,y,gameDisplay):
    _label=font.render(f'{title} {data}',1,(0,0,0))
    gameDisplay.blit(_label,(x,y))
    return y
def data_label(gameDisplay,dt,gameTime,score,font):
    y_pos=10
    gap=10
    x_pos=10
    y_pos=label(round(1000/dt,2),'FPS',font,x_pos,y_pos+gap,gameDisplay)
    y_pos=label(round(gameTime/1000,2),'Game Time',font,x_pos,y_pos+gap,gameDisplay)
    y_pos=label(score,'Score:',font,x_pos,y_pos+gap,GameDisplay)

def GameLoop():
    GameExit=True
    snake=Snake()
    food=Food()
    fps=10
    score=0
    game_time=0
    collision=False
    while GameExit:
        dt=clock.tick(fps)
        game_time+=dt
        GameDisplay.blit(BackGround,(0,0))
        if collision:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        GameLoop()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
                keys=pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_LEFT] and snake.direction['r']==False:
                        snake.direction['l']=True
                        snake.direction['u']=False
                        snake.direction['d']=False
                        snake.snake_sx=-20
                        snake.snake_sy=0
                    elif keys[pygame.K_RIGHT] and snake.direction['l']==False:
                        snake.direction['r']=True
                        snake.direction['u']=False
                        snake.direction['d']=False
                        snake.snake_sx=20
                        snake.snake_sy=0
                    elif keys[pygame.K_UP] and snake.direction['d']==False:
                        snake.direction['u']=True
                        snake.direction['l']=False
                        snake.direction['r']=False
                        snake.snake_sy= -20
                        snake.snake_sx=0
                    elif keys[pygame.K_DOWN] and snake.direction['u']==False:
                        snake.direction['d']=True
                        snake.direction['l']=False
                        snake.direction['r']=False
                        snake.snake_sy=20
                        snake.snake_sx=0
            if snake.snake_x-food.food_x==0 and snake.snake_y-food.food_y==0:
                score+=1
                snake.snake_length+=1
                food.PlotFood(snake,GameDisplay)
            snake.snake_x+=snake.snake_sx
            snake.snake_y+=snake.snake_sy

            if [snake.snake_x,snake.snake_y] in snake.snake_lst[:-1]:
                collision=True
            snake.snake_lst.append([snake.snake_x,snake.snake_y])
            if len(snake.snake_lst)>snake.snake_length:
                del snake.snake_lst[0]
            drawLines(GameDisplay)
            GameDisplay.blit(food.food,(food.food_x,food.food_y))
            if snake.snake_x<0 or snake.snake_x>480 or snake.snake_y<0 or snake.snake_y>480:
                collision=True
            snake.polt_snake(GameDisplay)
        data_label(GameDisplay,dt,game_time,score,GameDets)
        pygame.display.update()
    pygame.quit()

GameLoop()