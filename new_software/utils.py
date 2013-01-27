# This method bounds an input to low and high
# Input: input value, low and high limits
def bound(value, low, high):
    if value > high:
       return high;
    elif value < low:
       return low
    return value

# This method bounds an input to +high and -high
# Input: input value, high limits
def absBound(value, high):
    if value > high:
       return high;
    elif value < -high:
       return high

    return value
