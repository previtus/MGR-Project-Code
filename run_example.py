import keras
from DatasetHandler.CreateDataset import *
from ModelHandler.CreateModel.functions_for_vgg16 import *
import time

#d = load_8376_resized_150x150(desired_number=10)
#d.statistics()

start = time.time()
print time.ctime()

main_vgg16(TMP_num_of_epochs=100, name_of_the_experiment = '-first_experiments')

end = time.time()
print time.ctime()

print "### TOTAL TIME ", format(end - start, '.2f'), " sec."