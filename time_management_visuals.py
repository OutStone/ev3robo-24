from tkinter import *
# copy input variables
Arm_times = [[10,1],[30,3],[11,6]]
Rotor_times = [[15,2],[23,4],[31,5],[5,7]]


to_secs = 1 # change to 1000 once I will start working with miliseconds
ADJUSTED_BAR_GRAPH_SCALE = False # bar grapg wont have the scale of the first graph. Instead biggest value will have the maximal height.

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

    C.create_text(
        X + 0.5*w, Y + gap + font_height, 
        text=str(round(item[0],1)), 
        fill="black", 
        font=("Helvetica", font_height),
        anchor="center"
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

C.pack()
mainloop()
