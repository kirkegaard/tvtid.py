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
