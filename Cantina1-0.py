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

fig = Figure()

ax = fig.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()

COL_S=10
HEIGHT=1000
WIDTH=1300

days_month = [31,28,31,30,31,30,31,31,30,31,30,31]

# Function #
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


def csvData(filename):
        if os.path.isfile(filename+'.csv'):
            df = pd.read_csv(filename+'.csv', sep=';', engine='python', header=None)
            data = df.values.tolist()
            # Uses the first row (which should be column names) as columns names
            header_list = df.iloc[0].tolist()
            # Drops the first row in the table (otherwise the header names and the first row will be the same)
            data = df[1:].values.tolist()
        else:
            data=[]
            header_list=[]
        return [data, header_list]

def csvLayout(filename, extract=True, header=[]):
            if extract:
                [data, header_list] = csvData(filename)
            else:
                data=[['0' for i in header]]
                header_list = header


            table = [sg.Table(values=data,
                  headings=[ fSp(f,COL_S) for f in header_list],
                  max_col_width=20,  
                  display_row_numbers=False,
                  auto_size_columns=True,
                  justification = 'center',
                  row_height=20,
                  background_color= sg.BLUES[2],
                  text_color=sg.YELLOWS[1],
                  alternating_row_color=sg.BLUES[1],
                  num_rows=min(20, len(data)),
                  key='table_'+filename)]
            return table
        

def maturazioneSaveAndUpdateTable(values, ID, vigneto, dati):
            ###  Writing data in csv file
            filename = ID+'.csv'
            line = ''
            line_v=[]
            # creo la linea da aggiungere
            for val in ['maturazione_'+vigneto+'_'+d.replace(' ','_') for d in dati]:
                    line_v.append(str(values[val]))
            line = ';'.join(line_v)+'\n' 

            # Nel caso in cui il file non esista lo creo ed aggiungo l'intestazione
            if not os.path.isfile(filename):
                title = ';'.join([name.replace(' ','_') for name in dati])+'\n'
                with open(filename,'w') as fp:
                    fp.write(title)
                    fp.write(line)
            else:
                with open(filename,'a') as fp:
                    fp.write(line)
            fp.close()
            uploadTable(ID)

def SaveAndUpdateTable(values, ID, value_begin,  dati):
            ###  Writing data in csv file
            filename = ID+'.csv'
            line = ''
            line_v=[]
            # creo la linea da aggiungere
            for val in [value_begin+'_'+d.replace(' ','_') for d in dati]:
                    line_v.append(str(values[val]))
            line = ';'.join(line_v)+'\n' 

            # Nel caso in cui il file non esista lo creo ed aggiungo l'intestazione
            if not os.path.isfile(filename):
                title = ';'.join([name.replace(' ','_') for name in dati])+'\n'
                with open(filename,'w') as fp:
                    fp.write(title)
                    fp.write(line)
            else:
                with open(filename,'a') as fp:
                    fp.write(line)
            fp.close()
            uploadTable(ID)

def DeleteLine(filename, table_line):
    if len(table_line) != 0:
        with open(filename+'.csv', "r") as f:
            lines = f.readlines()
        cnt=0
        with open(filename+'.csv', "w") as f:
            for line in lines:
                if cnt != table_line[0]+1:
                    f.write(line)
                cnt+=1


def uploadTable(ID):
        [data, header_list]  = csvData(ID)
        window.Element('table_'+ID).Update(
                values= data, num_rows=min(len(data),20))

def updateGraphTable(ID,x_name ,y_name, time_names=[]):
        [data, header_list]  = csvData(ID)
        if x_name == 'time':
            x_i = header_list.index(time_names[0])
            x2_i = header_list.index(time_names[1])
        else:
            x_i = header_list.index(x_name)
        y_i = header_list.index(y_name)
        x=[]
        y=[]
        for line in data:
            if x_name == 'time':
                x.append( float(dateToSec(line[x_i])+ hourToSec(line[x2_i])))
            else:
                x.append( float(line[x_i]))    
            y.append(float(line[y_i]))

        updateGraph(x, y)
        window.Element('table_'+ID).Update(
                values= data, num_rows=min(len(data),20))

            

