'''
@author: Jeremy Bayley
@email : TheEnvironmentGuy@gmail.com
@websight : TheEnvironmentGuy.com

Friday March 28 2016

-*- coding: utf-8 -*-
'''

#Inch defined in decimal of a meter
inch = 0.0254

def ImperialToMetric(size=[1,2,3]):  
    size[0] *= inch
    size[1] *= inch
    size[2] *= inch
    return(size)
    