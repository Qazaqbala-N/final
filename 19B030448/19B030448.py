import pygame
from enum import Enum
import random
import sys


import pika
import sys
import json
import time
import uuid
import time
from threading import Thread


pygame.init()
screen=pygame.display.set_mode((800,600))
bullets=[]
shootsound=pygame.mixer.Sound("tank_sound3.wav")
backgroundmusic=pygame.mixer.music.load("bg_sound.mp3")
pygame.mixer.music.play(-1)

backgroundImage=pygame.image.load("backgr.jpg")
gamebackgroundImage=pygame.image.load("background.jpg")
wallImage=pygame.image.load("wall.jpg")
font = pygame.font.SysFont('Times new roman', 32)


IP='34.254.177.17'
PORT=5672
VIRTUAL_HOST='dar-tanks'
USERNAME='dar-tanks'
PASSWORD='5orPLExUYnyVYZg48caMpX'
infoPanel=pygame.image.load("infoPanel.jpg")
pygame.init()
# screen= pygame.display.set_mode((1000,600))
shootsound=pygame.mixer.Sound("C:\\Users\\user\\Desktop\\semester\\homework\\lecture3\\tank_sound3.wav")
tank1=pygame.image.load("tankd.png")
tankr=pygame.transform.rotate(tank1, 90)
tankd=pygame.transform.rotate(tank1,0)
tankl=pygame.transform.rotate(tank1, 270)
tanku=pygame.transform.rotate(tank1, 180)

tank2=pygame.image.load("tank2.png")
tanker=pygame.transform.rotate(tank2, 270)
tanked=pygame.transform.rotate(tank2,180)
tankel=pygame.transform.rotate(tank2, 90)
tankeu=pygame.transform.rotate(tank2, 0)

class Direction(Enum):
    UP=2
    DOWN=4
    LEFT=1
    RIGHT=3

class Tank:

    def __init__(self,x,y,speed,color,info,shoot, d_right = pygame.K_RIGHT,d_left = pygame.K_LEFT,d_down = pygame.K_DOWN,d_up = pygame.K_UP):
        self.x=x
        self.y=y
        self.speed=speed
        self.color=color
        self.shoot=shoot
        self.width=30
        self.direction=Direction.LEFT
        self.timer=0
        self.hp=3
        self.KEY ={d_right:Direction.RIGHT,d_left:Direction.LEFT,d_up:Direction.UP,d_down:Direction.DOWN}
        self.info=info
        self.a=False
        self.bonustime=0
 
    def  draw(self):
        tank_c = (self.x+int(self.width/2),self.y+int(self.width/2))
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.width),2)
        pygame.draw.circle(screen,self.color,tank_c,int(self.width/2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen,self.color,tank_c,(self.x+self.width+int(self.width/2),self.y+int(self.width/2)),4)

        if self.direction == Direction.LEFT:
             pygame.draw.line(screen,self.color,tank_c,(self.x-int(self.width/2),self.y+int(self.width/2)),4) 

        if self.direction == Direction.UP:
             pygame.draw.line(screen,self.color,tank_c,(self.x+int(self.width/2),self.y-int(self.width/2)),4)

        if self.direction == Direction.DOWN:
             pygame.draw.line(screen,self.color,tank_c,(self.x+int(self.width/2),self.width+self.y+int(self.width/2)),4)     

   
    def change_direction(self,direction):
        self.direction = direction
    
    def move(self):
            if self.direction ==Direction.LEFT:
                self.x-=self.speed
            if self.direction ==Direction.RIGHT:
                self.x+=self.speed
            if self.direction ==Direction.UP:
                self.y-=self.speed
            if self.direction ==Direction.DOWN:
                self.y+=self.speed
            if self.x>797:
                self.x=0
            if self.y>597:
                self.y=0 
            if self.x<0 :
                self.x=797
            if self.y<0:
                self.y=597       
            self.draw()

    def attack(self):
        if self.direction ==Direction.LEFT:
            bullets.append(Bullet(self.x-int(self.width/2),self.y+int(self.width/2),self.direction,self.color,self))        
        elif self.direction ==Direction.RIGHT:
            bullets.append(Bullet(self.x+self.width+int(self.width/2),self.y+int(self.width/2),self.direction,self.color,self))   
        elif self.direction ==Direction.UP:
            bullets.append(Bullet(self.x+int(self.width/2),self.y-int(self.width/2),self.direction,self.color,self))    
        elif self.direction ==Direction.DOWN:
            bullets.append(Bullet(self.x+int(self.width/2),self.width+self.y+int(self.width/2),self.direction,self.color,self))  
        shootsound.play()
    
    def hpshow(self):
        hptext=font.render('HP: '+str(self.hp),True,self.color)
        screen.blit(hptext,self.info)
    def ultra(self,speed):
        self.speed=speed
s=6
class Bullet():
    def __init__(self,x,y,direction,color,tank):
        self.x=x
        self.y=y
        self.direction=direction
        self.color=color
        self.tank=tank
        self.t=10
        
        
    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),3)
    
    def move(self):
        if self.direction== Direction.RIGHT:
            self.x+=s
        elif self.direction== Direction.LEFT:
            self.x-=s
        elif self.direction== Direction.UP:
            self.y-=s
        elif self.direction== Direction.DOWN:
            self.y+=s
        if self.x>797:
            self.x=0
        if self.y>597:
            self.y=0 
        if self.x<0 :
            self.x=797
        if self.y<0:
            self.y=597    
        self.draw()


