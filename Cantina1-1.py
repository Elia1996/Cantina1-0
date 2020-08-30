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

            lenmax=0
            for i in data:
                if lenmax<len(i):
                    lenmax=len(i)


            table = [sg.Table(values=data,
                  headings=[ fSp(f,COL_S) for f in header_list],
                  max_col_width=lenmax+10,  
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

def updateGraphTable(ID,graph_type,x_name ,y_name, time_names=[]):
        [data, header_list]  = csvData(ID)
        if len(data)!=0:
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

            updateGraph(x, y, graph_type)
            window.Element('table_'+ID).Update(
                    values= data, num_rows=min(len(data),20))

            

def updateGraph(x, y, tipo):
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
        if tipo == 'GF':
            fig_agg.draw()
        elif tipo == 'MAT':
            fig_agg2.draw()
        else:
            print("Error in update graph")


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



# ------ Menu Definition ------ #
vitigni = ['CorteseA1', 'CorteseA2', 'BarberaA2', 'DolcettoA2']
vini_vitigni = ['Cortese', ['CorteseA1', 'CorteseA2'],'Barbera', ['BarberaA2'], 'Dolcetto',['DolcettoA2']]
vini = ['Cortese', 'Barbera', 'Dolcetto']

maturazione_vitigni = [ v+'::MAT_'+v for v in vitigni]
maturazione_dati =  [ 'Data', 'Ora raccolta',  'T Esterna', 'T Uva' ,'T Mosto', 'Babo', 'PH']
maturazione_dati_default = [Data(), Hour(), '0', '0', '0', '0', '0']

raccolta_vini = [ v+'::RACC_'+v for v in vini]
raccolta_dati = [ 'Data', 'Ora inizio raccolta', 'Ora fine raccolta','Ora fine sgranatura', 'T Uva', 'T Mosto','Kg Uva', 'Hl mosto' , 'Babo']

fermentazioni_vini = [ v+'::FER_'+v for v in vini]
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

#### TABLE layout function
def layoutTable(top_text, table_header, table_header_input_default, table_header_input_size, key_begin):
    # top_text is the text write at the top of the block
    # table header is the list of field to fill in input
    # tbale_header_input_default is the default value of input field
    # table_header_input_size is the length in word of the input field
    # key_begin is used to create the key of each input as:
    #       key_begin + table_header[i].replace(' ','_')
    return [ [sg.Text(top_text)],
             [sg.Text(name, size = (table_header_input_size,1)) for name in table_header],
             [sg.InputText(size = (table_header_input_size,1), 
                            key = key_begin +'_'+ name.replace(' ','_'),
                            default_text= def_text) 
                            for (name,def_text) in zip(table_header, table_header_input_default)],
             csvLayout(key_begin, extract=False, header=[m.replace(' ','_') for m in maturazione_dati]),
             [sg.Submit(), sg.Cancel()]
             ]

#### TABLE layout ###############################################################################
layout_maturazione_csv = [ layoutTable('Prova di maturazione del vitigno '+v, 
                                     maturazione_dati,
                                     maturazione_dati_default, 
                                     COL_S-2, 
                                     'MAT_'+v )  for v in  vitigni]

layout_GF_Perdite = layoutTable('Perdite del circuito da 1000lt presente in cantina',
                                gf_perdite_dati,
                                gf_perdite_dati_default,
                                COL_S+2,
                                'GF_perdite')
#### GRAPH function #############################################################################
def layoutGraph(top_text, canvas_h, canvas_w, key_core, radiox_list=[], radioy_list=[]):
        canvas_key = '-canvas_'+key_core+'-'
        radiox_keys = {}
        radioy_keys = {}
        l = [ [sg.Text(top_text)],
              [sg.Canvas(size=(canvas_h, canvas_w), key=canvas_key)]
              ]
        
        if len(radioy_list) != 0:
            ly = [sg.Text('Settare asse y: ')]
            default1=True
            for y in radioy_list:
                radioy_keys[y] = '-RADIO_'+key_core+'_'+y.upper()+'_Y-'
                ly.append( sg.Radio(y,'radioy', 
                                    key='-RADIO_'+key_core+'_'+y.upper()+'_Y-',
                                    default=default1, enable_events=True))
                default1=False
            l.append(ly)
        
        if len(radiox_list) != 0:
            lx = [sg.Text('Settare asse x: ')]
            default1=True
            for x in radiox_list:
                radiox_keys[x] = '-RADIO_'+key_core+'_'+x.upper()+'_X-'
                lx.append( sg.Radio(x,'radiox', 
                                    key='-RADIO_'+key_core+'_'+x.upper()+'_X-',
                                    default=default1, enable_events=True))
                default1=False
            l.append(lx)

        return  [l, canvas_key, radiox_keys, radioy_keys]

#### GRAPH layout ###############################################################################
graph_GF = layoutGraph('Grafico del gruppo frigo',
                                HEIGHT, WIDTH//2-100,
                                'GF',
                                ['Time', 'Bar_accumolo', 'T_accumolo'],
                                ['Bar_accumolo', 'T_accumolo'])
layout_graph_GF = graph_GF[0]

graph_maturazione = layoutGraph('Grafico di maturazione',
                                        HEIGHT, WIDTH//2-100,
                                        'MAT',
                                        ['Babo','PH']
                                        )
layout_graph_maturazione = graph_maturazione[0]
# ----------- Create actual layout using Columns and a row of Buttons

col1 = sg.Column([[sg.Frame('Graph',
                            [[sg.Column(layout_graph_GF, key='-COL1_GF-', visible=False),
                              sg.Column(layout_graph_maturazione, key='-COL1_MAT-', visible=False)
                              ]]
                           )
                   ]]
                 )
            
col2 = sg.Column([[sg.Frame('Data',
                            [[*[ sg.Column(mat_csv,visible=False, key='-COL2_MAT_'+v+'-') 
                                    for (mat_csv, v) in zip(layout_maturazione_csv, vitigni)],
                                sg.Column(layout_GF_Perdite,visible=False, key='-COL2_GF_perdite-')
                              ]]
                            )
                   ]]
                 )

layout = [
           [sg.Menu(menu_def, tearoff=True)],
            #sg.VSeperator(),
            [col1,col2]
           ]
print(layout)

window = sg.Window('Cantina1.0', layout, finalize=True, size=(WIDTH,HEIGHT), location=(0,0), keep_on_top=True)
window.Finalize()
#window[f'-maturazione_{vitigni[0]}-'].update(visible=True)
canvas_elem = window['-canvas_GF-']
graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
canvas = canvas_elem.TKCanvas
fig_agg = draw_figure(canvas, fig)
canvas_elem2 = window['-canvas_MAT-']
graph2 = FigureCanvasTkAgg(fig, master=canvas_elem2.TKCanvas)
canvas2 = canvas_elem2.TKCanvas
fig_agg2 = draw_figure(canvas2, fig)

current_layout = 'none' #'GF_perdite'   # The currently visible layout
State = 'IDLE'
x_plot = 'time'
y_plot= 'Babo'
time_names=['Data','Ora_misura']

while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    # if maturazione is selected
    if 'MAT' in event:
        if 'RADIO' in event:
            if 'BABO' in event:
                y_plot='Babo'
            if 'PH' in event:
                y_plot='PH'
        else:
            x_plot = 'time'
            time_names=['Data', 'Ora_raccolta']
            if y_plot != 'Babo' and y_plot != 'PH':
                y_plot='Babo'

            if not current_layout == 'none':
                window[f'-COL1_GF-'].update(visible=False)
                window[f'-COL2_{current_layout}-'].update(visible=False)
            current_layout = event.split('::')[1]
            window[f'-COL1_MAT-'].update(visible=True)
            window[f'-COL2_{current_layout}-'].update(visible=True)
            
        updateGraphTable(current_layout, 'MAT', x_plot, y_plot, time_names)
    
    if 'GF' in event:
        y_plot = 'Bar_accumolo'
        if 'RADIO' in event:
        #    if 'BAR_X' in event:
        #        x_plot = 'Bar_accumolo'
        #        time_names=[]
        #    if 'TIME_X' in event:
        #        x_plot = 'time'
        #        time_names=['Data','Ora_misura']
        #    if 'T_X' in event:
        #        x_plot = 'T_accumolo'
        #    if 'BAR_Y' in event:
        #        y_plot = 'Bar_accumolo'
        #    if 'T_Y' in event:
        #        y_plot = 'T_accumolo'
            for x_keys in graph_GF[2]:
                if graph_GF[2][x_keys] in event:
                    if x_keys == 'Time':
                        x_plot = 'time'
                        time_names=['Data','Ora_misura']
                    x_plot = x_keys
                    break
            for y_keys in graph_GF[3]:
                if graph_GF[3][y_keys] in event:
                    y_plot = y_keys


        else:
            # gruppo frigo
            if x_plot=='time':
                time_names=['Data','Ora_misura']
            if not current_layout == 'none':
                window[f'-COL1_MAT-'].update(visible=False)
                window[f'-COL2_{current_layout}-'].update(visible=False)
            current_layout = event.split('::')[1]
            window[f'-COL1_GF-'].update(visible=True)
            window[f'-COL2_{current_layout}-'].update(visible=True)
        
        updateGraphTable(current_layout, 'GF',x_plot, y_plot, time_names)



    if 'Submit' in event:
        if 'MAT' in current_layout:
            SaveAndUpdateTable(values, current_layout, 'MAT_'+current_layout.split('_')[1], maturazione_dati)
            updateGraphTable(current_layout,'MAT','time','Babo',['Data','Ora_raccolta'])
        if 'GF' in current_layout:
            SaveAndUpdateTable(values, current_layout,  'GF_perdite', gf_perdite_dati)
            updateGraphTable(current_layout,'GF',x_plot, y_plot, time_names)

    if 'Cancel' in event:
        DeleteLine(current_layout, values['table_'+current_layout])
        if 'MAT'  in current_layout:
            updateGraphTable(current_layout,'MAT','time','Babo',['Data','Ora_raccolta'])
        if 'GF'  in current_layout:
            updateGraphTable(current_layout,'GF',x_plot, y_plot, time_names)

        


window.close()
