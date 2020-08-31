#!/usr/bin/env python3
import PySimpleGUI as sg
import pandas as pd
import os.path
import datetime
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import matplotlib.dates as mdates

days_month = [31,28,31,30,31,30,31,31,30,31,30,31]

def Hour():
    return datetime.datetime.now().strftime("%H:%M")

def Data():
    return datetime.datetime.now().strftime("%d/%m/%Y")


def fSp(stringa, n):
    l = len(stringa)
    l1=(n-l)//2
    l2=n-l-l1
    return ' '*(l1)+stringa+' '*(l2)


def dateToSec(date):
    date_v = date.split('/')
    return (int(date_v[0])+ days_month[int(date_v[1])])*86400

def hourToSec(hour):
    hour_v = hour.split(':')
    return int(hour_v[0])*3600 + int(hour_v[1])*60



class autoLayout:
    def __init__(self, screen_h, screen_w, key_core):
        self.screen_h = screen_h
        self.screen_w = screen_w
        self.key_core = key_core
        self.layout = []
        # menu var
        self.menu = []
        # graph variable
        self.graph=[]
        self.canvas_key = '-canvas_'+key_core+'-'
        self.radiox_keys = {}
        self.radioy_keys = {}
        self.x_plot=''
        self.y_plot=''
        self.time_names=[]
        # table variable
        self.table=[]
        self_table_obj =[]
        # frame variable
        self.frame_graph_key = ''
        self.frame_graph_key = ''
        # csv
        self.filename = key_core+'.csv' 

    def layoutMenu(self, menu_def):
        self.menu = [sg.Menu(menu_def, tearoff=True)]
        return self.menu

    def layoutTable(self, top_text, table_header, 
                    table_header_input_default, table_header_input_size):
        # top_text is the text write at the top of the block
        # table header is the list of field to fill in input
        # tbale_header_input_default is the default value of input field
        # table_header_input_size is the length in word of the input field
        self.table_header_input_size = table_header_input_size
        self.table_header = table_header
        self.csvLayout( extract=False)
        self.table = [ [sg.Text(top_text)],
                        [sg.Text(name, 
                                size = (table_header_input_size,1)
                                ) for name in table_header],
                        [sg.InputText(size = (table_header_input_size,1),
                                key = 'table_'+self.headerToKey( name ),
                                default_text= def_text)
                                for (name,def_text) 
                                in zip(table_header, table_header_input_default)],
                        [self.table_obj],
                        [sg.Submit(), sg.Cancel()]
                       ]    
        return self.table

    def layoutGraph(self, top_text, time_names=[], radiox_list=[], radioy_list=[]):
            # top_text is the top text of graph
            self.time_names=time_names
            self.canvas_key = '-canvas_'+self.key_core+'-'
            self.graph = [ [sg.Text(top_text)],
                  [sg.Canvas(size=(self.screen_w/2-self.screen_w//10, self.screen_h),
                      key=self.canvas_key)]
                  ]

            if len(radioy_list) != 0:
                ly = [sg.Text('Settare asse y: ')]
                default1=True
                for y in radioy_list:
                    self.radioy_keys[y] = '-RADIO_'+self.key_core+'_'+y.upper()+'_Y-'
                    ly.append( sg.Radio(y,'radioy',
                                        key=self.radioy_keys[y],
                                        default=default1, enable_events=True))
                    default1=False
                self.graph.append(ly)

            if len(radiox_list) != 0:
                lx = [sg.Text('Settare asse x: ')]
                default1=True
                for x in radiox_list:
                    self.radiox_keys[x] = '-RADIO_'+self.key_core+'_'+x.upper()+'_X-'
                    lx.append( sg.Radio(x,'radiox',
                                        key=self.radiox_keys[x],
                                        default=default1, enable_events=True))
                    default1=False
                self.graph.append(lx)
            return self.graph
            
    def layoutCreate(self, frame_graph_title, frame_table_title):
        if len(self.graph)== 0 or len(self.table)==0:
            print("Error table or graph not setted")
            exit(1)
        self.frame_graph_key = '-COL1_'+self.key_core+'-'
        self.frame_table_key = '-COL2_'+self.key_core+'-'

        frame_graph = sg.Column( [[ 
                        sg.Frame( frame_graph_title, [[
                            sg.Column(self.graph, 
                                      key = self.frame_graph_key,
                                      visible=True)
                            ]])
                        ]])
        frame_table = sg.Column( [[ 
                        sg.Frame( frame_table_title, [[
                            sg.Column(self.table, 
                                      key = self.frame_table_key,
                                      visible=True)
                            ]])
                        ]])
        self.layout  = [ self.menu,
                         [ frame_graph, frame_table ]
                       ]
        return self.layout

    def openWindow(self, name, on_top):
        self.window = sg.Window(name, self.layout, 
                            finalize=True, 
                            size=(self.screen_w, self.screen_h),
                            location=(0,0),
                            keep_on_top=on_top)
        self.window.Finalize()

    ##### Routine ##################################################
    def routine(self, event, values):
        if 'Submit' in event:
            self.saveAndUpdateTable(values)
        elif 'Cancel' in event:
            self.deleteLine()
            self.csvData()
            self.uploadTable()
        for ev in self.radiox_keys:
            if self.readiox_keys[ev] in event:
                self.x_plot = ev
                break
        else:
            for ev in self.radioy_keys:
                if self.readioy_keys[ev] in event:
                    self.y_plot = ev
                    break
        self.updateGraph()


    def read(self):
        return self.window.read()
    def close(self):
        return self.window.close()

    ##### TABLE function #################################################
    def csvLayout(self,  extract=True):
            if extract:
                csvData()
            else:
                self.data=[['0' for i in self.table_header]]

            lenmax=0
            for i in self.data:
                if lenmax<len(i):
                    lenmax=len(i)


            self.table_obj = [sg.Table(values=self.data,
                  headings=[ fSp(f,self.table_header_input_size) 
                      for f in self.table_header],
                  max_col_width=lenmax+10,
                  display_row_numbers=False,
                  auto_size_columns=True,
                  justification = 'center',
                  row_height=20,
                  background_color= sg.BLUES[2],
                  text_color=sg.YELLOWS[1],
                  alternating_row_color=sg.BLUES[1],
                  num_rows=min(20, len(self.data)),
                  key='table_'+self.key_core)]
    
    def csvData(self):
        if os.path.isfile(self.filename):
            df = pd.read_csv(self.filename, sep=';', engine='python', header=None)
            self.data = df.values.tolist()
            # Uses the first row (which should be column names) as columns names
            self.table_header = [var.replace('_',' ') for var in df.iloc[0].tolist()]
            # Drops the first row in the table i
            # (otherwise the header names and the first row will be the same)
            self.data = df[1:].values.tolist()
        else:
            self.data=[]
            self.table_header=[]



    def saveAndUpdateTable(self, values):
            ###  Writing data in csv file
            line = ''
            line_v=[]
            # creo la linea da aggiungere
            for val in [self.headerToKey(h) for h in self.table_header]:
                    line_v.append(str(values['table_'+val]))
            line = ';'.join(line_v)+'\n'

            # Nel caso in cui il file non esista lo creo ed aggiungo l'intestazione
            if not os.path.isfile(self.filename):
                title = ';'.join([self.headerToPar(h) for h in self.table_header])+'\n'
                with open(self.filename,'w') as fp:
                    fp.write(title)
                    fp.write(line)
            else:
                with open(self.filename,'a') as fp:
                    fp.write(line)
            fp.close()
            self.csvData()
            self.uploadTable()
    
    def uploadTable(self):
            self.window.Element('table_'+elf.key_core).Update(
                    values= self.data, num_rows=min(len(self.data),20))

    def deleteLine(self, table_line):
        if len(table_line) != 0:
            with open(self.filename, "r") as f:
                lines = f.readlines()
            cnt=0
            with open(self.filename, "w") as f:
                for line in lines:
                    if cnt != table_line[0]+1:
                        f.write(line)
                    cnt+=1    

    ##### GRAPH function #################################################
    def createGraph(self):
        fig = Figure()

        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid()

        canvas_elem = window[self.canvas_key]
        graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
        canvas = canvas_elem.TKCanvas
        self.fig_agg = self.draw_figure(canvas, fig)

    def draw_figure(self, canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


    def updateGraph(self):
        if len(self.data)!=0:
            if self.x_name == 'time':
                x_i = self.table_header.index(self.time_names[0])
                x2_i = self.table_header.index(self.time_names[1])
            else:
                x_i = self.table_header.index(self.x_name)
            y_i = self.table_header.index(self.y_name)
            x=[]
            y=[]
            for line in self.data:
                if x_name == 'time':
                    x.append( float(dateToSec(line[x_i])+ hourToSec(line[x2_i])))
                else:
                    x.append( float(line[x_i]))
                y.append(float(line[y_i]))

        self.ax.cla()                    # clear the subplot
        self.ax.grid()                   # draw the grid
        self.ax.plot(x, y,  color='purple')
        self.fig_agg.draw()

    ### various
    def headerToPar(self,header):
        return header.replace(' ','_')

    def headerToKey(self,header):
        return self.key_core+'_'+self.headerToPar(header)


                                            