class Menu():
    def __init__(self,punkts=[120,140,u'Punkt',(250,250,30),(250,30,250)]):
        self.punkts=punkts
    
    def render(self,poverhnost,font,num_punkt):
        for i in self.punkts:
            if num_punkt==i[5]:
                screen.blit(font.render(i[2],True,i[4]),(i[0]-50,i[1]))
            else :
                screen.blit(font.render(i[2],True,i[3]),(i[0]-50,i[1]))

    def menu(self):
        mainloop =True
        font_menu =pygame.font.SysFont('Times new roman', 32)
        punkt =0
        while mainloop:
            screen.blit(backgroundImage,(0,0))
            mp=pygame.mouse.get_pos()

            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+55 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt = i[5]
            self.render(screen,font_menu,punkt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key==pygame.K_UP:
                        punkt-=1
                        if punkt<0:
                            punkt = 2
                    if event.key==pygame.K_DOWN:
                        if punkt>len(self.punkts)-1:    
                            punkt+=1
                if event.type== pygame.MOUSEBUTTONDOWN and event.button==1:
                    if punkt ==0 :
                        return 0   
                    elif punkt==1:
                        return 1
                    elif punkt==2:
                        return 2

            screen.blit(screen,(0,0))
            pygame.display.flip()    


class TankRpcClient:

    def __init__(self):
        self.connection=pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel=self.connection.channel()
        queue = self.channel.queue_declare(queue='',
        auto_delete=True,
        exclusive=True   )

        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response= None
        self.corr_id=None
        self.token=None
        self.tank_id=None
        self.room_id=None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            
    
    def call(self,key,message={}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message))
        while self.response is None:
            self.connection.process_data_events()
    
    def check_server_status(self):
        self.call('tank.request.healthcheck')
        return self.response['status']=='200'

    def obtain_token(self,room_id):
        message={
            'roomId':room_id
        }
        self.call('tank.request.register',message)
        if 'token' in self.response:
            self.token=self.response['token']
            self.tank_id= self.response['tankId']
            self.room_id=self.response['roomId']
            return True
        return False

    def turn_tank(self,token,direction):
        message={
            'token':token,
            'direction':direction

        }
        self.call('tank.request.turn',message)
    
    def fire_bullet(self,token):
        message={
            'token': token,
        }
        self.call('tank.request.fire',message)


