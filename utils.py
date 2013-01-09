def bound(val, low, high):
  if val > high:
    return high;
  elif val < low:
    return low
  return val


def boundAndScale(val, iMin, iMax, oMin, oMax, thresh):
  sign = -1 if val < 0 else 1
  val *= sign
  val -= iMin
  
  val *= (oMax-oMin)/(iMax-iMin)
  if val > thresh:
    val += oMin

  val *= sign
  return val

def getMotorSpeeds(vel, rot):
  r = vel-rot;
  l = vel+rot;

  m = max(abs(r), abs(l))
  if (m > 1):
    r /= m;
    l /= m;

  return (r,l);

