from ModelHandler.TestModels import main, test_generators
import sys

name = '5556x_markable_640x640'
pix = 640

if len(sys.argv) > 2:
    name = (sys.argv[1])  # var1
    pix = int(sys.argv[2])  # var2

#main()
#main(set='1200x_markable_640x640', PIXELS=640)
#main(set='1200x_markable_299x299', PIXELS=299)
#main(set=name, PIXELS=pix)

# 5556x_mark_res_299x299 299
# 5556x_markable_640x640 640


test_generators(set=name, PIXELS=pix)