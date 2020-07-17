import pygame
import random

pygame.init()
pygame.display.set_caption('SnakeGame')
snake=pygame.image.load(r'C:\Users\jagat\Desktop\snakeBody.PNG')
food=pygame.image.load(r'C:\Users\jagat\Desktop\food2.PNG')
font=pygame.font.SysFont(None,55)
GameDisplay=pygame.display.set_mode((500,500))
def screen_score(text,color,x,y):
    screen_text=font.render(text,True,color)
    GameDisplay.blit(screen_text,[x,y])
def drawLines(surface):
    surface.fill((255,255,255))
    x,y=(0,0)
    for _ in range(25):
        x+=20
        y+=20
        pygame.draw.line(surface,(50,205,50),(x,0),(x,500))
        pygame.draw.line(surface,(50,205,50),(0,y),(500,y))
def plot_snake(snake_lst):
    for val in snake_lst:
        GameDisplay.blit(snake,val)
def GameLoop():
    score=0
    collision=False
    GameExit=False
    snake_lst=[]
    snake_length=1
    snake_x=20
    snake_y=20
    direction=dict.fromkeys(['u','d','l','r'],False)
    fps=10
    snake_sx=0
    snake_sy=0
    clock=pygame.time.Clock()
    food_x=(random.randint(0,500)//20)*20
    food_y=(random.randint(0,500)//20)*20
    while not GameExit:
        if collision:
            screen_score(f'Game Over',(255,0,0),140,100)
            screen_score(f'Score: {score}',(0,0,0),140,200)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        GameLoop()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    GameExit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT and direction['l']==False:
                        direction['r']=True
                        direction['u']=False
                        direction['d']=False
                        snake_sx=20
                        snake_sy=0
                    if event.key==pygame.K_LEFT and direction['r']==False:
                        direction['l']=True
                        direction['u']=False
                        direction['d']=False
                        snake_sx=-20
                        snake_sy=0
                    if event.key==pygame.K_UP and direction['d']==False:
                        direction['u']=True
                        direction['l']=False
                        direction['r']=False
                        snake_sy= -20
                        snake_sx=0
                    if event.key==pygame.K_DOWN and direction['u']==False:
                        direction['d']=True
                        direction['l']=False
                        direction['r']=False
                        snake_sy=20
                        snake_sx=0
            if snake_x-food_x==0 and snake_y-food_y==0:
                score+=1
                snake_length+=1
                while True:
                    food_x=(random.randint(0,500)//20)*20
                    food_y=(random.randint(0,500)//20)*20
                    if [food_x,food_y] in snake_lst:
                        food_x=(random.randint(0,500)//20)*20
                        food_y=(random.randint(0,500)//20)*20
                    else:
                        break
            snake_x+=snake_sx
            snake_y+=snake_sy
            
            if [snake_x,snake_y] in snake_lst[:-1]:
                collision=True
            snake_lst.append([snake_x,snake_y])
            if len(snake_lst)>snake_length:
                del snake_lst[0]
            drawLines(GameDisplay)
            if snake_x<0 or snake_x>480 or snake_y<0 or snake_y>480:
                collision=True
            GameDisplay.blit(food,(food_x,food_y))
            plot_snake(snake_lst)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
GameLoop()
            
