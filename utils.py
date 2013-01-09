def bound(val, low, high):
  if val > high:
    return high;
  elif val < low:
    return low
  return val


def boundAndScale(val, oMin, oMax, iMin, iMax):
  sign = -1 if val < 0 else 1
  val *= sign
  val -= iMin
  
  val *= (oMax-oMin)/(iMax-iMin)
  val += oMin

  val *= sign
  return val
