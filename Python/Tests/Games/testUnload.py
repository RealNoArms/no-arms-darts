import gc, sys
print len(gc.get_objects())


import AroundTheWorld
print len(gc.get_objects())

del sys.modules["AroundTheWorld"]
print len(gc.get_objects())

del AroundTheWorld
print len(gc.get_objects())

gc.collect()
print len(gc.get_objects())
