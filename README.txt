Binomial Options Pricing Model (BOPM)
Developed by Cox, Ross, and Rubinstein in 1979

The model divides the time to expiration into a series of discrete intervals.
At each step, the model assumes the price of the underlying asset can move up or down by a specific factor.
This is calculated based on the volatility of the underlying asset and the length of the time interval. 
The up factor is the exponential of volatility times the square root of the time step, and the down factor is its inverse.
The model also calculates the probability of each move occuring, which is derived from the risk-free rate, the time interval, and the up and down factors.
Starting from the underlying price of the asset, the model constructs a recombining binomial tree where each node represents a possible price at a future time.
At the final nodes (the expiration date), the value of the option is the payoff from exercising the option at those prices.
The model then goes backward through the tree, calculating the present value of the option by using the risk-neutral valuation method.
At each node, the option value is the probability-weighted average of the two possible values in the next time interval, discounted back at the risk-free rate.
