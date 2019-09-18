from email_helper import email_utils
import os
import json
import re
import collections
import datetime
import pandas


def send_wrangling_email(job, options):

    job_name = job["Props"]["Name"]
    job_id = job["_id"]
    receiver_address_list = ['egrana@thespastudios.com', "asierra@thespastudios.com", "jsoler@thespastudios.com"]
    subject = 'AutoWrangling - {} autowranglered'.format(job_name)
    text = "Job {} with id {} has been autowranglered with the following options:\n {}".format(job_name, job_id, str(options))
    sender_address = None

    email_utils.sendEmail(receiver_address_list, sender_address, subject, text, None)


def time_to_seconds(hour, minutes):
    return hour*3600 + minutes * 60


def seconds_to_time(seconds):
    date = str(datetime.timedelta(seconds=seconds))
    hour, min, secs = date.split(":")
    return hour, min


def export_rule(name, rule_info):
    path = os.path.join("T:/framework/settings/wrangling", "{}.json".format(name))
    with open(path, 'w') as outfile:
        json.dump(rule_info, outfile, indent=4)
    return path


def decode_json(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def get_chunk_frames(chunks, frame_range):
    range = list()
    single = list()
    regex = re.compile(r"((?P<range>\d+-\d+)|(?P<single>\d+))")
    for match in regex.finditer(frame_range): 
        groups = match.groupdict()
        range_group = groups.get("range")
        single_group = groups.get("single")
        if range_group:
            first_frame, last_frame = range_group.split("-")
            range.append(int(last_frame)-int(first_frame) + 1)
        if single_group:
            single.append(single_group)

    range_chunk_frames = sum(range)/float(chunks)
    if not range_chunk_frames.is_integer():
        range_chunk_frames = int(range_chunk_frames) + 1

    return range_chunk_frames
    # range_chunk_frames += len(single)


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.iteritems():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source    


def get_excel_data(excel_file):
    excel_dataframe = pandas.read_excel(excel_file)
    return excel_dataframe

    
if __name__ == "__main__":
    priority_excel = "C:/Users/asierra/Downloads/priority.xlsx"
    excel_dataframe = get_excel_data(priority_excel)
    excel_dataframe