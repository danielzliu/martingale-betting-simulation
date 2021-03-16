import random
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import math
import numpy as np
import statistics


class Simulation_Round:
    #One round of simulation betting with martingale strategy until money runs out.

    def __init__(self, money_history, attempted_bets):
        self.money_history = money_history
        self.attempted_bets = attempted_bets
        #Number of bets is the number of attempted bets minus one, since the last bet is never succesful
        self.number_of_bets = len(attempted_bets) - 1
        self.max_value = max(money_history)
        self.largest_bet = max(attempted_bets[:-1])
        self.consecutive_fails = math.log(max(attempted_bets),2)
        
    

def simulate_bet(p, win_factor, bet_amount):
    #Simulates a bet and returns the amount of money you win.
    random_number = random.random()

    if p > random_number:
        return bet_amount * 2

    else:
        return 0

def simulate_round(starting_money, p, win_factor):

    money = starting_money

    #A list of the money before each bet to plot later
    money_history = [money]

    attempted_bets = [1]

    #Start with a bet amount of 1
    bet_amount = 1

    while money > bet_amount:
        
        #Set aside money for bet
        money = money - bet_amount

        #Make the bet
        return_of_bet = simulate_bet(p, win_factor, bet_amount)

        #Add return of bet to your money if it is succesful
        money = money + return_of_bet

            
        #If the bet is not succesful, double it in the next bet. Otherwise just bet 1.
        if return_of_bet == 0:
            bet_amount = 2 * bet_amount

        elif return_of_bet != 0:
            bet_amount = 1

        
        #Write down the money after the round
        money_history.append(money)
        #Write down the bet for next round
        attempted_bets.append(bet_amount)


    simulation_round = Simulation_Round(money_history, attempted_bets)

    return simulation_round

def simulate_rounds(iterations = 10000):
    #Creates list of all simulation rounds

    simulations = []
    
    for i in range(iterations):
        simulation_round = simulate_round(starting_money, p, win_factor)

        simulations.append(simulation_round)

    return simulations


        
starting_money = 100
#The probability of success
p = 0.5
#The win factor if the bet is succesful. A factor 2 means you receive a return of 100% of you bet.
win_factor = 2

simulations = simulate_rounds(iterations = 10000)


#------------------------PLOTTING------------------------#

#Plots a histogram of the outcomes of the maximum values
max_values = [s.max_value for s in simulations]

plt.subplot(2,2,1)
plt.title('Distribution of maximum value of portfolio')
plt.xlabel('Maxiumu value of portfolio')
plt.ylabel('Percentage of occurences')
plt.hist(max_values, bins = 20, range = (starting_money, starting_money * 10),weights=np.ones(len(max_values)) / len(max_values))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))



#Plots the expected value if one would stop if they reached a certain limit
x = range(starting_money, 3*starting_money)
y = []

for i in x:
    simulations_over_threshold = [s.max_value for s in simulations if s.max_value >= i]
    number_of_succesful_simulations = len(simulations_over_threshold)
    expected_value_of_strategy = i * number_of_succesful_simulations / len(simulations)
    y.append(expected_value_of_strategy)

plt.subplot(2,2,2)
plt.title('Expected value if stopped after certain value of portfolio')
plt.xlabel('Value stopped at')
plt.ylabel('Expected value of portfolio')
plt.plot(x,y)



#Plots the expected value if one would stop after a certain amount of bets
expected_value_after_i_bets = []

for i in range(1,501):

    values_after_i_bets_case = [s.money_history[i] for s in simulations if len(s.money_history) > i]
    expected_value_after_i_bets_case = sum(values_after_i_bets_case) / len(simulations)
    expected_value_after_i_bets.append(expected_value_after_i_bets_case)
    
plt.subplot(2,2,3)
plt.title('Expected value if stopped after certain amounts of bets')
plt.xlabel('Number of bets')
plt.ylabel('Expected value of portfolio')
plt.plot(expected_value_after_i_bets)



#Plots variance after certain amount of mooves
variance_after_i_bets = []

for i in range(1,201):
    values_after_i_bets_case = [s.money_history[i] for s in simulations if len(s.money_history) > i]

    while len(values_after_i_bets_case) > len(simulations):
        values_after_i_bets_case.append(0)
    
    variance_after_i_bets.append(statistics.variance(values_after_i_bets_case))

    

plt.subplot(2,2,4)
plt.title('Variance of portfolio value after certain amounts of bets')
plt.xlabel('Number of bets')
plt.ylabel('Variance')
plt.plot(variance_after_i_bets)
    
   
plt.show()

    
