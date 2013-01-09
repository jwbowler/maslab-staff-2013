import balltracking

balltracking.setup()
while True:
    loc = balltracking.run()
    print str(loc/480) + " " + str(loc%480)
