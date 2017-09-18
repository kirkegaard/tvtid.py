import argparse
import os
import shutil
import sys
import urllib
import requests
import requests_cache

from datetime import date, datetime, timedelta
from dateutil import parser
from fuzzywuzzy import fuzz, process


class Schedule(object):

    def __init__(self, channel, programs=[]):
        self.channel = channel
        self.programs = programs

    def at(self, time):
        idx = 0
        aired, current, upcoming = None, None, None

        for index, program in enumerate(self.programs):
            if program.start_time <= time and program.stop_time >= time:
                idx = index
                break

        if idx != 0:
            aired = self.programs[:idx - 1]
            current = self.programs[idx]
            upcoming = self.programs[idx + 1:-1]

        return aired, current, upcoming


    def current(self):
        return self.at(datetime.now())


class Channel(object):

    icon = None
    logo = None
    logo_svg = None
    category = None
    region = None
    language = None

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def from_json(json):
        if json['id'] is None or json['title'] is None:
            return False

        channel = Channel(json['id'], json['title'])
        channel.icon = json.get('icon')
        channel.logo = json.get('logo')
        channel.logo_svg = json.get('svgLogo')
        channel.category = json.get('category')
        channel.region = json.get('region')
        channel.language = json.get('lang')

        return channel


class Program(object):

    start_time = None
    stop_time = None
    url = None
    channel_id = None
    category = None
    description = None
    production_year = None
    production_country = None
    teaser = None
    series_id = None
    series_info = None

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def from_json(json):
        if json['id'] is None or json['title'] is None:
            return False

        program = Program(json['id'], json['title'])

        program.start_time = datetime.fromtimestamp(json.get('start'))
        program.stop_time = datetime.fromtimestamp(json.get('stop'))
        program.url = json.get('url')
        program.channel_id = json.get('channelId')
        program.category = json.get('category')
        program.description = json.get('desc')
        program.production_year = json.get('prodYear')
        program.production_country = json.get('prodCountry')
        program.teaser = json.get('teaser')
        program.series_id = json.get('series_id')
        program.series_info = json.get('series')

        return program


class Client(object):

    # The API backend host.
    API_BASE_URI = 'http://tvtid-backend.tv2.dk/tvtid-app-backend'

    # The default HTTP request headers
    HTTP_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Accept': 'application/json, text/javascript'
    }

    # The default channels to return in a days schedule
    DEFAULT_CHANNELS = [1, 3, 5, 2, 31, 133, 7, 6, 4, 10155, 10154, 10153, 8,
                        77,   156,  10093,  10066,  14, 10089, 12566, 10111, 70,
                        118, 153, 94, 12948, 145, 185, 157, 15, 71, 93, 15049,
                        219, 37, 248]

    def __init__(self):
        requests_cache.install_cache('/tmp/tvtid_cache')

    def schedules_for(self, date=None, channels=None):
        channels = {k: self.channels()[k] for k in channels or self.DEFAULT_CHANNELS}
        channel_queries = urllib.parse.urlencode([("ch", cid) for cid in channels.keys()])
        endpoint = '%s/dayviews/%s' % (self.API_BASE_URI, date.strftime('%Y-%m-%d'))
        res = requests.get(endpoint, headers=self.HTTP_REQUEST_HEADERS, params=channel_queries)

        schedules = []
        for schedule in res.json():
            channel = channels[schedule.get('id')]

            programs = []
            for data in schedule['programs']:
                p = Program.from_json(data)
                p.channel_id = schedule.get('id')
                programs.append(p)

            schedules.append(Schedule(channel, programs))

        return schedules

    def schedules_for_today(self, channels=None):
        today = datetime.now()
        if datetime.now().hour >= 0 and datetime.now().hour <= 5:
            today = today - timedelta(days=1)
        return self.schedules_for(today, channels)

    def channel_schedule(self, channels):
        pass

    def channels(self):
        endpoint = '%s/channels' % self.API_BASE_URI
        res = requests.get(endpoint, headers=self.HTTP_REQUEST_HEADERS)
        return dict(map(lambda c: (c.get('id'), Channel.from_json(c)), res.json()))

    def get_program_details(self, program):
        endpoint = '%s/channels/%s/programs/%s' % (self.API_BASE_URI, program.channel_id, program.id)
        res = requests.get(endpoint, headers=self.HTTP_REQUEST_HEADERS)
        return Program.from_json(res.json())


def get_args(args):
    """Get the script arguments."""
    description = "tvtid - Feteches the tv schedule from client.dk"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-c", metavar="\"channel\"",
                     help="Sets the channel for the schedule")

    arg.add_argument("-d", metavar="\"date\"",
                     help="Sets the date for the schedule")

    return arg.parse_args(args)


def process_args(args):
    """Process args."""
    if not len(sys.argv) > 1:
        print("error: tvtid needs to be given arguments to run.\n"
              "       Refer to \"tvtid -h\" for more info.")
        sys.exit(1)

    client = Client()
    channels = client.channels()
    keys = {k: c.title for k, c in channels.items()}
    template = '[{start_time}] {title}\n'
    output = ''

    if not args.c:
        print('We need to know what channel you want the schedule for')
        sys.exit(1)

    key = process.extractOne(args.c, keys)
    output += 'Schedule for: %s\n' % key[0]

    if key is None:
        print('Couldnt find that channel')
        sys.exit(1)

    if args.d:
        date = parser.parse(args.d)
        output += 'Date: %s\n\n' % date.strftime("%Y-%m-%d")
        schedule = client.schedules_for(date, [key[2]])
        for program in schedule[0].programs:
            output += template.format(
                title=program.title,
                start_time=program.start_time.strftime('%H:%M'),
            )
    else:
        schedule = client.schedules_for_today([key[2]])
        output += 'Date: %s\n\n' % datetime.now().strftime("%Y-%m-%d")
        aired, current, upcoming = schedule[0].current()

        if current is None:
            output += 'Nothing is currently playing\n'
        else:
            output += template.format(
                title=current.title,
                start_time=current.start_time.strftime('%H:%M'),
            )

        if upcoming is None:
            output += 'No programs upcoming\n'
        else:
            for program in upcoming:
                output += template.format(
                    title=program.title,
                    start_time=program.start_time.strftime('%H:%M'),
                )

    print(output)


def main():
    """Main script function."""
    args = get_args(sys.argv[1:])
    process_args(args)


if __name__ == "__main__":
    main()
