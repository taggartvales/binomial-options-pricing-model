import math

# csp = S = current stock price
# sp = K = strike price of the option
# et = T = time to expiration in years
# rfir = r = risk free interest rate
# vs = sigma = volatility of the stock, expressed as a standard deviation
# nts = n = number of time steps in the binomial tree

# dt = time to expiration is divided into n equal intervals, each of length: delta t = T/n
# uf = up factor: u = e^(sigma*sqrt(delta t))
# df = down factor: d = 1/u = e^(-sigma*sqrt(delta t))
# rnp = risk neutral probability: p = (e^(r*delta t)-d)/(u-d)

# call option: payoff = max(S - K,0)
# put option: payoff = max(K - S,0)

# for node at time with future values Vup and Vdown, the option value is: V = e^(-r*delta t)[p*Vup + (1-p)Vdown]

print("What is the current stock price? ")
csp = float(input())

print("What is the strike price of the option? ")
sp = float(input())

print("What is the time to expiration in years? ")
et = float(input())

print("What is the risk free interest rate as a decimal? ")
rfir = float(input())

print("What is the volatility of the stock as a standard deviation? ")
vs = float(input())

print("What is the desired number of time steps? ")
nts = int(input())

dt = et/nts
uf = math.exp(vs*math.sqrt(dt))
df = math.exp((-vs)*math.sqrt(dt))
rnp = (math.exp(rfir*dt)-df)/(uf-df)

co = max(csp - sp, 0)
po = max(sp - csp, 0)

print(csp, sp, et, rfir, vs, nts)
print(dt, uf, df, rnp)
print(co, po)

class Node:
    def __init__(self, price, depth, index):
        self.price = price # price at node
        self.depth = depth # time step
        self.index = index
        self.up = None
        self.down = None
        
class Tree:
    def __init__(self, ip, uf, df, nts):
        self.ip = ip # initial price
        self.uf = uf # up factor
        self.df = df # down factor
        self.nts = nts # number of time steps
        self.root = Node(ip, 0, 0)
        self.construct_tree()

    def construct_tree(self):
        current_level = [self.root]
        for level in range(1, self.nts + 1):
            seen_prices = {}  # This should be a dictionary to hold nodes

            for node in current_level:
                up_price = round(node.price * self.uf, 2)
                down_price = round(node.price * self.df, 2)

                # Handle up node
                if up_price not in seen_prices:
                    up_node = Node(up_price, level, 0)  # The index is just a placeholder
                    seen_prices[up_price] = up_node
                else:
                    up_node = seen_prices[up_price]

                # Handle down node
                if down_price not in seen_prices:
                    down_node = Node(down_price, level, 0)  # The index is just a placeholder
                    seen_prices[down_price] = down_node
                else:
                    down_node = seen_prices[down_price]

                # Link current node to its up and down nodes
                node.up = up_node
                node.down = down_node

            current_level = list(seen_prices.values())  # Update current_level with unique nodes

            
    def display_tree(self):
        current_level = [self.root]
        for level in range(self.nts + 1):
            print(f"Level {level}:")
            seen_prices = set()  # Track prices to avoid duplicates
            for node in current_level:
                if node.price not in seen_prices:
                    print(node.price, end=' ')
                    seen_prices.add(node.price)
            
            print()  # New line after each level

            next_level = []
            for node in current_level:
                if node.up is not None and node.up.price not in seen_prices:
                    next_level.append(node.up)
                if node.down is not None and node.down.price not in seen_prices:
                    next_level.append(node.down)

            current_level = next_level

def calculate_payoff(node, sp):
    if node is None:
        return
    if node.up is None and node.down is None:
        node.option_value = max(node.price - sp, 0)
    else:
        calculate_payoff(node.up, sp)
        calculate_payoff(node.down, sp)

def calculate_present_value(node, rfir, dt, rnp):
    if node is None or (node.up is None and node.down is None):
        return
    calculate_present_value(node.up, rfir, dt, rnp)
    calculate_present_value(node.down, rfir, dt, rnp)
    
    up_value = node.up.option_value if node.up is not None else 0
    down_value = node.down.option_value if node.down is not None else 0
    node.option_value = math.exp(-rfir*dt)*(rnp*up_value+(1-rnp)*down_value)


bt = Tree(ip=csp, uf=uf, df=df, nts=nts)
bt.display_tree()
calculate_payoff(bt.root, sp)
calculate_present_value(bt.root, rfir, dt, rnp)
present_value = bt.root.option_value
print("The present value is $",present_value)

