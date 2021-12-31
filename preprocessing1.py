def get_data(filename = ''):
    filename = "vrp_dataset/" + filename 
    file = open(filename, 'r')
    lines = file.readlines()
    vehicles = 50
    capacity = 200
    demand = []
    available = []
    load_time = 0
    requests = 0

    i=0
    location = []

    for line in lines:
        line.strip()

    for l in lines:
        if i>0:
            x = (float(l.split()[1]), float(l.split()[2]))
            location.append(x)
            demand.append(float(l.split()[3]))
            load_time = float(l.split()[6])
            available.append(float(l.split()[4]))
        i+=1

    window = float(lines[1].split()[5])
    requests = i-2

    return requests, vehicles, load_time, window, capacity, available, demand, location 

