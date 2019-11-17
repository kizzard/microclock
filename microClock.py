# MicroPython Time Module with NTP sync
# For more accurate time keeping on ESP8266 / NodeMCU

import time, ntptime

def isDST(date):
  day = date[2]
  month = date[1]
  # Convert dow to 0 = Sunday
  dow = (date[6]+1)%7
  if month < 3 or month > 11: return False
  if month > 3 and month < 11: return True
  previousSunday = day - dow
  if month == 3: return previousSunday >= 8
  return previousSunday <= 0

class MicroClock():
  def __init__(self, offset, sync=True):
    self.tzOffset = offset
    self.dst = False
    if sync: self.syncTime()
    self.seconds = time.time()
    self.lastMillis = time.ticks_ms()

  def syncTime(self):
    try:
      ntptime.settime()
      self.seconds = time.time()
      self.lastMillis = time.ticks_ms()
    except Exception as ex:
      print("Error during NTP sync: " + str(ex))

  def update(self):
    newMillis = time.ticks_ms()
    milliDelta = time.ticks_diff(time.ticks_ms(), self.lastMillis)
    self.seconds += int(milliDelta/1000)
    self.lastMillis = newMillis - milliDelta % 1000

  def time(self):
    self.update()
    return self.seconds

  def getLocalTime(self):
    self.update()
    secondsOffset = (self.tzOffset + (1 if self.dst else 0)) * 3600
    date = time.localtime(self.seconds + secondsOffset)
    self.dst = isDST(date)
    return date
