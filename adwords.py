import csv
import pandas as pd
import numpy as np
import random
import sys
from operator import itemgetter
random.seed(0)

def Greedy(budgets, bids, queries):
	revenue = 0
	for query in queries:
		highest_bid = 0
        #Make list of highest bidders in case of duplicates
		highest_bidder = []
        #Iterate over the ad request array(bids) for a particular query in the descending order
		for bidder, bidders_bid in sorted(bids[query].items(), key=itemgetter(1), reverse=True):
			# Check if the bidder has enough budget to bid for the ad
			if budgets[bidder] >= bidders_bid:
				if bidders_bid >= highest_bid:
					highest_bid = bidders_bid
					highest_bidder.append(bidder)
				else:
                    #Since we iterate in the descneding order, we break because all subsequent bids will be lesser
					break
		if highest_bid != 0:
			revenue += highest_bid
			budgets[min(highest_bidder)] -= highest_bid

	return revenue


def MSVV(budgets, bids, queries):
	revenue = 0
	for query in queries:
		highest_bid = 0
		max_product = 0
		bidder_with_max_product = -1

		# Sort by id and constantly update bidder with the max product
		for bidder, bidders_bid in sorted(list(bids[query].items())):
			# Check if the bidder has enough budget to bid for the ad
			if budgets[bidder] >= bidders_bid:
				if bidders_bid*bidders_psi_product(bidder, budgets) > max_product:
					bidder_with_max_product = bidder
					highest_bid = bidders_bid
					max_product = highest_bid*bidders_psi_product(bidder, budgets)

		if highest_bid != 0:
			revenue += highest_bid
			budgets[bidder_with_max_product] -= highest_bid

	return revenue


def bidders_psi_product(bidder, budgets):
    #budget variable has the unspent budget
	return 1 - np.exp((budget[bidder]-budgets[bidder])/budget[bidder] - 1)


def Balance(budgets, bids, queries):
	revenue = 0
	for query in queries:
		highest_bid = 0
		bidder_with_highest_budget = -1
		highest_budget = 0

		# Sort by id and constantly update bidder with the highest budget
		for bidder, bidders_bid in sorted(list(bids[query].items())):
			# Check if the bidder has enough budget to bid for the ad
			if budgets[bidder] >= bidders_bid:
				if budgets[bidder] > highest_budget:
					bidder_with_highest_budget = bidder
					highest_budget = budgets[bidder]
					highest_bid = bidders_bid

		if highest_bid != 0:
			revenue += highest_bid
			budgets[bidder_with_highest_budget] -= highest_bid

	return revenue




#Parsing the input

algorithm = sys.argv[1]

with open('bidder_dataset.csv') as bids_file:
    bids_reader = csv.reader(bids_file, delimiter=',')
    line = 0
    budget = {}
    bids = {}
    for row in bids_reader:
        if line:
            bidder = int(row[0])
            keyword = row[1]
            bid = float(row[2])
            if bidder not in budget:
                budget[bidder] = int(row[3])
            if keyword not in bids:
                bids[keyword] = {}
            if bidder not in bids[keyword]:
                bids[keyword][bidder] = bid
        line += 1


with open('queries.txt') as queries_file:
	queries = queries_file.readlines()
queries = [query.strip() for query in queries]




#Since the budget is altered in every iteration of the loop, we pass a copy to preserve it for the next iteration.
total_revenue = 0
if algorithm == 'greedy':
	for i in range(0,100):
		random.shuffle(queries)
		budget_copy = budget.copy()
		revenue = Greedy(budget_copy, bids, queries)
		total_revenue += revenue
elif algorithm == 'balance':
	for i in range(0,100):
		random.shuffle(queries)
		budget_copy = budget.copy()
		revenue = Balance(budget_copy, bids, queries)
		total_revenue += revenue
elif algorithm == 'msvv':
	for i in range(0,100):
		random.shuffle(queries)
		budget_copy = budget.copy()
		revenue = MSVV(budget_copy, bids, queries)
		total_revenue += revenue



average_revenue = total_revenue/100
print(round(average_revenue,2))
comp_ratio = average_revenue/sum(budget.values())
print(round(comp_ratio, 2))
