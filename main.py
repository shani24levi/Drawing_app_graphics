# This program create ship and give the option to move it on screen
""""**********************************************
    *  Student 1 :  Shani Levi     ID: 302853619
    *  Student 2 :  Idan Kario     ID: 300853751
    *  Student 3 :  Mhmd atamny    ID: 207887720

**********************************************"""

# Import Libraries
import numpy as np
from tkinter import Tk, Canvas, Frame, Label, OptionMenu, Button, StringVar, IntVar
from tkinter import Tk, Canvas, messagebox, Frame, Label, OptionMenu, Button, StringVar, IntVar
from tkinter_custom_button import TkinterCustomButton
from tkinter import colorchooser
from PIL import Image, ImageTk
from collections import namedtuple
from math import sin, cos, radians
import math
import threading 
#for open file
import json
from tkinter import filedialog 
import os

class DrowingApp:
    data,fileOpend,my_point,x,y={} ,"",0,0,0
    #Constructor __init__
    def __init__(self, master,WIDTH=1100, HEIGHT=800):
        master.title("GUI HW2 By Shani & Idan & mhmd ")
        self.my_color = "Black"
        self.create_canvas(master, WIDTH, HEIGHT)
        master.attributes("-transparentcolor", "red")
        self.create_upper_menu()
        # lower section
        self.lower_frame = Canvas(self.master, bg='#c9daf8', bd=5)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
        self.lower_frame.bind("<ButtonPress-1>", self.moveEvent)
        self.reset()
     
     # resize image by canvas size
    def resizeimage(self, event):
        image = self.image_copy.resize((self.master.winfo_width(), self.master.winfo_height()))
        self.image1 = ImageTk.PhotoImage(image)
        self.label.config(image=self.image1)
    def loadbackground(self):
        self.label = Label(self.canvas, image=self.background)
        self.label.bind('<Configure>', self.resizeimage)
        self.label.pack(fill='both', expand='yes')

    def rootgeometry(self, WIDTH, HEIGHT):
        self.master.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    #Create Ship from data get from file 
    def createShip(self,lines,circels,bezier):
        #Process work simultany
        thread_list = []
        for  line in lines:
            thread=threading.Thread(target=self.myLine, args=(line[0],line[1],line[2],line[3]))
            thread_list.append(thread) 
        for  circle in circels:
            thread=threading.Thread(target=self.myCircle, args=(circle[0],circle[1],circle[2],circle[3]))
            thread_list.append(thread) 
        thread=threading.Thread(target=self.myCurve, args=(bezier[0],bezier[1],bezier[2],bezier[3],bezier[4],bezier[5],bezier[6],bezier[7]))
        thread_list.append(thread) 
        for thread in thread_list:
            thread.start()

    def create_upper_menu(self):
        # Uper section 1
        frame = Frame(self.master, bg='#a0dbd1', bd=4)
        frame.place(relx=0.5, rely=0.04, relwidth=0.80, relheight=0.1, anchor='n')
        # Open jason file
        openfile = TkinterCustomButton(master=frame, height=52, text="Open File", command=self.openfile)
        openfile.place(relx=0)
        # Derivative
        derivative = TkinterCustomButton(master=frame, height=52, text="cutting",command=self.derived)
        derivative.place(relx=0.20)
        # Reset by defult/user file if he upload file
        reset = TkinterCustomButton(master=frame, height=52, text="Reset", command=self.reset)
        reset.place(relx=0.40)
        # Help give the option to open help file to get all information abount function
        helps = TkinterCustomButton(master=frame, height=52, text="Help", command=self.helpf)
        helps.place(relx=0.60)
        rotate = TkinterCustomButton(master=frame, height=52, text="rotate", command=self.rotate)
        rotate.place(relx=0.80)

        # Uper section 2
        frame2 = Frame(self.master, bg='#a0dbd1', bd=4)
        frame2.place(relx=0.5, rely=0.15, relwidth=0.8, relheight=0.1, anchor='n')
        # Move to current position
        move = TkinterCustomButton(master=frame2, height=52, text="Move", command=self.move)
        move.place(relx=0)
        # zoomIn
        zoomIn = TkinterCustomButton(master=frame2, height=52, text="zoomIn +", command=self.zoomIn)
        zoomIn.place(relx=0)
        # zoomOut
        zoomOut = TkinterCustomButton(master=frame2, height=52, text="zoomOut -", command=self.zoomOut)
        zoomOut.place(relx=0.20)
        MirorX = TkinterCustomButton(master=frame2, height=52, text="Miror to X", command=self.mirrorX)
        MirorX.place(relx=0.40)
        MirorY = TkinterCustomButton(master=frame2, height=52, text="Miror to Y", command=self.mirrory)
        MirorY.place(relx=0.60)
        MirrorXY = TkinterCustomButton(master=frame2, height=52, text="Miror to XY", command=self.mirrorXY)
        MirrorXY.place(relx=0.80)
        
     # Open file if dont find any will drop massage
    def openfile(self):
        self.action ='openfile'
        tf = filedialog. askopenfilename(initialdir="../Path/For/JSON_file",
                                        filetypes=((".json", "*.json"), ("All Files", "*.*")),
                                        title="Choose a file.")
        try:
            if tf:
                with open(tf) as f:
                    self.data = json.load(f)
                    self.fileOpend = f          
                self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
            elif tf=='':
                messagebox.showinfo("cencel", "file not selcted")
        except IOError:
            messagebox.showinfo("Error", "erorr")
    # Upload last file and create ship from screatch
    def reset(self):
        self.action="reset"
        if self.fileOpend == "":
            with open('./ship.json') as f:
                self.data = json.load(f)  
        else:    
            with open(self.fileOpend) as f:
                self.lower_frame.delete("all")
                self.data = json.load(f)  
        self.lower_frame.delete("all")
        self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
    # create_canvas with all atributes
    def create_canvas(self, master, WIDTH, HEIGHT):
        self.master = master
        self.rootgeometry(WIDTH, HEIGHT)
        self.canvas = Canvas(self.master)
        self.canvas.pack()
        self.background_image = Image.open('bg.PNG')
        self.image_copy = self.background_image.copy()
        self.background = ImageTk.PhotoImage(self.background_image)
        self.loadbackground()
    # Put pixel on gui by cordinat
    def putPixel(self, x_, y_):
        self.lower_frame.create_line(x_, y_, x_ + 1, y_ + 1, fill=self.my_color)

    # Bersenheim
    def myLine(self,x1,y1,x2,y2):
        #Bresenham's Line Algorithm
        # Determine how steep the line is
        direction =abs(y2-y1)> abs(x2-x1)
        if direction:
            x1, y1,x2, y2 = y1, x1,  y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        errp = 2*dx 
        direcx=1 if x2-x1>=0 else -1
        direcy=1 if y2-y1>=0 else -1
        # Iterate over bounding box generating points between start and end
        y,x = int(y1),int(x1)
        steps=int(max(dx,dy))
        for i in range(steps):
            self.putPixel(y,x) if direction else self.putPixel(x,y)
            errp -= 2*abs(dy)
            if errp < 0:
                y += direcy
                errp += 2*abs(dx)
            x+=direcx    
    # Plot Circle
    def plotCirclePoints(self, xc, yc, x, y):
        self.putPixel(xc + x, yc + y)
        self.putPixel(xc - x, yc + y)
        self.putPixel(xc + x, yc - y)
        self.putPixel(xc - x, yc - y)
        self.putPixel(xc + y, yc + x)
        self.putPixel(xc - y, yc + x)
        self.putPixel(xc + y, yc - x)
        self.putPixel(xc - y, yc - x)
    # Create Circle
    def myCircle(self, xc,yc,x2,y2):
        radius= math.sqrt( (x2 - xc)**2 + (y2 - yc)**2 )
        "Bresenham complete circle algorithm in Python"
        p = 3 - (2 * radius)
        x = 0
        y = radius
        while x < y:
            self.plotCirclePoints(xc,yc,x,y)
            if p < 0:
                p = p + (4 * x) + 6
            else:
                self.plotCirclePoints(xc,yc,x,y)
                p = p + (4 * (x - y)) + 10
                y -=1
            x+=1
        if(x==y):
            self.plotCirclePoints(xc,yc,x,y)
     # bezier for cruve
    def bezier(self, x1, x2, x3, x4, t):
        ax = -x1 + 3 * x2 - 3 * x3 + x4
        bx = 3 * x1 - 6 * x2 + 3 * x3
        cx = -3 * x1 + 3 * x2
        dx = x1
        res = ax * t ** 3 + bx * t ** 2 + cx * t + dx
        return int(res)

    def myCurve(self, x1,y1,x2,y2,x3,y3,x4,y4):        
        xt1 = x1
        yt1 = y1
        path_resolution=1000
        for t in range(0, path_resolution + 1):
            pointx = self.bezier(x1, x2, x3, x4, t / path_resolution)
            pointy = self.bezier(y1, y2, y3, y4, t / path_resolution)
            self.myLine(xt1, yt1, pointx, pointy)
            xt1 = pointx
            yt1 = pointy
        return
   


    def zoomToFile(self,shape,zoom):
        if(zoom):
            for i in range(len(shape)):
                if i % 2 == 0:
                    shape[i] =int(1.1*shape[i])
                else:
                    shape[i] =int(1.1*shape[i])
        else:          
            for i in range(len(shape)):
                if i % 2 == 0:
                    shape[i] =int(0.9*shape[i])
                else:
                    shape[i] =int(0.9*shape[i])
    # Help file
    def helpf(self):
        self.action="helpf"
        os.system('help.pdf')

    def zoomIn(self):
        self.action="zoomIn"
        self.lower_frame.delete("all")
        x,y= self.data["lines"][0][0],self.data["lines"][0][1]
        self.moveTo(0,0)
        for  line in self.data["lines"]:
            self.zoomToFile(line,1)
        for  circle in self.data["circles"]:
            self.zoomToFile(circle,1)
        self.zoomToFile(self.data["bezier"],1)
        self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
        self.moveTo(x,y)
    def zoomOut(self):
        self.action="zoomOut"
        x,y= self.data["lines"][0][0],self.data["lines"][0][1]
        self.moveTo(0,0)
        self.lower_frame.delete("all")
        for  line in self.data["lines"]:
            self.zoomToFile(line,0)
        for  circle in self.data["circles"]:
            self.zoomToFile(circle,0)
        self.zoomToFile(self.data["bezier"],0)
        self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
        self.moveTo(x,y)



    def moveShape(self,shape,stepx,stepy):
        for i in range(len(shape)):
                if i % 2 == 0:
                    shape[i] +=stepx
                else:
                    shape[i] +=stepy
               
    def moveTo(self, x,y,move=0):
        if(self.action=='move'or move):
            # Get first x,y
            self.x = x
            self.y = y
            #clear
            self.lower_frame.delete("all")
            #set new ship
            stepx= x-self.data["lines"][0][0]
            stepy= y-self.data["lines"][0][1]
            for line in self.data["lines"]:
                self.moveShape(line,stepx,stepy)
            for  circle in self.data["circles"]:
                self.moveShape(circle,stepx,stepy)
            self.moveShape(self.data["bezier"],stepx,stepy)
            self.createShip( self.data['lines'],self.data['circles'],self.data['bezier']) 
    def moveEvent(self,event):
        self.moveTo(event.x,event.y)
    def move(self):
        #lisinigs for click
        self.action ='move'
    def derivedShape(self,shape,derive):
        for i in range(len(shape)):
            if i % 2 == 0:
                shape[i]=  shape[i] +shape[i+1]*derive
        
    def derived(self):
        self.action="derived"
        self.lower_frame.delete("all")
        for  line in self.data["lines"]:
            self.derivedShape(line,0.1)
        for  circle in self.data["circles"]:
            self.derivedShape(circle,0.1)
        self.derivedShape(self.data["bezier"],0.1)
        self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
  
    def myMirror(self,shape ,mirror):
        for i in range(len(shape)):
            if i % 2 == 0:
                [x,y,d] =  np.array([shape[i] , shape[i+1],1] )*  np.array(mirror)
                shape[i],shape[i+1]=x[0],y[1]
    def mirrorfunc(self,mirrorP):
      
        self.lower_frame.delete("all")
        for  line in self.data["lines"]:
            self.myMirror(line,mirrorP)
        for  circle in self.data["circles"]:
            self.myMirror(circle,mirrorP)
        self.myMirror(self.data["bezier"],mirrorP)
        
    def mirrorXY(self):
        x,y= self.data["lines"][0][2],self.data["lines"][0][3]
        mirrorP = [[-1,0,0],[0,-1,0],[0,0,1]]
        self.mirrorfunc(mirrorP)
        self.moveTo(x,y,1)

    # rotation logic
    def mirrorX(self):
        x,y= self.data["lines"][0][0],self.data["lines"][0][1]
        mirrorP = [[1,0,0],[0,-1,0],[0,0,1]]
        self.mirrorfunc(mirrorP) 
        self.moveTo(x,y,1)
        # rotation logic

    def mirrory(self):
        x,y= self.data["lines"][0][2],self.data["lines"][0][3]
        mirrorP =[[-1,0,0],[0,1,0],[0,0,1]]
        self.mirrorfunc(mirrorP) 
        self.moveTo(x,y,1)

    def rotateShape(self,shape,angle=45):
        for i in range(len(shape)):
            if i % 2 == 0:
                x,y=shape[i],shape[i+1]
                shape[i] = int(x * cos(angle) - y * sin(angle))
                shape[i+1] = int(y * cos(angle) + x * sin(angle))

    
    # rotate 
    def rotate(self):
        self.action ='rotate'
        self.lower_frame.delete("all")
        x,y= self.data["lines"][8][2],self.data["lines"][8][3]
        self.moveTo(0,0)
        for  line in self.data["lines"]:
            self.rotateShape(line)
        for  circle in self.data["circles"]:
            self.rotateShape(circle)
        self.rotateShape(self.data["bezier"])
        self.moveTo(x,y,1)
        self.createShip( self.data['lines'],self.data['circles'],self.data['bezier'])
       

if __name__ == '__main__':
    root = Tk()
    my_gui = DrowingApp(root)
    root.mainloop()