class TankConsumerclient(Thread):
    def __init__(self,room_id):

        super().__init__()
        self.connection=pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel=self.connection.channel()

        queue = self.channel.queue_declare(queue='',
        auto_delete=True,
        exclusive=True   )

        event_listener=queue.method.queue

        self.channel.queue_bind(exchange='X:routing.topic',
        
                                        queue=event_listener,
                                        routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
       
        
    def run(self):
        self.channel.start_consuming()

UP='UP'
DOWN='DOWN'
LEFT='LEFT'
RIGHT='RIGHT'
Gamever=pygame.image.load("Gameover.png")
MOVE_KEYS={
    pygame.K_w:UP,
    pygame.K_s:DOWN,
    pygame.K_a:LEFT,
    pygame.K_d:RIGHT
}
def lose(screen):
    time.sleep(10)
    screen.blit(Gamever,(0,0))
    
    
def draw_tank(screen, x,y,width,height,direction,id,health,score,**kwargs):
    if id==client.tank_id:
        if direction=='UP': 
            screen.blit(tanku,(x,y))
        elif direction=='DOWN':
            screen.blit(tankd,(x,y))
        elif direction=='RIGHT':
            screen.blit(tankr,(x,y))
        elif direction=='LEFT':
            screen.blit(tankl,(x,y))
    elif id!=client.tank_id:
        if direction=='UP': 
            screen.blit(tankeu,(x,y))
        elif direction=='DOWN':
            screen.blit(tanked,(x,y))
        elif direction=='RIGHT':
            screen.blit(tanker,(x,y))
        elif direction=='LEFT':
            screen.blit(tankel,(x,y))

def panel(screen,info, x, y):
    screen.blit(info,(x,y))

def Sort(data):
    return data['score']

def draw_bullet(screen, x,y,width,height,direction,owner,a,b,c):
    pygame.draw.rect(screen,(a,b,c),(x,y,width,height))


font = pygame.font.Font('freesansbold.ttf', 12)
font1 = pygame.font.SysFont("comicsansms",20)
font2 = pygame.font.SysFont('Times new roman', 12)
def game_start(screen,event_client):
    mainloop=True
     
    while mainloop:
        screen.fill((0,200,0))
        screen.blit(infoPanel,(831,0))
        screen.blit(font1.render(f"INFORMATION",True,(240,10,130)),(852,30))
        for event in pygame.event.get():       
            if event.type == pygame.QUIT:
                mainloop = False           
                client.connection.close()
                sys.exit(0)    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False       
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token,MOVE_KEYS[event.key])
                if event.key==pygame.K_SPACE:
                    client.fire_bullet(client.token)

    #============================================================#remainig time    
        try:
            remaining_time= event_client.response['remainingTime']
            text = font.render('Remaining Time: {}'.format(remaining_time), True,(0,0,0))
            textRect = text.get_rect()
            textRect.center = (1854//2, 1104//2)
            screen.blit(text,textRect)
        except:
            pass
    #==============================================================#   
        kicked = event_client.response['kicked']  
        for kick in kicked:
            if kick['tankId']==client.tank_id:
                game.menu()
                client.connection.close()
                 
        bullets= event_client.response['gameField']['bullets']
        winners = event_client.response['winners']
        tanks = event_client.response['gameField']['tanks']
        tanks.sort(key=Sort,reverse=True)
        losers = event_client.response['losers']


        for loser in losers:
            if loser['tankId']==client.tank_id:
                lose(screen)
        
        for winner in winners:
            if winner['tankId']==client.tank_id:
                lose(screen)

        for tank in tanks:
            # tank_x=tank['x']
            # tank_y=tank['y']
            # tank_width=tank['width']
            # tank_height=tank['height']
            # tank_direction=tank['direction']
        
            tank_id=tank['id']
            tank_score=tank['score']
            tank_hp=tank['health']
        
            draw_tank(screen,**tank)
            

        for bullet in bullets:
            bullet_x=bullet['x']
            bullet_y=bullet['y']
            bullet_width=bullet['width']
            bullet_height=bullet['height']
            bullet_direction=bullet['direction']
            bullet_owner=bullet['owner']
            if bullet['owner']==client.tank_id:
                a,b,c=255,0,0   
            else:
                a,b,c=255,255,0 
            draw_bullet(screen, bullet_x,bullet_y,bullet_width,bullet_height,bullet_direction,bullet_owner,a,b,c)

        k=0
        for tank in tanks:
            
            Me=font2.render('{0}: Score: {1},Hp: {2}'.format(tank['id'],tank['score'],tank['health']),True,(123,123,123)) 
            Etank=font2.render('{0}: Score: {1},Hp: {2}'.format(tank['id'],tank['score'],tank['health'],),True,(255,255,0))
            if tank['id']==client.tank_id:
                tank_score=tank['score']
                screen.blit(Me,(850,150+(20*k)))
                k+=1
            else:
                screen.blit(Etank,(850,160+(20*k)))
                k+=1    


        pygame.display.update()       

client= TankRpcClient()
 


   
    

class Wall():
    def __init__(self):
        self.x=random.randrange(0,20)*40
        self.y=random.randrange(0,15)*40
        self.image=pygame.image.load("wall.jpg")
        self.hp=1
    def draw(self):
        screen.blit(self.image,(self.x,self.y))

class Food():
    def __init__(self):
        self.x=random.randint(0,790)
        self.y=random.randint(0,590)
        self.image=pygame.image.load("bonus.png") 
        self.active=True
    def draw(self):
        if self.active==True:
            screen.blit(self.image,(self.x,self.y))

    




punkts = [(350,200,u'Single Player',(250,250,30),(250,30,250),0),
          (360,240,u'Multiplayer',(250,250,30),(250,30,250),1),
          (350,280,u'MultiplayerAI',(250,250,30),(250,30,250),2)]

start=True
game=Menu(punkts)
def single():
    tank1=Tank(500,300,4,(0,123,100),(700,10),pygame.K_RETURN)
    tank2=Tank(300,300,4,(0,250,250),(10,10),pygame.K_SPACE,pygame.K_d,pygame.K_a,pygame.K_s,pygame.K_w)
    tanks=[tank1,tank2]

    FPS =13
    clock=pygame.time.Clock()

    walls=[]
    for i in range(15):
        walls.append(Wall())
    tim=0
    food=Food()
    mainloop = True
    while mainloop:
        millis= clock.tick(FPS)
        second=millis/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    return True
                for tank in tanks:    
                    if event.key in tank.KEY.keys() :
                        tank.change_direction(tank.KEY[event.key])
                    if event.key ==tank.shoot and tank.timer>1:
                        tank.attack()
                        tank.timer=0
                    if all((food.x>=tank.x,food.x<=tank.x+tank.width,food.y>=tank.y,food.y<=tank.y+tank.width)) and food.active==True:
                        food.active=False
                        tank.bonustime=5
         

                        
                        
                        
                    
        try:
            for tank in tanks:
                for i in range(len(bullets)):
                    if all((bullets[i].x>=tank.x,bullets[i].x<=tank.x+tank.width,bullets[i].y>=tank.y,bullets[i].y<=tank.y+tank.width,bullets[i].tank!=tank)):
                        bullets.pop(i)
                        tank.hp-=1  
                for  i in range(len(bullets)):
                    if bullets[i].t<0:
                        bullets.pop(i)
                for i in range(len(tanks)):
                    if tanks[i].hp<=0:
                        tanks.pop(i)
                tank.bonustime-=second
                if tank.bonustime>=0:
                    tank.move()
                    
                for wall in walls:   
                    for i in range(len(walls)):        
                        if all((walls[i].x>=tank.x,walls[i].x<=tank.x+tank.width,walls[i].y>=tank.y,walls[i].y<=tank.y+tank.width)):
                            walls.pop(i)
                            tank.hp-=1
            
            for wall in walls:
                for i in range(len(bullets)):
                    if all((bullets[i].x>=wall.x,bullets[i].x<=wall.x+tank.width,bullets[i].y>=wall.y,bullets[i].y<=wall.y+tank.width)):
                        bullets.pop(i)
                        wall.hp-=1
                for i in range(len(walls)):
                    if walls[i].hp<=0:
                        walls.pop(i)  
                     
        except IndexError:
            pass
            
        

        tim+=second
        if tim>10:
            food.active=True
            tim=0
            food.x=random.randint(0,790)
            food.y=random.randint(0,590)
        screen.blit(gamebackgroundImage,(0,0))
        food.draw()
        for wall in walls:
            wall.draw()
        for tank in tanks:
            tank.move()
            tank.hpshow()
            tank.timer+=second
        for bullet in bullets:
            bullet.move()
            if tank.bonustime>=0:
                bullet.move() 
            bullet.t-=second

        if len(tanks)<2:
            screen.blit(Gamever,(0,0))
            
        pygame.display.flip()

def multi():
    event_client = TankConsumerclient('room-24')
    screen = pygame.display.set_mode((1030,600))
    client.check_server_status() 
    client.obtain_token('room-24')
    event_client.daemon=True
    event_client.start()
    game_start(screen,event_client)
    
    screen = pygame.display.set_mode((800,600))

def ii():
    event_client = TankConsumerclient('room-1')
    screen = pygame.display.set_mode((1030,600))
    client.check_server_status() 
    client.obtain_token('room-1')
    event_client.daemon=True
    event_client.start()
    game_start(screen,event_client)
    
    screen = pygame.display.set_mode((800,600))

while start:    
    a=game.menu()
    if a==0:
        single()
    elif a==1:
        multi()
    elif a==2:
        ii()


pygame.quit()

