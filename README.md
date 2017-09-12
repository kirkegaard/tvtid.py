# TVTid

This is a Python library for interfacing with the unofficial API on `tvtid.tv2.dk`.

## Installation

`pip install tvtid`

## CLI

To get the schedule off a channel from now and forward

```bash
$ tvtid -c tv2
Schedule for: TV 2
Date: 2017-09-12

[21:25] Fogeden kommer
[22:00] Nyhederne, Sporten og Vejret
[22:27] Regionale nyheder
...
```

To get the schedule at a specific date

```bash
$ tvtid -c dr1 -d '14. september'
Schedule for: DR1
Date: 2017-09-14

[05:15] Udsendelsesophør - DR1
...
[04:40] Kender du typen 2013
```

## Library Example
```python
import tvtid

client = tvtid.Client()
schedules = client.schedules_for_today()
channel_length = max(len(c.title) for c in client.channels().values())

for schedule in schedules:
    channel = schedule.channel
    aired, current, upcoming = schedule.current()

    if current:
        title = channel.title.ljust(channel_length, ' ')
        print('\n%s [%s] %s ' % (title, current.start_time.strftime('%H:%M'), current.title), end='')
        for program in upcoming[:3]:
            print('[%s] %s ' % (program.start_time.strftime('%H:%M'), program.title), end='')

# TV 2          [20:00] Fuld plade [21:15] Baby Surprise [23:05] Obsessed
# DR1           [20:00] X Factor [21:00] TV AVISEN [21:15] Vores vejr
# TV 2 Charlie  [20:30] Fede Finn i modvind [21:25] Fede Finn i modvind [22:15] En sag for Frost
# DR2           [20:45] VM håndbold: Kroatien-Norge, direkte [21:20] VM håndbold: Studiet [21:35] VM håndbold: Kroatien-Norge, direkte
# TV3           [20:00] Dagens mand [21:00] American Pie 2 [23:10] The Joneses
# …
```

## License
`tvtid` is published under the MIT license which can be read in the `LICENSE` file.
