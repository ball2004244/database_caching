# import two modules app and direct_access to compare the performance of the two modules
from app import ReadySetQuery
from direct_access import DirectQuery
import threading
import csv
import matplotlib.pyplot as plt


# create two instances of the two modules
readyset_query = ReadySetQuery()
direct_query = DirectQuery()

def main(query, log_data=False):
    # create two threads to run the two modules simultaneously
    t1 = threading.Thread(target=readyset_query.main, args=(query, log_data))
    t2 = threading.Thread(target=direct_query.main, args=(query, log_data))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('Finished') 

# run 2 prototypes n times and append the performance of each result to csv file
# iteration, readyset, direct_access

def loop(n, query, log_data=False):
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['iteration', 'readyset', 'direct_access']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(n):
            print(f'Iteration {i + 1} of {n}')
            readyset_time = readyset_query.main(query, log_data)
            direct_time = direct_query.main(query, log_data)
            writer.writerow({'iteration': i, 'readyset': readyset_time, 'direct_access': direct_time})
    
    print('Finished')

# read the csv file and calculate the average time of each module
def computing_time():
    with open('results.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        readyset_sum = 0
        direct_sum = 0
        count = 0
    
        for row in reader:
            readyset_sum += float(row['readyset'])
            direct_sum += float(row['direct_access'])
            count += 1
    
        readyset_avg = readyset_sum / count
        direct_avg = direct_sum / count
        print("Readyset average time: ", readyset_avg)
        print("Direct_access average time: ", direct_avg)

        print(f'ReadySet is {direct_avg / readyset_avg:.2f} times faster than Direct Access')

def data_plot():
    with open('results.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        readyset = []
        direct = []
    
        for row in reader:
            readyset.append(float(row['readyset']))
            direct.append(float(row['direct_access']))
    
        plt.plot(readyset, label='ReadySet')
        plt.plot(direct, label='Direct Access')
        plt.xlabel('Iteration')
        plt.ylabel('Time (s)')
        plt.title('ReadySet vs Direct Access')
        plt.legend()
        plt.savefig('plot.png')

def get_query():
    with open('query.txt', 'r') as f:
        query = f.read()
    return query

if __name__ == '__main__':
    # main(get_query(), log_data=False)

    loop(1000, get_query(), log_data=False)
    computing_time()
    data_plot()


