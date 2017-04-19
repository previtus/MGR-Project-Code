import keras
from DatasetHandler.CreateDataset import *
from ModelHandler.CreateModel.functions_for_vgg16 import *
import time
import sys

# DEFAULT VALUES:
TMP_size_of_dataset=100
TMP_num_of_epochs=150
name_of_the_experiment = '-newWawe-1stRoundShouldCountBoth'

# python python_script.py var1 var2 var3
if len(sys.argv) > 3:
    TMP_size_of_dataset = int(sys.argv[1])  # var1
    TMP_num_of_epochs = int(sys.argv[2])  # var2
    name_of_the_experiment = sys.argv[3]  # var3
else:
    print "Using default values. Please run as: python_script.py sizeOfDataset numOfEpochs nameOfExp"

print "[Setting] python_script.py", TMP_size_of_dataset, TMP_num_of_epochs, name_of_the_experiment


#d = load_8376_resized_150x150(desired_number=10)
#d.statistics()

start = time.time()
print time.ctime()

main_vgg16(TMP_size_of_dataset=TMP_size_of_dataset, TMP_num_of_epochs=TMP_num_of_epochs, name_of_the_experiment = name_of_the_experiment)

end = time.time()
print time.ctime()

print "### TOTAL TIME ", format(end - start, '.2f'), " sec."