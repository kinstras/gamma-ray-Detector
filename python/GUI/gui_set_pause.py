from tkinter import *
import pandas as pd
from pandas import DataFrame
import time
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np
import logging
import os
import shutil
from matplotlib.animation import FuncAnimation
from tkinter import messagebox

#global variable
pause = False

class Gui:
    
    
    def __init__(self):
        try:
            
            print("Enter your path of your source folder: ")
            self.source_folder_path = input()
            print("Enter your path of your destination folder: ")
            self.destination_folder_path = input()
            self.setting_gui()
        except KeyboardInterrupt:
            print("Keyboard Interruption")
            self.root.destroy
        finally:
            print("Session Closed")
        
    
    
    def setting_gui(self):
        """
        Sets the main Graphical User Interface with tKinder.
        Returns
        -------
        None.
        """
        self.root = Tk()
        self.root.geometry('1400x900')  
        self.root.title("LISER")  
        Label(self.root, text='LISER Project', font='Arial  15').place(x=0, y=0)
        
        ####### Setting GUI #######
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New')
        filemenu.add_command(label='Open...')
        filemenu.add_command(label='Save as')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.root.quit)
        helpmenu = Menu(menu)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About')
        
        var = StringVar()
        label = Message( self.root, anchor = CENTER, textvariable=var, relief=RAISED, width = 100, cursor = "dot" )

        #var is just a mock-up, we will create a "console window" in order to log-print
        #some messages in right-bottom of GUI
        var.set("Hey!? How are you doing?")
        label.place(x=1000, y=700)

        #Setting one figure and four axes that belongs to it
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(11, 6))
        self.fig.tight_layout(pad=3)

        self.ax1.set(title='Time- Altitude Plot', ylabel='Altidute [m]', xlabel='Time [sec]')
        self.ax2.set(title='Altitude- Pressure Plot', ylabel='Pressure [bar]', xlabel='Altitude [m]')

        self.ax3 = plt.subplot(223,projection ='3d')
        self.ax3.set(title='3d line for altitude', ylabel='Height [m]', xlabel='Time [sec]')

        self.ax4 = plt.subplot(224)
        self.ax4.set(title='Gamma ray spectrum ', ylabel='Events / 1.639 keV', xlabel='Energy [keV]')
        #initialize x & y
        x=[]
        y=[]
        #draw the lines
        (self.line1,) = self.ax1.plot(x,y,'r-')
        (self.line2,) = self.ax2.plot(x,y)

                
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=TOP)
        
        
        # Set Buttons
        self.button_start = Button(self.root, text='Start', font='Arial  15',width=12, fg='green' , command = self.start_session)
        self.button_stop = Button(self.root, text='Stop', font='Arial  15',width=12, fg='red', command=self.askMe)   #self.root.destroy
        self.button_pause = Button(self.root, text='Pause', font='Arial  15',width=12)
        self.button_pause.bind('<Button-1>', self.onPause)
        self.button_screenshot = Button(self.root, text='Screenshot', font='Arial  15',width=12, command = self.screenshot)
        self.button_continue = Button(self.root, text='Continue', font='Arial  15',width=12, command = self.ccontinue)
        self.button_master1 = Button(self.root, text='Master', font='Arial  15',width=12, command = self.master1)
        self.button_batsave= Button(self.root, text='Battery Save', font='Arial  15',width=12,  command = self.battery_save)
        #Placing Buttons
        self.button_start.place(x=100, y=600)
        self.button_screenshot.place(x=300, y=600)
        self.button_pause.place(x=100, y=650)
        self.button_continue.place(x=300, y=650)
        self.button_master1.place(x=100, y=700)
        self.button_batsave.place(x=300, y=700)
        self.button_stop.place(x=500, y=650)
        
        
        mainloop()

    
    
    def askMe(self):
        """
        Creates a pop up window when you press the "stop button"
        and needs confirmation to exit
        Returns
        -------
        None.
        """
        reply = messagebox.askquestion('Confirm exit', 'Do you want to exit ?')
        if reply == 'yes':
            self.root.destroy()
        elif reply == 'no':
            pass
        else:
            messagebox.showwarning('error', 'Something went wrong!')
    
    
    
    def start_session(self):
        """
        Creates an object of FuncAnimation class and calls self.plot() every 1 sec
        Returns
        -------
        None.
        """
        
        self.flag = 0   # flag metavliti gia na mpei MONO MIA FORA stin if sinthiki
        #self.anim_running = True
        self.Myanimation = FuncAnimation(self.fig, self.plot, interval=1000,blit=False)
        print(self.Myanimation)
        print("inside start_session")
        plt.tight_layout()
        self.canvas.draw()

    def onPause(self,event):
        """
        Pause reading txts and takes screenshots, need continue button
        So far only stops the animation
        Returns
        -------
        None.
        """
        #pass
        
        print("on click")
        global pause
        pause ^= True
        #Fig.canvas.mpl_connect('button_press_event', onClick)
        print(pause)
        self.Myanimation.event_source.stop()

        pass
    def screenshot(self):
        """
        Takes screenshots of plots
        """
        pass
    def ccontinue(self):
        """
        Continue the data acquisition
        """
        pass

    def master1(self):
        """
        Triggers arduino to start spectroscopy or stops the first mission
        """
        pass

    def battery_save(self):
        """
        Closes the unnecessary mission
        """
        pass

    def plot(self, i):
        """
        Reads .txt files from "source_folder" and send them in
        "destination_folder", sets values for x&y , and calls update functions
        for each plot
        Returns
        -------
        None.
        """
        try:
         
            list = sorted(os.listdir(self.source_folder_path) , key = lambda x: int(os.path.splitext(x)[0]))  #sort by number due to lambda function
            print(list[0])              #pairno to proto stoixeio
            source = self.source_folder_path + '/' + list[0]
            
            self.df = pd.read_fwf(source, header=None)      #to txt to metatrepo se dataframe
            self.df_spectrum = pd.read_fwf(source, header=None) 
            self.df.dropna(axis='columns')               #petao ta null values
            self.df_spectrum.dropna(axis='columns')
            # Remove all columns between column index 1 to 3
            
            self.df_spectrum.drop(self.df_spectrum.iloc[:, 0:16], inplace = True, axis = 1)
            
            print(self.df_spectrum)
            #self.df = self.df[[9,10,11]]
            #print("Arxiko dataframe: " ,self.df)
            if self.flag == 0:
                self.df_first_mission = self.df             #to df_sum itan adeio kai to gemizoume me tis times tou df
                self.df_sum = self.df_spectrum
                
                self.flag = 1
                print("mesa stin if",self.df_sum)
            else: 
                self.df_first_mission = self.df_first_mission.append(self.df, ignore_index=True)
                self.df_sum = self.df_sum.add(self.df_spectrum, fill_value=0)
                print("inside else")
            
            #proergasia gia spectrum
            columns = self.df_sum.shape[1]
            array = np.array(self.df_sum)
            array.resize(1,columns) #kanw resize ton array se (1,12)
            #total_counts = np.sum(array) #vrisko sinoliko arithmo counts 
            #print("Total counts: ",total_counts)
            cps_list = array[0].tolist()  #metatrepo to array se lista
            energy_list = np.arange(0, 5, 1)

            #print(cps_list)

            #move file to destination_folder
            shutil.move(source,self.destination_folder_path)
            
            x1 = self.df_first_mission[5]
            y1 = self.df_first_mission[9]
            
            x2 = self.df_first_mission[9]
            y2 = self.df_first_mission[10]

            x3 = self.df_first_mission[7]
            y3 = self.df_first_mission[8]
            z3 = self.df_first_mission[9]

            plt.cla()
            #call plot function
            self.refreshPlot1(x1,y1)
            self.refreshPlot2(x2,y2)
            self.refresh3dPlot(x3,y3,z3)
            self.refreshSpectrum(energy_list,cps_list)
            plt.tight_layout()
            
        except IndexError:
                print("File not found.")
        
        
        
    def refreshPlot1(self,x,y):
        """
        Parses data to line1 and re-arrange axes
        Returns
        -------
        None.
        """
        self.line1.set_data(x,y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())        
        self.canvas.draw()
        
    def refreshPlot2(self,x,y):
        """
        Parses data to line2 and re-arrange axes
        Returns
        -------
        None.
        """
        self.line2.set_data(x,y)
        ax = self.canvas.figure.axes[1]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())        
        self.canvas.draw()
        
    def refresh3dPlot(self,x,y,z):
        """
        Parses data to line3 and plot a 3d model
        Returns
        -------
        None.
        """
        self.ax3.plot3D(x, y, z)[2]
        self.canvas.draw()

    def refreshSpectrum(self,x,y):
        """
        Parses data to spectrum and plot a histogram that
        represent the gamma-ray spectroscopy
        Returns
        -------
        None.
        """
        self.ax4.bar(x,y, color='blue', width=0.1)
        self.canvas.draw()


obj = Gui()

