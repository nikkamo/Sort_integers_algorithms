#####################################         SORT INTEGERS USING TWO ALGORITHMS AND PLOT ELAPSED TIME AS FUNCTION OF LIST LENGTH         #####################################

# This program sorts integers from a list in ascending order. It uses a txt file with 50 lists of integers and sorts all of them using two algorithms.
# The first algorithm is a simple algorithm, and the other is a divde and conquer algorithm. The average time it takes for the two algorithms to sort all 50 lists and the 
# standard deviation is printed in the terminal. The average elapsed time for lists of the same length and the standard deviation are also calculated and used to make an error
# bar plot with the error given as the standard deviation.

###############################################################################################################################################################################

import time
from statistics import mean, stdev
import matplotlib.pyplot as plt



# Get a file with several lists of integers and save them in a list of lists.
# 
# Input : File with rows of integers to be sorted. Each row should represent a list to sort and the numbers in each row
#         to be sorted should be seperated by a blank space.
# Output : List of integers. list_num[i][j] is the j'th integer in the i'th row.
def make_integer_lists(input_file):
    f = open(input_file, "r", encoding="utf-8")
    rows = f.readlines() # split the input file into strings of each row.
    f.close()

    list_string = []
    list_num = [[int(num) for num in row.split()] for row in rows] # Convert each list of strings to lists of integers
    return list_num


# Simple sorting algorithm where the first number is initially taken as the lowest number and compared with the rest of
# the numbers in the list and everytime a number is less this is taken as the new lowest number. Then this number is
# removed from the list and the list is gone through again the same way, etc.
#
# Input : A list of intergers.
# Output :
#           sorted_list : The sorted list.
#           elapsed_time : The time it takes to sort the list.
def simple_sort(input_list):
    list = input_list.copy()
    start = time.perf_counter()

    sorted_list = []
    for i in range(len(list)): # Take one element in the list at a time
        lowest = list[0] # To start, set the first element in the list to the lowest number
        index = 0
        for j,num in enumerate(list[1:]): # Compare element j with the first element at the beginning and then the first element that is less than this and so on
            if num < lowest: 
                lowest = num # If an element j is less than the previously lowest number put this as the new lowest and continue
                index = j+1 # Because start from index 1 (j=0 still), shift this index by 1
        sorted_list.append(lowest) 
        list.pop(index)
    
    end = time.perf_counter()
    elapsed_time = end - start

    return sorted_list, elapsed_time


# A divide and conquer algorithm to sort integers. It calls itself (recursive function).
#
# Input : A list of intergers.
# Output :
#           sorted_list : The sorted list.
#           elapsed_time : The time it takes to sort the list.
def merge_sort(input_list): 
    sorted_list = []
    start = time.perf_counter()

    if len(input_list) > 1: # If list has more than 1 element, divide it and use function on it
        mid = len(input_list) // 2 # Find mid index of list (//2 divide with integer result, discard remainer)
        
        # Divide list into two halves:
        left = input_list[:mid]
        right = input_list[mid:]

        # Sort the two halves:
        # The lists will be divded until they only have 1 element (because of if-statement). Function merge_sort is called recursively
        left, _ = merge_sort(left)
        right, _ = merge_sort(right)

        i = j = 0
        # Add the lowest current element of the two lists until all of the numbers of one of the lists has been added to sorted_list
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        
        # When all of the numbers of one of the lists has been added to sorted_list, then add the remaining numbers of the other list
        if i == len(left):
            sorted_list.append(right)
        else:
            sorted_list.append(left)

    end = time.perf_counter()
    elapsed_time = end - start
    return sorted_list, elapsed_time

def python_sort(input_list):
    sorted_list = []
    start = time.perf_counter()

    sorted_list = sorted_list.sort()
    
    end = time.perf_counter()
    elapsed_time = end - start
    return sorted_list, elapsed_time


# Sort lists and get average and standard deviations of elapsed times to sort for lists with same length.
#
# Input : 
#           list_num : All the lists to be sorted. Given as a list of lists, such that list_num[i][j] is the j'th number in the i'th list.
#           function : The sorting function to be used.
# Output : 
#           list_num_sorted: The sorted lists in a list. Same structure as input.
#           elapsed_times : List of all elapsed times
#list_num_sorted, elapsed_times, av_list, std_list
def output(list_num, function, print_av = True):
    list_num_sorted = []
    elapsed_times = []
    my_dict = dict() # Dictionary to be able to use key (length) as input
    for my_list in list_num:
        # Get all sorted lists and elapsed times
        sorted_list, elapsed_time = function(my_list)
        list_num_sorted.append(sorted_list)
        elapsed_times.append(elapsed_time)

        # Distinguish lists by their length
        if str(len(my_list)) in my_dict.keys(): # If the length is already a key, append the elapsed time to the output of the key
            my_dict[str(len(my_list))].append(elapsed_time)
        else:
            my_dict[str(len(my_list))] = [elapsed_time] # If the length is not a key, make it a key, and put the elapsed time as output

    if print_av:
        av = []
        stand = []
        av = '{:.2e}'.format( mean(elapsed_times) )
        stand = '{:.2e}'.format( stdev(elapsed_times) )
        if function is simple_sort:
            print('Using simple sorting algorithm:')
        elif function is merge_sort:
            print('Using divide-and-conquer sorting algorithm, merge-sort:')
        else:
            print('Using Python .sort() function:')

        print('Average elapsed time to sort ' + str(len(list_num_sorted)) + ' randomly generated lists in increasing order is: ' + str(av) + ' s')
        print('Standard deviation of elapsed time to sort ' + str(len(list_num_sorted)) + ' lists in increasing order is: ' + str(stand) + ' s')
        print('\n')

    # Find the different lengths of the lists and the corresponding average and standard deviation of elapsed times
    n_list = [int(val) for val in list(my_dict.keys())]
    av_list = []
    std_list = []
    for key in my_dict.keys():
        times = my_dict[key]
        av_list.append( mean(times) )
        if len(times) > 1:
            std_list.append( stdev(times) )
        else: # If only 1 list has certain length, there's no average or standard deviation
            std_list.append( 0 )

    return list_num_sorted, elapsed_times, n_list, av_list, std_list


input_file = "input.txt"
list_num = make_integer_lists(input_file)

plt.figure()
for function in [simple_sort, merge_sort, python_sort]:
    _, _, n_list, av_list, std_list  = output(list_num, function)

    if function is simple_sort:
        label = 'Simple sort'
        ftm = 'o'
    elif function is merge_sort:
        label = 'Merge sort'
        ftm = 's'
    else:
        label = 'Python .sort() function'
        ftm = '*'
    
    plt.errorbar(n_list, av_list, std_list, fmt=ftm, label = label)

plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0)) # Use scientific notation on y-axis
plt.legend()
plt.show()