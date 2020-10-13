# spin-checker

```
./spin.py --help

usage: spin-checker [-h] [-l] [-i LOOP_INTERVAL] [-s TWILIO_SID] [-t TWILIO_TOKEN] [-f SEND_FROM] [-n ...]

Spin Checker verifies whether the next week schedule for the Stride Spin Studio is available.

optional arguments:
  -h, --help            show this help message and exit
  -l, --loop            Run the check in a loop until the schedule is posted.
  -i LOOP_INTERVAL, --interval LOOP_INTERVAL
                        How often to check in seconds (requires loop mode)
  -s TWILIO_SID, --sid TWILIO_SID
                        Account SID for Twilio integration
  -t TWILIO_TOKEN, --token TWILIO_TOKEN
                        Auth token for Twilio integration
  -f SEND_FROM, --from SEND_FROM
                        Number to use as source for Twilio notifications
  -n ..., --numbers ...
                        List of phone numbers to send notifications to.
```
