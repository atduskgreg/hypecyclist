import numpy as np
from scipy.interpolate import spline
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as p

import scipy
import scipy.optimize

import subprocess
import os
import csv
import re

import string
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

x = np.array([0,10,20,30,40,50])
y = np.random.randint(50,size=len(x))

f2 = interp1d(x, y, kind='cubic', bounds_error=False, fill_value=0)
xnew = np.linspace(np.amin(x), np.amax(x), 5000)

ptsX = []
ptsY = []

for i in xnew:
 	d = scipy.misc.derivative(f2,i)
 	if np.absolute(d) < 0.1:
 		if len(ptsX) == 0 or np.absolute(i - ptsX[-1]) > 1:
 			ptsX = np.append(ptsX, i)
 			ptsY = np.append(ptsY, f2(i))

# add midpoints

for i in range(len(ptsX)):
	if i > 0:
		prevDist = np.absolute(ptsY[i] - ptsY[i-1])
		if i < len(ptsX) - 1:
			nextDist = np.absolute(ptsY[i+1] - ptsY[i])
		else:
			nextDist = 50
		
		print "prevDist: {} nextDist: {}".format(prevDist, nextDist)

		if prevDist > 15 and nextDist > 15:
			midX = ptsX[i-1] + (ptsX[i] - ptsX[i-1])/2
			ptsX = np.append(ptsX, midX)
			ptsY = np.append(ptsY, f2(midX))
			# print "({} -> {}) {},{}".format(ptsX[i], ptsX[i-1], midX, f2(midX))


def label_for_point(px,d):
	# print d
	if d > 0 and d < 1:
		return subprocess.check_output("ruby generate_terms2.rb max", shell=True)
	elif d > 1:
		return subprocess.check_output("ruby generate_terms2.rb slup", shell=True)
	elif d < -1:
		return subprocess.check_output("ruby generate_terms2.rb slown", shell=True)
	elif d < 0 and d > -1:
		return subprocess.check_output("ruby generate_terms2.rb min", shell=True)
	else:
		return "label"

for i in range(len(ptsX)):
	d = scipy.misc.derivative(f2, ptsX[i], n=1)

	# if i > 1:
	# 	plt.axvline(ptsX[i-1] + (ptsX[i] - ptsX[i-1])/2, color="#cccccc", linestyle="--")
	# else:
	# 	plt.axvline(ptsX[i]/2, color="#cccccc", linestyle="--")
	# # else:


	plt.axvline(ptsX[i], color="#cccccc", linestyle="--")


	if d > 0 and d < 1:
		m = 5
	elif d < 0 and d > -1:
		m = -5
	else:
		m = 0

	plt.annotate(label_for_point(ptsX[i],d), xy=(ptsX[i], ptsY[i]),verticalalignment="top", xytext=(ptsX[i], -3), fontsize=10, horizontalalignment='center')


plt.annotate(subprocess.check_output("ruby generate_terms2.rb start", shell=True),xy=(x[0], y[0]), xytext=(x[0], -3),verticalalignment="top", fontsize=10, horizontalalignment='center')

pts = np.clip(np.random.randint(2,6, size=20).cumsum(), np.amin(xnew), np.amax(xnew))#np.linspace(np.amin(x) + 5, np.amax(x) - 5, 10)


csv_path = "lists/{}".format(random.choice(os.listdir("lists")))
entries = open(csv_path).read().split(",")
title =  re.sub(r'List', "Hype Cycle", string.capwords(entries[0]))
es = np.array(entries[1:len(entries)])

for pt in pts:
	d = scipy.misc.derivative(f2,pt)
	if d > 0.8:
		xOffset = -2
		yOffset = -0.2
		hAlign = "right"
	elif d < -0.8:
		xOffset  = 2
		yOffset = -0.2
		hAlign = "left"
	else:
		xOffset = 0
		yOffset = 1
		hAlign = "center"

	print "d: {}, xoff: {} yoff: {}".format(d, xOffset, yOffset)
 	plt.annotate(unicode(random.sample(es, 1)[0]), xy = (pt, f2(pt)), xytext=(pt + xOffset, f2(pt) + yOffset),verticalalignment="center", horizontalalignment=hAlign, fontsize=8, arrowprops=dict(shrink=0.1, color='gray', frac=0, width=0.1, headwidth=0))

print(title)
plt.title(unicode(title), fontsize=24)
plt.plot(xnew,f2(xnew), linewidth=3.0, color="#66ccff")

plt.plot(pts, f2(pts), marker="o", color="w", linestyle="none")

frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)

frame.spines['top'].set_visible(False)
frame.spines['right'].set_visible(False)
frame.spines['left'].set_color('#aaaaaa')
frame.spines['bottom'].set_color('#aaaaaa')

# plt.arrow(0, np.amax(y) + 3, 0, 0.1, color="0.6", clip_on=False, head_width=0.5, head_length=1)
# plt.arrow(29, 0, 0.1, 0, color="0.6", clip_on=False, head_width=1, head_length=0.5)

plt.savefig('samplefigure', bbox_inches='tight')

plt.show()