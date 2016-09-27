# Loaders.py

'''
Collection of loaders
http://softwarerecs.stackexchange.com/questions/7463/fastest-python-library-to-read-a-csv-file
'''

# import pandas
# import numpy
import csv

csv_delimiter = ','

# 3.82s
def open_with_python_csv(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    data =[]
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        for row in csvreader:
            data.append(row)    
    return data

# 8.55s
def open_with_python_csv_cast_as_float(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    data =[]
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        for row in csvreader:
            data.append(map(float, row))    
    return data

# 3.58s --- victorious!
def open_with_python_csv_list(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    data =[]
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        data = list(csvreader)    
    return data

'''
# 26.6s
def open_with_numpy_loadtxt(filename):
    # http://stackoverflow.com/questions/4315506/load-csv-into-2d-matrix-with-numpy-for-plotting

    data = numpy.loadtxt(open(filename,'rb'),delimiter=csv_delimiter,skiprows=0)
    return data

# 4.37s, skips first line
def open_with_pandas_read_csv(filename):
    df = pandas.read_csv(filename, sep=csv_delimiter)
    data = df.values
    return data    
'''
