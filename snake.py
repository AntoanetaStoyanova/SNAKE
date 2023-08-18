import PySimpleGUI as sg
from time import time
from random import randint

def convert_pos_to_pixel(cell):
#convert to pixel
    tl = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE 
    br = tl[0] + CELL_SIZE, tl[1] + CELL_SIZE
    return tl, br

def place_apple():
    apple_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    while apple_pos in snake_body:
        apple_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    return apple_pos

#game constants
FIELD_SIZE = 400
CELL_NUM = 10 #number of cells
CELL_SIZE = FIELD_SIZE / CELL_NUM #size of cells

#snake
snake_body = [(4,4),(3,4),(2,4)]  #LISTE IN TUPLES
DIRECTIONS = {'left':(-1,0), 'right':(1,0), 'up':(0,1), 'down':(0,-1)}  #dictionary
direction = DIRECTIONS['up']

#apple  (position of the apple, with tuple)
apple_pos = (0,0)
apple_eaten = False

sg.theme('Green')
#visual
field = sg.Graph (   #graph element
    canvas_size = (FIELD_SIZE,FIELD_SIZE), #width, height canvas_size = (w,h)
    graph_bottom_left = (0,0),  #tuple (x,y)
    graph_top_right = (FIELD_SIZE,FIELD_SIZE),
    background_color = 'black')
layout = [[field]]

window = sg.Window('Snake', layout, return_keyboard_events = True) #for the keyboard, moves, later we check for the event


start_time = time()
while True:
    event, values = window.read(timeout = 10)
    if event == sg.WIN_CLOSED:
        break

    if event == 'Left:37':
        direction = DIRECTIONS['left']
    if event == 'Up:38':
        direction = DIRECTIONS['up']
    if event == 'Right:39':
        direction = DIRECTIONS['right']
    if event == 'Down:40':
        direction = DIRECTIONS['down']
    
    time_since_start = time() - start_time
    if time_since_start >= 0.5:
        start_time = time()

        #apple snake collision
        if snake_body[0] == apple_pos:
            apple_pos = place_apple()
            apple_eaten = True

        #snake update
        new_head = (snake_body[0][0] + direction[0],snake_body[0][1] + direction[1])
        snake_body.insert(0,new_head)
        if not apple_eaten:
            snake_body.pop()
        apple_eaten = False

        #RIP snake
        if not 0 <= snake_body[0][0] <= CELL_NUM - 1  or\
            not 0 <= snake_body[0][1] <= CELL_NUM - 1 or\
            snake_body[0] in snake_body[1:]:
            break

        field.DrawRectangle((0,0),(FIELD_SIZE,FIELD_SIZE), 'black')

        tl, br = convert_pos_to_pixel(apple_pos)
    #draw apple position
        field.DrawRectangle(tl,br,'red')  #(topleft,bootmright,color)

        

    #DRAW SNAKE
        for index, part in enumerate(snake_body):
            tl, br = convert_pos_to_pixel(part)
            color = 'yellow' if index == 0 else 'green'
            field.DrawRectangle(tl,br,color)




window.close()