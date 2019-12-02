import turtle
import time


def test():
    # t.fillcolor('red')
    t.hideturtle()
    t.left(45)
    for _ in range(2):
        for _ in range(4):
            t.forward(100)
            t.right(90)
        t.right(180)


def twistline():
    t.speed(20)
    t.pensize(2)
    turtle.bgcolor("black")
    colors = ["red", "yellow", "purple", "blue"]  # 设置四种颜色，你可以自己修改
    # t.tracer(False)
    for x in range(400):
        t.forward(2*x)  # 每次画的长度是变量x的2倍
        t.color(colors[x % 4])  # 改变颜色
        t.left(91)  # 逆时针旋转91度形成交叉螺旋
    # t.tracer(True)


def pentagram():
    # 设置画笔
    t.pensize(5)
    t.pencolor("yellow")
    t.fillcolor("red")

    # 开始画五角星并填充
    t.begin_fill()
    for _ in range(5):
        t.forward(200)
        t.right(144)
    t.end_fill()

    time.sleep(2)  # 等待2秒
    # 开始签名
    t.penup()  # 抬起画笔,用于另起一个地方绘制
    t.goto(150, -160)  # 移动到指定位置
    t.color("violet")  # 设置颜色
    t.write("大猫 2019", font=('Arial', 20, 'normal'))  # 写文本Done


def drawsnake(rad, angle, len, neckrad):
    for _ in range(len):  # 画弧线，弯曲的蛇身
        t.circle(rad, angle)
        t.circle(-rad, angle)
        t.circle(rad, angle / 2)

    t.forward(rad / 2)  # 直线前进
    t.circle(neckrad, 180)  # 回头
    t.forward(rad / 4)  # 直线前进


def snake():
    turtle.setup(1500, 1400, 0, 0)
    t.pensize(30)  # 画笔尺寸
    t.pencolor("green")
    t.seth(-40)    # 前进的方向
    drawsnake(70, 80, 2, 15)


def sunflower():
    # t.penup()  # 抬起画笔,用于另起一个地方绘制
    t.goto(-100, 0)  # 移动到指定位置
    # t.color("violet")  # 设置颜色
    # 设置画笔
    t.pensize(1)
    t.speed(10)
    t.pencolor("yellow")
    t.fillcolor("red")
    t.begin_fill()
    for _ in range(24):
        t.forward(200)
        t.right(165)
    t.end_fill()


def drawcircle():
    t.pensize(3)
    t.color('yellow')

    t.up()
    t.goto(-100, 50)
    t.down()

    for x in range(5):
        if x == 3:
            t.circle(100, 180)
        t.left(90)
        t.circle(100)


def fivecircles():
    t.pensize(3)
    t.color('yellow', 'red')
    t.begin_fill()

    t.up()
    t.forward(200)
    t.down()
    t.circle(100)

    t.up()
    t.backward(200)
    t.down()
    t.right(90)
    t.circle(100)

    # t.up()
    t.left(90)
    # t.down()
    t.circle(100)

    t.up()
    t.backward(200)
    t.down()
    t.right(90)
    t.circle(100)

    t.left(90)
    t.circle(100)

    t.end_fill()
    turtle.done()


def square():
    turtle.reset()
    a = 60
    turtle.fillcolor("red")
    turtle.pencolor("blue")
    turtle.pensize(10)
    turtle.begin_fill()
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    turtle.end_fill()


def main():
    global t
    t = turtle.Turtle()
    # test()
    # t.reset()
    # pentagram()
    # t.reset()
    # twistline()
    t.reset()
    square()
    turtle.done()
    # time.sleep(10)


if __name__ == "__main__":
    main()
