# ESP8266 microclock
MicroPython's time module does not hold accurate time on the ESP8266. This module offers more accuracy (in the realm of seconds per week)

## Notes
I don't recommend this for extremely accurate time or date calculation. DST calculation is hard coded for the USA, but you could override microClock.isDST() with a method that accepts a date tuple and returns a boolean to change this behavior.

## Reference

    class microClock.MicroClock(offset[, sync])

Returns (MicroClock)

 - offset (integer): timezone hour offset eg -8 for US/Pacific
 - sync (boolean): initialize seconds via NTP

------------

    MicroClock.time()

Return (integer): seconds since 2000 epoch

Returns the number of seconds since Jan 1st, 2000.

------------

    MicroClock.getLocalTime()

Return (tuple[int]): (year, month, day, hour, second minute, dayOfWeek)

Returns the current date and time

------------

    MicroClock.update()

Should be called once every so often if getLocalTime() is not called. This ensures the system ticks which are relied upon for time keeping don't wrap around more than once. The wrap around period is not well defined but in testing on a NodeMCU it is at least several minutes.

------------

    MicroClock.syncTime()

Sync time to pool.ntp.org