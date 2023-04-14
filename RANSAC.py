# 1-2 ----
import numpy as np
import matplotlib.pyplot as plt
import csv

# 1-3 ----
# line
f = open('/home/c02/Downloads/RANSAC_data.csv', 'r')
rdr = csv.reader(f)
_mydata = []
# data loading and store to list
for line in rdr :
	#print(line)
	x_data = float(line[0])
	y_data = float(line[1])
	_mydata.append([x_data, y_data])
f.close()
data = np.array(_mydata)

# 1-4 ----

def ransac_line_fitting(data, n_iterations=100, threshold=1, min_inliers=10) :
	best_fit = None
	best_error = np.inf
	best_inliers = None

	for i in range(n_iterations) :
		# Randomly select 2 points from the data
		sample = data[np.random.choice(data.shape[0], 2, replace=False), :]
	
		# Fit a line to the selected points
		x1, y1 = sample[0]
		x2, y2 = sample[1]
		a = (y2 - y1) / (x2 - x1)
		b = y1 - a * x1
	
		# Compute the distance of each point to the line
		distances = np.abs(a * data[:, 0] - data[:, 1] +b) / np.sqrt(a**2 + 1)
	
		#Find inliers within the threshold
		inliers = data[distances < threshold]
	
		#Check if we found a better fit
		if len(inliers) >= min_inliers :
			error = np.sum(distances**2)
			if error < best_error :
				best_fit = (a, b)
				best_error = error
				best_inliers = inliers
		
	return best_fit, best_inliers
	
# 1-5 ----
model, inliers = ransac_line_fitting(data, n_iterations=100, threshold=1, min_inliers=10)

plt.scatter(data[:, 0], data[:, 1], label="Data")
plt.scatter(inliers[:, 0], inliers[:, 1], label="Inliers")
x_range = np.linspace(0, 10, 100)
plt. plot(x_range, model[0] * x_range + model[1], 'r', label="RANSAC Line")
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