def updateGraph(x, y):
        ax.cla()                    # clear the subplot
        ax.grid()                   # draw the grid
        #years = mdates.YearLocator()   # every year
        #months = mdates.MonthLocator()  # every month
        #days = mdates.DayLocator()  # every month
        #fmt = mdates.DateFormatter('%D/%M/%Y')
        ax.plot(x, y,  color='purple')
        #ax.xaxis.set_major_locator(days)
        #ax.xaxis.set_major_formatter(fmt)
        #ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        #ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        fig_agg.draw()

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



# ------ Menu Definition ------ #
vitigni = ['CorteseA1', 'CorteseA2', 'BarberaA2', 'DolcettoA2']
vini_vitigni = ['Cortese', ['CorteseA1', 'CorteseA2'],'Barbera', ['BarberaA2'], 'Dolcetto',['DolcettoA2']]
vini = ['Cortese', 'Barbera', 'Dolcetto']

maturazione_vitigni = [ v+'::maturazione_'+v for v in vitigni]
maturazione_dati =  [ 'Data', 'Ora raccolta',  'T Esterna', 'T Uva' ,'T Mosto', 'Babo']
maturazione_dati_default = [Data(), Hour(), '0', '0', '0', '0']

raccolta_vini = [ v+'::raccolta_'+v for v in vini]
raccolta_dati = [ 'Data', 'Ora inizio raccolta', 'Ora fine raccolta','Ora fine sgranatura', 'T Uva', 'T Mosto','Kg Uva', 'Hl mosto' , 'Babo']

fermentazioni_vini = [ v+'::fermentazioni_'+v for v in vini]
fermentazioni_dati_babo = ['Data', 'Ora', 'Babo', 'Temperatura']
fermentazioni_dati_rimontaggi = ['Data', 'Ora', 'Rimontaggi ore On', 'Rimontaggi ore Off', 'Posizione pompa']
fermentazioni_dati_vasca = ['Data', 'Ora', 'Vasca']

gf_perdite_dati = ['Data', 'Ora misura', 'T accumolo', 'Bar accumolo']
gf_perdite_dati_default = [Data(), Hour(), '0','0']

menu_def = [['Vendemmia', 
                ['Maturazione',
                    maturazione_vitigni, 
                 'Raccolta', 
                    raccolta_vini, 
                 'Fermentazioni',
                    fermentazioni_vini,
                ]
            ],
            ['Gruppo frigo',
                ['Perdite circuito::GF_perdite',
                  'Chiller::GF_chiller'      
                    ]
                ],
            ['Impostazioni', ['Vitigni', 'Vini'] ],
            ['&Help', '&About...'], 
             ]

# ----------- Create the 3 layouts this Window will display -----------
layout_maturazione_csv = [ [ 
                        [sg.Text('Prova di maturazione del vitigno '+v)],
                        [sg.Text(name, size = (COL_S-2,1)) for name in maturazione_dati],
                        [sg.InputText(size = (COL_S-2,1), 
                            key = 'maturazione_'+v+'_'+name.replace(' ','_'),
                            default_text= def_text) 
                            for (name,def_text) in zip(maturazione_dati, maturazione_dati_default)],
                        csvLayout('maturazione_'+v, extract=False, header=[m.replace(' ','_') for m in maturazione_dati]),
                        [sg.Submit(), sg.Cancel()]
                      ] for v in vitigni ]

layout_GF_Perdite = [ [sg.Text('Perdite del circuito da 1000lt presente in cantina')],
                      [sg.Text(name, size = (COL_S-2,1)) for name in gf_perdite_dati],
                      [ sg.InputText(size = (COL_S-2,1),
                          key='GF_perdite_'+name.replace(' ','_'),
                          default_text=def_text)
                          for (def_text, name) in zip(gf_perdite_dati_default, gf_perdite_dati)],
                        csvLayout('GF_perdite', extract=False, header=[m.replace(' ','_') for m in gf_perdite_dati]),
                        [sg.Submit(), sg.Cancel()]
                        ]

