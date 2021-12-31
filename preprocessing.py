def get_data(filename = 'big_tai385D.vrp'):
	filename = "vrp_dataset/" + filename 
	file = open(filename, 'r')
	lines = file.readlines()

	 
	for line in lines:
	    line.strip()

	requests = int(lines[7].split(' ')[1])
	vehicles = int(lines[8].split(' ')[1])
	capacity = int(lines[9].split(' ')[1])

	demand = [0]*(requests)
	
	for i in range(1, requests):
		demand[i] = int(lines[i+13].split()[1])*-1
	
	k = 13 + requests + 1

	location = [(None, None)]*(requests)

	for i in range(requests):
		location[i] = (( int(lines[i+k].split()[1])), int(lines[i+k].split()[2]) )

	k  += 2*requests + 3
	load_time = int(lines[k].split()[1])
	k += requests
	window = int(lines[k].split()[2])

	available = [0]*(requests)
	for i in range(1, requests):
		available[i] = int(lines[i+k+2].split()[1])

	return requests, vehicles, load_time, window, capacity, available, demand, location 
