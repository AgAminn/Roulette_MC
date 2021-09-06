import numpy as np
import matplotlib.pyplot as plt

def get_spin_result(win_prob):
    """
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.

    :param win_prob: The probability of winning
    :type win_prob: float
    :return: The result of the spin.
    :rtype: bool
    """
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def pseudo_code_test():
    episodes_winning = 0
    while episodes_winning <80 :
        won = False
        bet_amount = 1
        while not won:
            # wager on black = bet_amount
            won = get_spin_result(win_prob=18/38)
            if won:
                episodes_winning+=bet_amount
            else:
                episodes_winning-=bet_amount
                bet_amount = bet_amount*2
    return episodes_winning

def experiment_1(n_episode = 1, winning_prob=18/38, bet=1,episode_size=1000):
    '''
    - unlimited bankroll -
    Professor Balch’s original betting strategy. 
    The approach is called Monte Carlo simulation. 

    '''
    results = []
    tab = np.empty((n_episode,episode_size),dtype=type(bet))
    tab.fill(80)
    #tab[0,2]=5
    #print(tab)
    
    #while episodes_winning <80 :
    for e in range(n_episode):
        episodes_winning = 0
        won = False
        bet_amount = bet
        for i in range (1000):
            # wager on black = bet_amount
            won = get_spin_result(win_prob=winning_prob)
            if won:
                episodes_winning+=bet_amount
                bet_amount = bet
            else:
                episodes_winning-=bet_amount
                bet_amount *=2
            if episodes_winning > 80:
                break
            results.append(episodes_winning)
            tab[e,i]=episodes_winning
        #print(results[0])
    return tab


def experiment_2(n_episode = 1, winning_prob=18/38, bet=1,bankroll_0=256,episode_size=1000):
    '''
    - Limited bankroll -
    Martingale method. 
    '''

    tab = np.empty((n_episode,episode_size),dtype=type(bet))
    tab.fill(80)
    for e in range(n_episode):
        bet_amount = bet
        bankroll_history = []
        episodes_winning = 0
        i = 0
        bankroll = bankroll_0
        while bankroll > 0  and i<tab.shape[1]:
            if bet_amount > bankroll:
                bet_amount = bankroll
            roll = get_spin_result(win_prob=winning_prob)
            if roll :
                bankroll += bet_amount
                episodes_winning+=bet_amount
                bet_amount = bet
                tab[e,i]= episodes_winning
            else:
                bankroll -= bet_amount
                episodes_winning-=bet_amount
                bet_amount *=2
                tab[e,i]= episodes_winning
            if episodes_winning > 80:
                tab[e,i:].fill(80)
                bankroll = 0
            elif episodes_winning <-255 :
                tab[e,i:].fill(-256)
                bankroll = 0
            '''elif bankroll <1 :
                tab[e,i:].fill(episodes_winning)
                bankroll = 0'''
            i+=1
        bankroll_history.append(bankroll)
        #print(bankroll_history[-1])
    #print(len(bankroll_history))
    return tab

def plot_result(tab, experiment_num=1):

    def set_fig():
        plt.ylim(ymax = 100, ymin = -256)
        plt.xlim(xmax = indx_80_max, xmin = 0)
        plt.xlabel("spin")
        plt.ylabel("Win")
        plt.legend()

    # find when the the max 80$ is reached
    indx_80_max = 0
    for e in range(tab.shape[0]):
        indx_80 = 0
        for i in range(indx_80_max,tab.shape[1]):
            if tab[e,i] == 80 or tab[e,i]==-256:
                indx_80 = i
                break
        if indx_80 > indx_80_max:
            indx_80_max = indx_80
    
    #plot ep graphs
    fig_num=1
    if experiment_num == 1:
        plt.figure(1)
        for e in range(tab.shape[0]):
            plt.plot(tab[e,:], label='ep_'+str(e),)
        fig_num+=1
        # Adding legend, Naming the x-axis, y-axis, Figure title
        plt.title("Fig "+str(fig_num)+" :Winnings per spin for each episode")
        set_fig()
    else:
        fig_num+=3    
    

    plt.figure(fig_num)
    #calculating mean and median
    up_mean=[]
    low_mean=[]
    up_median = []
    low_median = []
    for i in range(tab.shape[1]):
        up_mean.append(np.mean(tab[:,i])+np.std(tab[:,i]) )
        low_mean.append(np.mean(tab[:,i])-np.std(tab[:,i]) )
        up_median.append(np.median(tab[:,i])+np.std(tab[:,i]) )
        low_median.append(np.median(tab[:,i])-np.std(tab[:,i]) )

    
    for e in range(tab.shape[0]):
        plt.plot(tab[e,:], label='ep_'+str(e),color='0.75')
    plt.plot(up_mean, label='U mean')
    plt.plot(low_mean, label='L mean')
        
    # Adding legend, Naming the x-axis, y-axis, Figure title
    plt.title("Fig "+str(fig_num)+" :Mean per spin")
    fig_num+=1
    set_fig()

    plt.figure(fig_num)
    for e in range(tab.shape[0]):
        plt.plot(tab[e,:], label='ep_'+str(e),color='0.75')
    plt.plot(up_median, label='U median')
    plt.plot(low_median, label='L median')
    


    # Adding legend, Naming the x-axis, y-axis, Figure title
    plt.title("Fig "+str(fig_num)+" Median per spin")
    set_fig()
    plt.show()
    return 0


def test_code():
    """
    Method to test your code
    """
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(42)  # do this only once
    print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    
    res = experiment_1(n_episode=10)
    plot_result(tab=res,experiment_num=1)
    res = experiment_2(n_episode=10)
    plot_result(tab=res,experiment_num=2)
    


if __name__ == "__main__":
    test_code()