layout_graph = [ 
            [sg.Text('Graph')],
                [sg.Canvas(size=(HEIGHT, WIDTH//2-100), key='-canvas-')
                ],
                [sg.Text('Set x axes: '),
                    sg.Radio('Time','radio', key='-RADIO_GF_TIME_X-',default=True, enable_events=True),
                    sg.Radio('Bar','radio',key='-RADIO_GF_BAR_X-', enable_events=True),
                    sg.Radio('T','radio', key='-RADIO_GF_T_X-', enable_events=True)],
                [sg.Text('Set y axes: '),
                    sg.Radio('Bar','radio1',key='-RADIO_GF_BAR_Y-', default=True, enable_events=True),
                    sg.Radio('T','radio1', key='-RADIO_GF_T_Y-', enable_events=True)]
                ]


# ----------- Create actual layout using Columns and a row of Buttons
layout = [
           [sg.Menu(menu_def, tearoff=True)],
            [sg.Column(layout_graph, key='-col2-'),
            sg.VSeperator(),
            *[ sg.Column(mat_csv, visible=False, key='-maturazione_'+v+'-') for (mat_csv, v) in zip(layout_maturazione_csv, vitigni)],
                sg.Column(layout_GF_Perdite, visible=False, key='-GF_perdite-')
                ]
           ]
print(layout)

window = sg.Window('Cantina1.0', layout, finalize=True, size=(WIDTH,HEIGHT), location=(0,0))
window.Finalize()
#window[f'-maturazione_{vitigni[0]}-'].update(visible=True)
canvas_elem = window['-canvas-']
graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
canvas = canvas_elem.TKCanvas
fig_agg = draw_figure(canvas, fig)

current_layout = 'none'   # The currently visible layout
State = 'IDLE'
x_plot = 'time'
time_names=['Data','Ora_misura']

while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    # if maturazione is selected
    if 'maturazione' in event:
        time_names=['Data', 'Ora_raccolta']
        y_plot='Babo'
        if not current_layout == 'none':
            window[f'-{current_layout}-'].update(visible=False)
        current_layout = event.split('::')[1]
        window[f'-{current_layout}-'].update(visible=True)
        updateGraphTable(current_layout,x_plot, y_plot, time_names)
    
    if 'GF' in event:
        y_plot = 'Bar_accumolo'
        if 'RADIO' in event:
            if 'BAR_X' in event:
                x_plot = 'Bar_accumolo'
                time_names=[]
            if 'TIME_X' in event:
                x_plot = 'time'
                time_names=['Data','Ora_misura']
            if 'T_X' in event:
                x_plot = 'T_accumolo'
            if 'BAR_Y' in event:
                y_plot = 'Bar_accumolo'
            if 'T_Y' in event:
                y_plot = 'T_accumolo'
            updateGraphTable(current_layout,x_plot, y_plot, time_names)

        else:
            # gruppo frigo
            if not current_layout == 'none':
                window[f'-{current_layout}-'].update(visible=False)
            current_layout = event.split('::')[1]
            window[f'-{current_layout}-'].update(visible=True)
            updateGraphTable(current_layout,x_plot, y_plot, time_names)



    if 'Submit' in event:
        if 'maturazione' in current_layout:
            maturazioneSaveAndUpdateTable(values, current_layout, current_layout.split('_')[1], maturazione_dati)
            updateGraphTable(current_layout,'time','Babo',['Data','Ora_raccolta'])
        if 'GF' in current_layout:
            SaveAndUpdateTable(values, current_layout,  'GF_perdite', gf_perdite_dati)
            updateGraphTable(current_layout,x_plot, y_plot, time_names)

    if 'Cancel' in event:
        DeleteLine(current_layout, values['table_'+current_layout])
        if 'maturazione'  in current_layout:
            updateGraphTable(current_layout,'time','Babo',['Data','Ora_raccolta'])
        if 'GF'  in current_layout:
            updateGraphTable(current_layout,x_plot, y_plot, time_names)

        


window.close()
