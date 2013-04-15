# -*- coding: utf-8 -*-


def learning_rate(iter_no, iter_count):
    '''
    Varies the learning rate, depending on iteration step
    '''
    MAX_VALUE = 0.75
    MIN_VALUE = 0.1
    totalrange = MAX_VALUE - MIN_VALUE
    step = iter_no / float(iter_count)

    # Liniar function
    lr = MAX_VALUE - step**1 * totalrange
    return lr

if __name__ == '__main__':
    '''Plots'''
    from pylab import *
    from learning_rate import *

    x = arange(1, 1000, 1)
    y = [learning_rate(i, 1000) for i in x]
    plot(x, y)
    show()
