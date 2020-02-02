import random
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Dense
import pandas as pd
import itertools

def move(current, previous, wt, wte):
    if current == previous:
        count = 2
    else:
        count = 1
        
    wt += len(queues[0]) + len(queues[1]) + len(queues[2]) + len(queues[3]) 
    wte += queues[0].count('e') + queues[1].count('e') + queues[2].count('e') + queues[3].count('e') 
    with open('MLtest.txt', 'a') as f:    
        if current:
            q0 = min(count, len(queues[0]))
            q1 = min(count, len(queues[1]))
            q2 = 0
            q3 = 0
            f.write(f'{queues[0]} {q0} {queues[1]} {q1} {queues[2]} {q2} {queues[3]} {q3} {current} \n')
            del queues[0][0:q0]
            del queues[1][0:q1]
            return wt, wte
        else:
            q0 = 0
            q1 = 0
            q2 = min(count, len(queues[2]))
            q3 = min(count, len(queues[3]))
            f.write(f'{queues[0]} {q0} {queues[1]} {q1} {queues[2]} {q2} {queues[3]} {q3} {current} \n')
            del queues[2][0:q2]
            del queues[3][0:q3]
            return wt, wte


def algorithm(c):
    if 'e' in queues[0] or 'e' in queues[1]:
        return True
    if 'e' in queues[2] or 'e' in queues[3]:
        return False
    if c:
        tpc = min(2, len(queues[0])) + min(2, len(queues[1]))
        tpa = min(1, len(queues[2])) + min(1, len(queues[3]))
    else:
        tpa = min(2, len(queues[0])) + min(2, len(queues[1]))
        tpc = min(1, len(queues[2])) + min(1, len(queues[3]))
        
    if tpa > tpc:
        return not c
    else:
        return c
    
def train(queues, c, e0, e1):
    if e0:
        return True
    if e1:
        return False
    if c:
        tpc = min(2, queues[0]) + min(2, queues[1])
        tpa = min(1, queues[2]) + min(1, queues[3])
    else:
        tpa = min(2, queues[0]) + min(2, queues[1])
        tpc = min(1, queues[2]) + min(1, queues[3])
        
    if tpa > tpc:
        return not c
    else:
        return c
    
def timer(c, t):
    t += 1
    if t == 60:
        c = not c
        return c, t
    elif t == 80:
        t = 0
        c = not c
        return c, t
    else:
        return c, t
    
def add_cars(q, num_emergency):
    n = random.choice(qp[q])
    re = []
    for _ in range(n):
        c = np.random.choice(['n', 'e'], p = [299/300, 1/300])
        if c == 'e':
            num_emergency += 1
        re.append(c)
    return re, num_emergency
  
M = 'ML'

if M == 'ML':
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c = [False, True]
    e0 = [False, True]
    e1 = [False, True]
    product = list(itertools.product(r, r, r, r, c, e0, e1))
    res = []
    for p in product:
        res.append(train(p[:4], p[4], p[5], p[6]))
    df = pd.DataFrame()
    df['Q1'] = [k[0] for k in product]
    df['Q2'] = [k[1] for k in product]
    df['Q3'] = [k[2] for k in product]
    df['Q4'] = [k[3] for k in product]
    df['C'] = [k[4] for k in product]
    df['e0'] = [k[5] for k in product]
    df['e1'] = [k[6] for k in product]
    df['R'] = res
    X = df[['Q1','Q2','Q3','Q4','C', 'e0', 'e1']]
    y = df['R']
    model = Sequential()
    model.add(Dense(6, input_dim=7, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=50)
    _, accuracy = model.evaluate(X, y)
    print('Accuracy: %.2f' % (accuracy*100))


qp = [[0] * 9 + [1],
      [0] * 9 + [1],
      [0] * 19 + [1],
      [0] * 19 + [1]]

l = []
le = []


ta = 0

for __ in range(100):
    current = True

    previous = True
    
    wt = 0
    
    wte = 0
    
    t = 0
    
    num_cars = 0
    
    num_emergency = 0

    queues = [[], [], [], []]
    
    for _ in range(3600):
        previous = current
        for x in range(4):
            n, num_emergency = add_cars(x, num_emergency)
            num_cars += len(n)
            queues[x] += n
        if M == 'timer':
            current, t = timer(current, t)
        elif M == 'algorithm':
            current = algorithm(current)
        else:
            if 'e' in queues[0] or 'e' in queues[1]:
                e0 = True
            else:
                e0 = False
            if 'e' in queues[2] or 'e' in queues[3]:
                e1 = True
            else:
                e1 = False
            X = pd.DataFrame([{'Q1':len(queues[0]), 'Q2':len(queues[1]), 'Q3':len(queues[2]), 
                               'Q4':len(queues[3]), 'C':current, 'e0':e0, 'e1':e1}])
            current = model.predict(X)[0][0]
            if current >= 0.5:
                current = True
            else:
                current = False
        wt, wte = move(current, previous, wt, wte)
    l.append(wt/num_cars)
    if num_emergency:
        le.append(wte/num_emergency)
    
print(f'{M}: {np.mean(l)}')
print(f'Emergency {M}: {np.mean(le)}')
    
    


