#!/usr/bin/python3
'''
title: Pushbullet from command linke
author: qkzk
date: 2020/02/24
'''
import argparse
import sys
from pathlib import Path
# self
from tokens import APIKEY, PHONENAME
# community
from pushbullet import Pushbullet


def create_pb_object():
    '''returns the pushbullet object. Default if your phone can't be found'''
    pushbullet = Pushbullet(api_key=APIKEY)
    return find_phone(pushbullet)


def find_phone(pushbullet):
    '''Try to find your phone'''
    for device in pushbullet.devices:
        if PHONENAME in device.nickname:
            return device
    return pushbullet


class PushBulletSender:
    '''Wrapper for pushbullet push methods'''

    def __init__(self, pushbullet):
        self.pushbullet = pushbullet

    def send_link(self, link: str = None, description: str = None) -> dict:
        '''send a link to your phone'''
        if description is None:
            description = ""
        if link is None:
            raise ValueError(
                "You must provide a link : -l https://example.com")
        return self.pushbullet.push_link(description, link)

    def send_note(self, body: str = None, title: str = None) -> dict:
        '''send a note to your phone'''
        if body is None:
            raise ValueError("You must provide a body : -n hello")
        if title is None:
            title = body
        return self.pushbullet.push_note(title, body)

    def send_file(self, filepath: str, name: str = None) -> dict:
        '''send a local file to your phone'''
        if name is None:
            name = Path(filepath).name
        with open(filepath, "rb") as uploaded_file:
            file_data = self.pushbullet.upload_file(uploaded_file, name)

        return self.pushbullet.push_file(**file_data)

    def send_uploaded_file(self,
                           file_url: str,
                           file_type: str = None,
                           file_name: str = None):
        '''send an uploaded file to your phone'''
        if file_name is None:
            file_name = file_url.split("/")[-1]
        if file_type is None:
            file_type = guess_mime_type(file_url)
            if file_type == "":
                raise ValueError("Couldn't guess the file type, can't send !")
        return self.pushbullet.push_file(file_url=file_url,
                                         file_name=file_name,
                                         file_type=file_type)


def guess_mime_type(file_url: str) -> str:
    '''try to guess the mimetype of an uploaded file from its name'''
    mimetype = ""
    if file_url.endswith("jpg") or file_url.endswith("jpeg"):
        mimetype = "image/jpeg"
    elif file_url.endswith("png"):
        mimetype = "image/png"
    elif file_url.endswith("txt") or file_url.endswith("md") or file_url.endswith("py"):
        mimetype = "text/plain"
    elif file_url.endswith("mp4"):
        mimetype = "video/mp4"
    elif file_url.endswith("mp3"):
        mimetype = "audio/mpeg"
    elif file_url.endswith("pdf"):
        mimetype = "application/pdf"
    return mimetype


def parse_args():
    '''argument parser'''
    parser = argparse.ArgumentParser(
        description="Send a note, a link or a file to your phone",
        prog='pushbullet')

    parser.add_argument("-d", "--description",
                        type=str,
                        help="-d My message "
                        "Description of what you send")
    parser.add_argument("-t", "--type",
                        type=str,
                        help="-t image/jpeg "
                        "- The filetype of uploaded_file")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("-l", "--link",
                        type=str,
                        help="-l https://qkzk.xyz. "
                        "- The link you want to send")
    action.add_argument("-u", "--url",
                        type=str,
                        help="-u https://i.imgur.com/IAYZ20i.jpg "
                        "- The url of the file you want to send")
    action.add_argument("-p", "--path",
                        type=str,
                        help="-p /home/bob/hello.txt "
                        "- The path of the file to send")
    action.add_argument("-n", "--note",
                        type=str,
                        help="-n blablabla... "
                        "- The body of your note")
    action.add_argument("--TESTS",
                        action="store_true",
                        help="Tests the functions")

    args = parser.parse_args()
    return args


def push(pushbullet: PushBulletSender, args) -> dict:
    '''action taken depending of parsed arguments'''
    if args.TESTS:
        test()
        return {}
    if args.link:
        return pushbullet.send_link(args.link, args.description)
    if args.path:
        return pushbullet.send_file(args.path, args.description)
    if args.url:
        return pushbullet.send_uploaded_file(args.link, args.type,
                                             args.description)
    if args.note:
        return pushbullet.send_note(args.note, args.description)
    return {}


def main():
    '''main program : parse arguments, create PB object, push notification'''
    args = parse_args()
    pushbullet = create_pb_object()
    pb_sender = PushBulletSender(pushbullet)
    response = push(pb_sender, args)
    print(response)


def test():
    '''test everything tests'''
    test_args()
    test_pushbullet()
    test_send_file()
    test_send_link()
    test_send_note()
    sys.exit(0)


def test_args():
    '''test reading the args'''
    args = parse_args()
    assert args is not None


def test_pushbullet():
    '''test creating the pushbullet object'''
    pushbullet = create_pb_object()
    assert pushbullet is not None


def test_send_link():
    '''sending a link'''
    pushbullet = create_pb_object()
    pb_sender = PushBulletSender(pushbullet)
    assert pb_sender.send_link(
        link="https://qkzk.xyz", description="qkzk") != {}


def test_send_note():
    '''send a note'''
    pushbullet = create_pb_object()
    pb_sender = PushBulletSender(pushbullet)
    assert pb_sender.send_note(body="body", title="title") != {}


def test_send_file():
    '''send a local file'''
    pushbullet = create_pb_object()
    pb_sender = PushBulletSender(pushbullet)
    assert pb_sender.send_link(link="./hello.txt", description="salut") != {}


def test_send_uploaded_file():
    '''send an uploaded file'''
    pushbullet = create_pb_object()
    pb_sender = PushBulletSender(pushbullet)
    assert pb_sender.send_uploaded_file(
        file_url="https://i.imgur.com/IAYZ20i.jpg",
        file_type="image/jpeg",
        file_name="cat.jpg") != {}


if __name__ == "__main__":
    main()
