def loadSegment( FromId, ToId ):
   "Load info about segment from the ids"
   import csv
   csv_file = open(r'nodes_small.csv')
   reader = csv.reader(csv_file, skipinitialspace=True)
   A = int(FromId)+1
   B = int(ToId)+1
   segmentFrom = []
   segmentTo = []
   stop = 0
   
   for i, row in enumerate(reader):
      if stop > 2:
         break;
      if i == A:
         segmentFrom = row
         stop += 1
      if i == B:
         segmentTo = row
         stop += 1

   #print segmentFrom
   #print segmentTo
   return [segmentFrom, segmentTo]
