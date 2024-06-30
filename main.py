import turtle
import pandas
import random
import time

# Set up the screen
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.title("SA Provinces Game")
image = "output.gif"
screen.addshape(image)
turtle.shape(image)

# Load data
data = pandas.read_csv("SA_Provinces.csv")
all_provinces = data.province.to_list()
guessed_provinces = []

# Create a turtle object for the timer
timer_turtle = turtle.Turtle()
timer_turtle.hideturtle()
timer_turtle.penup()
# position the timer on screen
timer_turtle.goto(0, 260)

# Timer countdown function
def update_timer(time_left):
    timer_turtle.clear()
    timer_turtle.write(f"Time Left: {time_left} seconds", align="center", font=("Arial", 16, "normal"))
    if time_left > 0 and len(guessed_provinces) < 9:
        screen.ontimer(lambda: update_timer(time_left - 1), 1000)
    elif len(guessed_provinces) == 9:
        congratulate()

# Function to end the game
def end_game():
    screen.bye()

# Function to display missing provinces
def display_missing_provinces(missing_provinces):
    for province in missing_provinces:
        province_data = data[data.province == province]
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(int(province_data.x), int(province_data.y))
        t.color("red")
        t.write(province_data.province.item(), align="center", font=("Arial", 16, "normal"))

# Function to congratulate the player
def congratulate():
    timer_turtle.clear()
    turtle.bgcolor("yellow")
    turtle.write("Congratulations!\nYou guessed all provinces!", align="center", font=("Arial", 40, "normal"))

# Start the timer with 60 seconds
update_timer(60)

while len(guessed_provinces) < 9:
    answer_province = screen.textinput(title=f"{len(guessed_provinces)}/9 Provinces Correct",
                                       prompt="What's another Province's name? Type 'Exit' to quit.").title()
    if answer_province == "Exit":
        missing_provinces = [province for province in all_provinces if province not in guessed_provinces]
        new_data = pandas.DataFrame(missing_provinces)
        new_data.to_csv("provinces_to_learn.csv")
        display_missing_provinces(missing_provinces)
        time.sleep(5)
        screen.bye()
        break
    if answer_province in all_provinces:
        if answer_province not in guessed_provinces:
            guessed_provinces.append(answer_province)
            t = turtle.Turtle()
            t.hideturtle()
            t.penup()
            province_data = data[data.province == answer_province]
            t.goto(int(province_data.x), int(province_data.y))
            t.color(random.choice(['red', 'blue', 'green', 'purple', 'orange', 'brown', 'black', 'pink', 'cyan']))
            t.write(province_data.province.item(), align="center", font=("Arial", 16, "normal"))
        else:
            screen.textinput(title="Already Guessed", prompt=f"You already guessed {answer_province}. Try again.")
    else:
        screen.textinput(title="Incorrect Guess", prompt=f"{answer_province} is not a correct province. Try again.")


screen.exitonclick()
