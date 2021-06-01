# HELLO GITHUB ahahaah)
import pygame
from pygame.draw import *
from random import randint
pygame.init()

 # DEFINE FPS , width screen , height screen and create screen
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))

 # DEFINE FPS,finished is boolean value. if finished = False -> programm work  
FPS = 2
clock = pygame.time.Clock()
finished = False

 # CREATE NEEDED COlORS 
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


 # DEFINE items for programm
points = 0
items_list = [] # чудеса интеллекта- просто содержит координаты ТЕЛ и размеры опорных частей ...

 # спрашиваем, кто 
profile = 'тиси ФИ вфкВ'

# DEFINE functions 

def make_ball(width,height,screen_ = screen,color = BLUE,type = 'static'):
    '''
    func draw ball on x,y random coordinats of main screen
    width - width screen ()
    height - height sreen () 
    type - 'static' or 'move' 
    ball have determined radius calculus from size screen
    Return --> None (x,y,rad,type - 'static' or 'move' in items_list)
    '''
    type = type
    static_x_circ = randint(0,width)
    static_y_circ = randint(0,height)
    static_radius = 12
    item = list((static_x_circ,static_y_circ,static_radius,type))
    circle(screen_,color,(item[0],item[1]),item[2])
    items_list.insert(0,item)
    return item

def move_ball(move_x,move_y,width = width,height = height):
    '''
    функция двигает item опираясь на размеры экрана
    move_x насколько топать аналогично - 
    move_y
    Return --> None
    '''
    global items_list
    for item in items_list:
        if item[3] == 'move':
            circle(screen,BLACK,(item[0],item[1]),item[2])
            
            item[0] += move_x
            item[1] += move_y
            circle(screen,RED,(item[0],item[1]),item[2])
            if item[0] >= width:
                print('УЛЕТЕЛ ',item)
                circle(screen,BLACK,(item[0],item[1]),item[2]) # закрашиваем и удаляй из списка шары, которые улетели за экран
                items_list.pop(items_list.index(item))
            if item[1] >= height:
                print('УЛЕТЕЛ ',item)
                circle(screen,BLACK,(item[0],item[1]),item[2])
                items_list.pop(items_list.index(item))


    return None




def MBD_cheker(event):
    ''''
    я заея на англ писать
    Функция обрабатывает событие MOUSEBUTTONDOWN из PYGAME
    Плюсует поинты в points
    return --None
    '''
    global items_list,points
    n = 0
    for item  in items_list:
        item = list(item)  # item список [x1,y1,radius,type]
        mouse_pos = list(event.pos) # mouse_pos - список [x2,y2]
        distanse_x = item[0] - mouse_pos[0]
        distanse_y = item[1] - mouse_pos[1]
        distanse = (distanse_x**2+distanse_y**2)**0.5  # ну тут все понятно, если сдать огэ на "3"
        if distanse <= item[2]:
            print('ПРОБИТИЕ !Й!',item)
            circle(screen,BLACK,(item[0],item[1]),item[2]) # закрашиваем шарики, в которые мы попали
            items_list.pop(n) # также убираем их из списка
            if item[3] == 'static':
                points +=1           # даем очки в зависимости от типа шарика
            elif item[3] == 'move':
                points += 2
       # else:  # если не попал, то выодиться Miss в консоль
           # print('Miss')

        n += 1   # счетчик итерация для цикла for in , для того чтобы pop'нуть n елемент из списка
    return None

# РАБОТАЕМ !!!
while not finished:
# draw balls and wait time for click
    if len(items_list) <= 2: # исключает спам
        make_ball(width,height,type = 'move',color = RED)  # создаем шарики разных типов
    move_ball(2,1)       # двигаем шарики, которые долдны двигаться
    move_ball(-2,1) 
    clock.tick(70)
    pygame.display.update()
 # ОБРАБАТЫВАЕМ ЕВЕНТЫ ыы
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MBD_cheker(event)
    pygame.display.update()
  #  print(len(items_list))  # выводило кол-во итемов живых

with open(r"D:\ЛАБЫ МФТИ\profiles.txt",'a',encoding = 'utf-8') as file:
    file.write(f"{profile}:{points}\n")

print(profile,' набрал: ',points," points")
#close pygame screen
pygame.quit()
