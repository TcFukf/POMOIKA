# DOBRYA I POZITIVA KENT!  (╯°□°）╯︵ ┻━┻
# Hi!
from random import randint
import pygame
from module1 import *
 # colors
pygame.init()

width = 1100
height = 900
screen = pygame.display.set_mode((width, height))  # прописывается в  ScreenObj, или не туда выводит

# 
# 
# как рисовать фигуры
# pygame.draw.circle(Surface, color, pos, radius, width=0)
# pygame.draw.lines(Surface, color, closed, pointlist, width=1)
# pygame.draw.rect(Surface, color, Rect, width=0)
# pygame.draw.polygon(Surface, color, pointlist, width=0)

class ScreenObj:
    radius = 20
    surface = screen
    surface_color = BLACK # цвет фона
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
    def draw(self):
        pass # для каждого типы свой метод
    def info(self):
        return {'x':self.x,'y':self.y, 'type':'target'}

class Ball(ScreenObj):
    '''
    sunclass of Screen  Obj. Get x, y color, vx, vy (self) static ball is just ball with velocity 0
    '''
    def __init__(self, x, y, color,vx,vy):
        super().__init__(x, y, color)
        self.vx = vx
        self.vy = vy
        self.ay = 0.000000
        self.ax = 0.000000
    def draw(self):
        pygame.draw.circle(Ball.surface, self.color, (self.x,self.y), Ball.radius, width=0)
        return None
    def move(self):
        '''realesed 1 type of moving - ПРД(прямол,рарномерное)'''
        self.x += self.vx
        self.y += self.vy
        self.vx -= self.ax
        self.vy -= self.ay
        
        #print(self.vy)
class Gun(ScreenObj):
    '''
    sunclass of     Screen Obj
    get x , y color (self)
    '''
    long = 70
    def __init__(self, x, y, color):
        '''нужно для создания self.end_pos - координаты отслеживающего круга'''
        super().__init__(x, y, color)
        self.end_pos = [self.x,self.y-Gun.long]
        return None

    def follow(self):
        '''отслеживает курсор'''
        a = list(pygame.mouse.get_pos())
        if a[0]**2+a[1]**2 != 0:
            self.end_pos[0] = (Gun.long*a[0])/(a[0]**2+a[1]**2)**0.5+self.x
            self.end_pos[1] = (Gun.long*a[1])/(a[0]**2+a[1]**2)**0.5+self.y
            #print(a[1]/(a[0]**2+a[1]**2)**0.5)
            #print('x =',self.end_pos[0])
            #print('y =',self.end_pos[1])
    def draw(self):
        '''выводит обьект на экран'''
        pygame.draw.lines(Gun.surface, self.color, True, [(self.x,self.y),(self.end_pos[0],self.end_pos[1])], width=10)
        pygame.draw.circle(Gun.surface, RED, (self.end_pos[0],self.end_pos[1]), Gun.radius/2, width=0)
        #pygame.draw.circle(Gun.surface, RED, (self.x,self.y), Gun.radius/2, width=0)
        return None
    def info(self):
        return{'x': self.end_pos[0], 'y': self.end_pos[1], 'type': 'gun'}


class Shell(Ball):
    '''пули, которыми стрелют ДА ДА '''
    def info(self):
        return {'x':self.x,'y':self.y, 'type':'killer'}
    def draw(self):
        pygame.draw.circle(Ball.surface, self.color, (self.x,self.y), Ball.radius, width=0)
        return None
    def move(self):
        
        '''realesed 1 type of moving - ПРД(прямол,рарномерное)'''
        self.ax = 0
        self.ay = 0
        self.x += self.vx
        self.y += self.vy
        #self.vx += self.ax
        #self.vy += self.ay

