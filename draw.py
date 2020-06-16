def main():
    import pandas as pd
    import random as rdm
    import numpy as np

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

def Names(numRandoms=4000, opf=True):
    """
    \n **Names() IS ONLY USED FOR TESTING**
    \n\n numRandoms(default=4000): generates a random number of names for the purposes of introducing random players in game.\n\n opf(default=True): if opf is True, then the names of OPF Redes will be added to the players.
    """
    import names
    additional_names = []
    for i in range(0,numRandoms):
        name = names.get_full_name()
        additional_names.append(name)

    opf = ['Sebastian Pastor', 'Daniel Vijil', 'Hugo Caballero', 'Aldo Piaggio', 'Antonella Wing','Carlos Faccuse','Diego Lorenzana','Diana Mourra','Edison Martinez','Gaspar Vallecillo','Gustavo Raudales','Isabelle Villeda','Lissane Kafie','Alejandro Matamoros','Percy Lainez']

    if opf is True:
        additional_names = additional_names+opf
    return additional_names

def proof(dataset, n, onlyWins=False):
    """
    \ndataset: the DataFrame with respective ['names'] & ['pval'] columns used to generate the draw weighted by the corresponding probability for the number of tickets purchased per player. \n\n n:number of things to draw (for our purposes pass 21, since we are drawing 21 shirts). Can be adjusted per draw to 1,3,7, etc. \n\n onlyWins(default=False): if onlyWins is False, it will give you the entire dataframe with a boolean value per winner. if onlyWins is True, the function will return only the list of winners, the corresponding p-values can further be accessed through a for-loop: \n\n
    for i in range(0,len(proof(dataset,n,onlyWins=True))):
        print(participants[participants.values == winners[i]])
    """
    lst=set()
    p=dataset['pval']
    n=n
    players=dataset['names']

    if onlyWins:
        return (rdm.choices(players, p, k=n))
    else:
        lst = rdm.choices(players, p, k=n)

        for player in players:
            num = lst.count(player)
            print(player,":" ,f"{num:,}", 'wins.')

        num = len(lst)
        print("Total wins:",f"{num:,}")
    print(dataset)


if __name__ == '__main__':
    main()
# generates pool of winners
participants = makePool(Names(500000), max=5000)
winners = proof(participants, 21, onlyWins=True)

# prints the winners with their respective odds
for i in range(0,21):
    print(participants[participants.values == winners[i]],'\n')

def simulation(numSims = 10):
    avgSims = set()
    opfS = dict()

    while len(avgSims) is not numSims:
        participants = makePool(Names())
        winners = proof(participants, 21, onlyWins=True)

        a = set(opfS)
        b = set(winners)

        count = 0
        while bool((set(a).intersection(set(b)))) is False:
            participants = makePool(Names())
            winners = proof(participants, 21, onlyWins=True)
            count +=1
        if bool((set(a).intersection(set(b)))) is True:
            avgSims.add(count)
            opfS[str(set(a).intersection(b))]=count
            count=0
        return(opfS,avgSims)

simulation(2)
len(avgSims)
sum(avgSims)/len(avgSims)


len(avgSims)
# Sebastián Pastor Ferrari 2020 ©
