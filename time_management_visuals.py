from tkinter import *
# copy input variables 
Rotor_times= [[7674, 0], [2020, 1], [369, 2], [549, 3], [478, 4], [3168, 8], [2606, 13], [926, 15], [2324, 16], [3697, 20], [887, 21], [2307, 24], [2427, 26], [799, 27], [4740, 30], [3471, 32], [1990, 35], [1401, 37], [1138, 38], [2772, 39], [2906, 41], [2357, 43], [2950, 45], [5537, 49], [3553, 51], [2503, 52], [1528, 53]] 
Arm_times= [[1081, 5], [17165, 6], [15666, 7], [11510, 9], [1875, 10], [1089, 11], [12762, 12], [1101, 14], [1367, 17], [1998, 18], [2493, 19], [11230, 22], [7795, 23], [15808, 25], [24257, 28], [6253, 29], [7458, 31], [1687, 33], [2962, 34], [7910, 36], [12434, 40], [2364, 42], [2935, 44], [4021, 46], [3888, 47], [5548, 48], [13685, 50], [10820, 54]]


to_secs = 1 # change to 1000 once I will start working with miliseconds
ADJUSTED_BAR_GRAPH_SCALE = True # bar grapg wont have the scale of the first graph. Instead biggest value will have the maximal height.

#zpracovani dat
suma = 0
maxi = 0
for item in Arm_times:
    item[0] = item[0]/to_secs
    suma += item[0]
    maxi = max(item[0], maxi)

suma_arm = suma

for item in Rotor_times:
    item[0] = item[0]/to_secs
    suma += item[0]
    maxi = max(item[0], maxi)


# drawing setup
canvas_height = 500
canvas_width  = 2*canvas_height

color = {
    'a' : 'green',
    'r' : 'blue'
}
pie_chart_width = 150
font_height = 16
H = round( 3*canvas_height/4 ,0) # hight of the space in middle of screen that will be actually used for graphs


root = Tk()
C = Canvas(root,
           height=canvas_height, width=canvas_width)

# 100% skladany sloupcovy graf
Y = canvas_height/2 +H/2
X = 50
w = 20
unit = H/suma

R_i = 0
A_i = 0
for i in range(len(Rotor_times + Arm_times)):

    if R_i == len(Rotor_times):
        item = Arm_times[A_i]
        item.append('a')
        A_i += 1 
    elif A_i == len(Arm_times):
        item = Rotor_times[R_i]
        item.append('r')
        R_i += 1 

    elif Rotor_times[R_i][1] < Arm_times[A_i][1]:
        item = Rotor_times[R_i]
        item.append('r')
        R_i += 1 
    else:
        item = Arm_times[A_i]
        item.append('a')
        A_i += 1 

    incr = -item[0]*unit
    C.create_rectangle( X,   Y,
                        X+w, Y + incr,
                       fill = color[ item[2] ],
                    outline = color[ item[2] ])
    Y += incr




# sloupcovy graf
Y = canvas_height/2 +H/2
X = (2*X -w)
gap = 10    
w = (canvas_width - X - pie_chart_width - 2*w)/len(Rotor_times + Arm_times) - gap


unit = H/suma
if ADJUSTED_BAR_GRAPH_SCALE:
    unit = H/maxi

# drawing
R_i = 0
A_i = 0
for i in range(len(Rotor_times + Arm_times)):

    if R_i == len(Rotor_times):
        item = Arm_times[A_i]
        item.append('a')
        A_i += 1 
    elif A_i == len(Arm_times):
        item = Rotor_times[R_i]
        item.append('r')
        R_i += 1 

    elif Rotor_times[R_i][1] < Arm_times[A_i][1]:
        item = Rotor_times[R_i]
        item.append('r')
        R_i += 1 
    else:
        item = Arm_times[A_i]
        item.append('a')
        A_i += 1 

    incr =  item[0]*unit
    C.create_rectangle(
        X,   Y,
        X+w, Y - item[0]*unit,
        fill = color[ item[2] ],
        outline = color[ item[2] ]
    )
    X += w + gap


# pie chart
arm_ratio = suma_arm/suma

mid_x = canvas_width - pie_chart_width/2 - 20
mid_y = canvas_height/2
pie_chart_r = pie_chart_width/2

# one part starts as 100%
C.create_oval(mid_x - pie_chart_r, mid_y - pie_chart_r,
              mid_x + pie_chart_r, mid_y + pie_chart_r,
              fill=color['r'],
              outline=color['r'],
              width=0)

# the other then takes (overshadows) what should be its
C.create_arc(mid_x - pie_chart_r, mid_y - pie_chart_r,
              mid_x + pie_chart_r, mid_y + pie_chart_r,
              start=90,
              extent= 360*arm_ratio,
              fill=color['a'],
              outline=color['a'],
              width=0) 

# doporucena zmena rychlosti + casova rezeva
mid_y = (mid_y + pie_chart_width/2)/2 + canvas_height/2
C.create_text(
    mid_x, mid_y - font_height/2, 
    text="△t=" + str(round(90 - suma,1)), 
    fill="black", 
    font=("Helvetica", font_height),
    anchor="center"
)
C.create_text(
        mid_x, mid_y + font_height/2 + 5, 
        text="v_koef=" + str(round(suma/90,2)), 
        fill="black", 
        font=("Helvetica", font_height),
        anchor="center"
    )

C.create_text(
        mid_x, mid_y + 1.5 * font_height + 5, 
        text="arm", 
        fill=color['a'], 
        font=("Helvetica", font_height),
        anchor="center"
    )
C.pack()
mainloop()
