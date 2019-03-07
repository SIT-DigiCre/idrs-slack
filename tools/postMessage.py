#!/usr/bin/env python3

import os
import sys
from slackclient import SlackClient

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
sc.api_call("chat.postMessage", channel = sys.argv[1], text = sys.argv[2])
