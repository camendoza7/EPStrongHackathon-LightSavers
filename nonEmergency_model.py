import random
import numpy as np
from keras.models import Model, Sequential
from keras.layers import Dense
import pandas as pd
import itertools

def move(current, previous, wt):
    with open('MLsim.txt', 'a') as f:
        if current == previous:
            count = 2
        else:
            count = 1
            
        wt += queues[0] + queues[1] + queues[2] + queues[3]  
            
        if current:
            q0 = min(count, queues[0])
            q1 = min(count, queues[1])
            q2 = 0
            q3 = 0
            f.write(f'{queues[0]} {q0} {queues[1]} {q1} {queues[2]} {q2} {queues[3]} {q3} {current} \n')
            queues[0] -= q0
            queues[1] -= q1
            return wt
        else:
            q0 = 0
            q1 = 0
            q2 = min(count, queues[2])
            q3 = min(count, queues[3])
            f.write(f'{queues[0]} {q0} {queues[1]} {q1} {queues[2]} {q2} {queues[3]} {q3} {current} \n')
            queues[2] -= q2
            queues[3] -= q3
            return wt


def algorithm(c):
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
    
def train(c, queues):
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
  
M = 'ML'

if M == 'ML':
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c = [False, True]
    product = list(itertools.product(r, r, r, r, c))
    res = []
    for p in product:
        res.append(train(p[-1], p[:-1]))
    df = pd.DataFrame()
    df['Q1'] = [k[0] for k in product]
    df['Q2'] = [k[1] for k in product]
    df['Q3'] = [k[2] for k in product]
    df['Q4'] = [k[3] for k in product]
    df['C'] = [k[4] for k in product]
    df['R'] = res
    X = df[['Q1','Q2','Q3','Q4','C']]
    y = df['R']
    model = Sequential()
    model.add(Dense(6, input_dim=5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=200)
    _, accuracy = model.evaluate(X, y)
    print('Accuracy: %.2f' % (accuracy*100))


qp = [[0] * 2 + [1],
      [0] * 2 + [1],
      [0] * 9 + [1],
      [0] * 9 + [1]]

l = []


ta = 0

for __ in range(100):
    current = True

    previous = True
    
    wt = 0
    
    t = 0
    
    num_cars = 0

    queues = [0, 0, 0, 0]
    
    for _ in range(600):
        previous = current
        for x in range(4):
            n = random.choice(qp[x])
            num_cars += n
            queues[x] += n
        if M == 'timer':
            current, t = timer(current, t)
        elif M == 'algorithm':
            current = algorithm(current)
        else:
            X = pd.DataFrame([{'Q1':queues[0], 'Q2':queues[1], 'Q3':queues[2], 
                               'Q4':queues[3], 'C':current}])
            current = model.predict(X)[0][0]
            if current >= 0.5:
                current = True
            else:
                current = False
        wt = move(current, previous, wt)
    l.append(wt/num_cars)
    
print(f'{M}: {np.mean(l)}')
    
    