class Manager:
    '''get self'''
    def __init__(self):
        self.ball_list = []
        self.gun_list = [] # добавляется в алл лист
        self.all_items = []
        return None

    def make_balls(self, vx, vy,count):
        '''добавляет объекты шары в список шаров (словари потом мб)'''
        for ball in range(count):  # random x ,y pink color and choised vx, vy
            x = randint(0,width)
            y = randint(0,height)
            color = PINK
            self.all_items.append(Ball(x,y,color,vx,vy))
        return None

    def make_shell(self, pos_x, pos_y, vx, vy, count):
        '''self, vx, vy, count'''
        '''добавляет объекты shell в список шаров (словари потом мб)'''
        for shell in range(count):  # random x ,y pink color and choised vx, vy
            x = pos_x
            y = pos_y
            color = GREY
            self.all_items.append(Shell(x,y,color,vx,vy))
        return None
    
    def delete_object(object,all_items):
            obj_index = all_items.index(object)
            all_items.pop(obj_index)
    def make_gun(self, x = 0, y = 0):
        '''добавляет объект GUN в список gun
        self, x = 0, y = 0
        '''
        self.gun_list.append(Gun(x, y, GREY))
        return None

    def draw_items(self):
        for item in self.all_items:
            item.draw()
        for gun in self.gun_list:
            gun.draw()
        return None

    def tracking(self):
        for gun in self.gun_list:
            gun.follow()
        return None
    def gun_info(self):
        for gun in self.gun_list:
            return gun.info()

    def move_items(self):
        for item in self.all_items:
            item.move()
    def check_collision(self):
        n = 1
        for object in self.all_items:         # LIST[A,B,C,D,E,F,G]
            for other_object in self.all_items[n:len(self.all_items)]:
                pos_obj = object.info()
                pos_other_obj = other_object.info()
                distance_x = pos_obj['x']-pos_other_obj['x']
                distance_y = pos_obj['y']-pos_other_obj['y']
                distance = (distance_x**2+distance_y**2)**0.5
                if distance <= object.radius*2:
                    if object.info()['type'] == 'killer' or other_object.info()['type'] == 'killer' :
                        if object.info()['type'] == 'killer':
                            object.vx +=2
                            object.vy += 2
                            Manager.delete_object(other_object,self.all_items)
                            Manager.delete_object(object,self.all_items)
                        else:
                            other_object.vx +=2
                            other_object.vy += 2
                            Manager.delete_object(object,self.all_items)
                            Manager.delete_object(other_object,self.all_items)
                            print('shell destroy')
                        pass
                    else:
                        #print('столкновение')
                        other_object.color = YELLOW
                        object.color = BLUE
                        object.vx  = -object.vx*1.5
                        object.vy  = -object.vy*randint(75,96)/60  # маин тема, но я решил трай с ускорением
                        #object.ax *= -1
                        #object.ay *= -1
                        object.move()
                        other_object.vx  = -other_object.vx*1.5
                        other_object.vy  = -other_object.vy*1.5
                        #other_object.ax *= -1
                        #other_object.ay *= -1
                        other_object.move()
            n +=1
        return None
    
    def check_visiable(self):
        for object in self.all_items:
                pos_obj = object.info()
                distance_x_right = abs(pos_obj['x']-width)
                #print('ДИСТАНциЯ ПО XR  ',distance_x_right)
                # дистанция с правой границей
                distance_x_left = width - distance_x_right
                #print('ДИСТАНциЯ ПО XL  ',distance_x_left)
                # дистанция с левой границей
                distance_y_down = abs(pos_obj['y']-height)
                # дистанция с нижней границей
                distance_y_up = height - distance_y_down
                # дистанция с верхней границей
                if (distance_x_right <= object.radius) or (distance_x_left <= object.radius):
                    object.vx  = -object.vx*0.6
                    object.ax *= -1 # улетают далеко
                    object.move()

                if (distance_y_down <= object.radius) or (distance_y_up <= object.radius) :
                    object.vy  = -object.vy*0.6
                    object.ay *= -1
                    object.move()
        return None

class LevelManager:
    ''' get count ball'''
    def __init__(self, count_ball, event = None):
        self.count_ball = count_ball
        self.manager = Manager()

    def load_lvl(self,Vx =1, Vy = 1):
        #self.manager.make_balls(Vx, Vy, self.count_ball)
        self.manager.make_gun(x = 0, y = 0)
        # ЗАГРУЖАЕМ ЧТО НУЖНО

    def work(self):
        self.manager.draw_items()
        self.manager.check_collision()
        self.manager.check_visiable()
        self.manager.move_items()
        self.manager.tracking()
    def event(self,V = 3):
        self.manager.tracking()
        gun_info = self.manager.gun_info()
        gun_x, gun_y = gun_info['x'], gun_info['y']
        hypotenuse = (gun_x**2+gun_y**2)**0.5
        sin_angle  = gun_y/ hypotenuse
        cos_angle = (1-sin_angle**2)**0.5
        Vy = sin_angle * V
        Vx = V*cos_angle
        print(Vx, ' Vx')
        print(Vy, ' Vy')
        self.manager.make_shell(gun_x, gun_y, Vx, Vy, 1)

    def spawn_targer(self,Vx = 1, Vy = 1):
        self.manager.make_balls(Vx, Vy, self.count_ball)
level = LevelManager(10)
level.load_lvl()
#a = Manager()
#a.make_gun()
#a.make_balls(0,0,1)
#a.draw_items()



finish = False

while not finish:
    try:
        level.work()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    print('ABOBA')
                    level.event()
                elif event.key == pygame.K_w:
                    level.spawn_targer()
    except:
        print('fail')
    pygame.display.flip()
    pygame.time.wait(0)
    #print('итерация ')
    screen.fill((0,0,0))



# OGO !!!
pygame.quit()



