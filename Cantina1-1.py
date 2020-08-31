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
from autoLayout import (Data, Hour, autoLayout)

COL_S=10
HEIGHT=1000
WIDTH=1300


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

win = autoLayout(HEIGHT, WIDTH, 'GF')
win.layoutMenu(menu_def)
win.layoutTable('Tabella per annotare l\'andamento Pressione/Temperatura/tempo dell\'accumolo',
                gf_perdite_dati,
                gf_perdite_dati_default,
                COL_S+2)
win.layoutGraph('Grafico del gruppo frigo',
                ['Data','Ora_misura'],
                ['time', 'T_accumolo', 'Bar_accumolo'],
                ['T_accumolo', 'Bar_accumolo'])
win.layoutCreate('Grafico','Tabella')
win.openWindow('Cantina1',True)


while True:
    event, values = win.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    win.routine(event, values)

win.close()
