"""
Snake Eater Game
Made by IHEfty
"""
from tkinter import *
import random as rn

GAME_WIDTH = 720  
GAME_HEIGHT = 480  
SPEED = 50  
SPACE_SIZE = 10  
BODY_PARTS = 3 
SNAKE_COLOR = "#00FF00" 
FOOD_COLOR = "#FFFFFF" 
SPECIAL_FOOD_COLOR = "#FF0000"  
BACKGROUND_COLOR = "#000000" 
DIFFICULTY = 25 

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS 
        self.coordinates = [[100, 50]]  
        self.squares = [canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                         fill=SNAKE_COLOR, tag="snake") for x, y in self.coordinates]

class Food:
    def __init__(self):
        self.coordinates = self.place_food()  
        self.special_food_coordinates = None  

    def place_food(self):
        while True:
            x = rn.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = rn.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:  
                return [x, y]

    def spawn_special_food(self):
        self.special_food_coordinates = self.place_food()
        canvas.create_oval(self.special_food_coordinates[0], self.special_food_coordinates[1],
                           self.special_food_coordinates[0] + SPACE_SIZE, self.special_food_coordinates[1] + SPACE_SIZE,
                           fill=SPECIAL_FOOD_COLOR, tag="special_food")
        window.after(11000, self.remove_special_food)

    def remove_special_food(self):
        global special_food_active
        if special_food_active:  
            canvas.delete("special_food")
            self.special_food_coordinates = None
            special_food_active = False

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    x %= GAME_WIDTH
    y %= GAME_HEIGHT

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))

        canvas.delete("food") 
        food.coordinates = food.place_food()  
        canvas.create_oval(food.coordinates[0], food.coordinates[1],
                           food.coordinates[0] + SPACE_SIZE, food.coordinates[1] + SPACE_SIZE,
                           fill=FOOD_COLOR, tag="food")

        if score % 5 == 0:
            food.spawn_special_food()
            global special_food_active
            special_food_active = True  

    elif special_food_active and food.special_food_coordinates is not None:
        if x == food.special_food_coordinates[0] and y == food.special_food_coordinates[1]:
            score += 23  
            label.config(text="Score: {}".format(score))
            food.remove_special_food()  

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposite_directions = {
        'left': 'right', 'right': 'left',
        'up': 'down', 'down': 'up'
    }
    if new_direction != opposite_directions[direction]:  
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    return any(x == part[0] and y == part[1] for part in snake.coordinates[1:])

def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", font=('Arial', 70), fill="red")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
                       font=('consolas', 30), text="Final Score: {}".format(score), fill="white")
    restart_button.pack() 

def restart_game():
    global score, direction, snake, food, special_food_active
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    special_food_active = False  
    
    canvas.create_oval(food.coordinates[0], food.coordinates[1],
                       food.coordinates[0] + SPACE_SIZE, food.coordinates[1] + SPACE_SIZE,
                       fill=FOOD_COLOR, tag="food")  
    next_turn(snake, food)
    restart_button.pack_forget() 

window = Tk()
window.title("Snake Eater")  
window.resizable(False, False)  

score = 0
direction = 'down'  
special_food_active = False  

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

restart_button = Button(window, text="Restart", font=('consolas', 30), command=restart_game)
restart_button.pack_forget()  

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('a', lambda event: change_direction('left'))
window.bind('d', lambda event: change_direction('right'))
window.bind('w', lambda event: change_direction('up'))
window.bind('s', lambda event: change_direction('down'))

snake = Snake()
food = Food()
canvas.create_oval(food.coordinates[0], food.coordinates[1],
                   food.coordinates[0] + SPACE_SIZE, food.coordinates[1] + SPACE_SIZE,
                   fill=FOOD_COLOR, tag="food") 
next_turn(snake, food)

window.mainloop()
