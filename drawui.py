# ---------------------------------------------------------- import dependencies
import tkinter as tk
from tkinter import *
import pandas as pd
import random as rdm
import numpy as np
# ---------------------------------------------------------------------- set wd
FILE_NAME_HERE = "C:\\Users\\Sebastian Pasotr\\Documents\\Data_Coding\\ga_desprendete\\databases\\desprendete.csv"
# -------------------------------------------------------------------- FUNCTIONS
def makePool(namesList, trueBids=None,min=0, max=100):
    """
    \nnamesList: is a list of the participants involved. \n\n trueBids(default=None): is a list of the true number of bids (if available). If not trueBids is passed, then the bids will be generated randomly with min and max parameters. \n\n min(default=0): is the min random bid possible that can be given out.\n\n max(default=100)L is the max random bid possible that can be given out.
    """
    participants = pd.DataFrame()

    participants['names'] = namesList

    # if True then the probabilities will not be random.
    if trueBids:
        participants['bids'] = trueBids
    else:
        # random number from 0-10 representing bids into pool. Ordinal values
        participants['bids'] = np.random.randint(min,max, size=len(participants))

    # gives 1,000 points to each participant arbitrarily
    participants['pts'] = 0
    participants['pts'] = [points*1000 for points in participants['bids']]

    # list of points per player
    lstpts = participants['pts']
    # normalizes points scale from 0.0 - 1.0. Sum of points adds up to 1.
    norm = [float(i)/sum(lstpts) for i in lstpts]
    participants['pval']=norm # adds norm as pval
    # % win column added
    participants['%Win']=[round(p*100,10) for p in participants['pval']]

    return participants
def proof(dataset, n, onlyWins=False):
    """
    \ndataset: the DataFrame with respective ['names'] & ['pval'] columns used to generate the draw weighted by the corresponding probability for the number of tickets purchased per player. \n\n n:number of things to draw (for our purposes pass 21, since we are drawing 21 shirts). Can be adjusted per draw to 1,3,7, etc. \n\n onlyWins(default=False): if onlyWins is False, it will give you the entire dataframe with a boolean value per winner. if onlyWins is True, the function will return only the list of winners, the corresponding p-values can further be accessed through a for-loop: \n\n
    for i in range(0,len(proof(dataset,n,onlyWins=True))):
        print(participants[participants.values == winners[i]])
    """
    lst=set()
    dataset['win_frequency'] = 0
    p=dataset['pval']
    n=n
    players=dataset['names']

    if onlyWins:
        return rdm.choices(players, weights=p, k=n)
    else:
        lst = rdm.choices(players, weights=p, k=n)
        for player in players:
            num = lst.count(player)
            # dataset['win_frequency'].loc[dataset['names'] == player] = num
            print(player,":" ,f"{num:,}", 'wins.')

        num = len(lst)
        print("Total wins:",f"{num:,}")
    return(dataset)
def phrase_display():
    # Winners of draw
    number_of_winners = 1

    df_real = pd.read_csv(FILE_NAME_HERE)
    df_real['bids'] = [int(amount/1) for amount in df_real['amount']]
    players = makePool(df_real['names'],trueBids=list(df_real['bids']))
    players['names'] = players['names'].str.upper()
    players = players.groupby(['names']).sum()
    players = players.reset_index()
    winners = proof(players,number_of_winners,onlyWins=True)

    # Text field creator
    winners_display = tk.Text(master=window, height=10, width=60)
    winners_display.grid(column=1,row=3)

    winners_display.insert(tk.END,winners)

    return winners
# -------------------------------------------------------------------- CREATE UI
window = tk.Tk()
window.title("Frijol Tech - The Givewaway Engine")
window.geometry("500x500")
# ------------------------------------------------------------- BACKGROUND IMAGE
filename = PhotoImage(file = "C:\\Users\\Sebastian Pasotr\\Documents\\Data_Coding\\ga_desprendete\\images\\desprendete.png")
background_label = Label(window, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# ---------------------------------------------------------------------- BUTTONS
button1 = tk.Button(text="iSortear!",bg='violet', command=phrase_display)
button1.grid(column=1,row=1)
# ------------------------------------------------------------------ RUN PROGRAM
window.mainloop() # runs the gui
# ----------------------------------------------------------- SIMULATION RESULTS
def markdown_creator(filename, numwinners=0):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df1 = pd.read_csv(filename)
    df1['bids'] = [int(amount/1) for amount in df1['amount']]
    pl2 = makePool(df1['names'],trueBids=list(df1['bids']))
    pl2['names'] = pl2['names'].str.upper()
    pl2 = pl2.groupby(['names']).sum()
    pl2 = pl2.reset_index()
    # for i in range(900000,1000001):
    #     print("Simulation: ", i,(proof(pl2, numwinners, onlyWins=True))[0])
    print(proof(pl2, numwinners, onlyWins=False).to_markdown())
markdown_creator(FILE_NAME_HERE,1)
