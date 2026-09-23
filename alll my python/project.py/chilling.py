import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("I Love You ❤️")

# Create turtle
t = turtle.Turtle()
t.speed(3)
t.color("red")

# Draw the heart
t.begin_fill()
t.left(140)
t.forward(180)

t.circle(-90, 200)

t.left(120)
t.circle(-90, 200)

t.forward(180)
t.end_fill()

# Write the message
t.penup()
t.goto(0, -30)
t.color("white")
t.write("SHOW ME YOUR ASSSSSSSSSSSS", align="center", font=("Arial", 24, "bold"))

# Hide turtle
t.hideturtle()

# Keep the window open
turtle.done()