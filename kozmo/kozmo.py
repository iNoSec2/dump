#!/usr/bin/python3

import re
import os
import sys
import socket
import warnings
import readline
import tempfile
from os import listdir

from core.colors import *
from core.tree import tree
from core.update import updater
from core.comparer import comparer
from core.requester import requester
from core.pluginizer import pluginizer

from plugins.bing import binger
from plugins.google import googler
from plugins.decodify import dcode
from plugins.encodify import encode
from plugins.wappalyzer import detect_tech
from plugins.waf_detector import detect_waf
from plugins.cms_detector import detect_cms
from plugins.findSubdomains import findsubdomains

from plugins import *

try:
    from urllib.parse import urlparse # for python3
except ImportError:
    input = raw_input
    from urlparse import urlparse # for python2

warnings.filterwarnings('ignore') # Disable SSL related warnings

default_headers = '''Host: $,
User-Agent: $,
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,
Accept-Language': en-US,en;q=0.5,
Accept-Encoding: gzip, deflate,
Connection: close,
DNT: 1,
Connection: close,
Upgrade-Insecure-Requests: 1,
Origin: '''

print('\n %sK o z m o    ^_^%s\n' % (blue, end))


####
# AutoComplete
###

commands = ['post ', 'detect ', 'use ', 'edit headers',
'show ', 'restart', 'decode ', 'encode ']

def completer(text, state):
    options = [x for x in commands if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

####
# Reads payloads from files
####

payloads = {}

def reader():
    path = sys.path[0] + '/db/'
    files = listdir(path)
    for file in files:
        with open(path + file, 'r') as f:
            payloads[file.replace('.txt', '')] = f.readlines()

reader()

####
# Uses nano for getting input
####

def editor(default=None):
    editor = 'nano'
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:
        if default:
            tmpfile.write(default)
            tmpfile.flush()

        child_pid = os.fork()
        is_child = child_pid == 0

        if is_child:
            os.execvp(editor, [editor, tmpfile.name])
        else:
            os.waitpid(child_pid, 0)
            tmpfile.seek(0)
            return tmpfile.read().strip()

####
# Prompts the user for entering URL
####

def getURL():
    target = input('%surl%s%s>%s ' % (idblue, ique, iblue, iend))
    if target.startswith('post '):
        url = target[5:]
        post_data = input('%sdata%s%s>%s ' % (idblue, ique, iblue, iend))
        return url, False, post_data
    else:
        url = target
        if not url.startswith('http'):
            url = 'http://' + url
        return url, True, ''

####
# Parses the url or POST data to extract parameters & their values
####

def getParams(url, data, GET):
    params = {}
    if GET:
        if '=' in url:
            data = url.split('?')[1]
            if data[:1] == '?':
                data = data[1:]
        else:
            data = ''
    parts = data.split('&')
    for part in parts:
        each = part.split('=')
        try:
            params[each[0]] = each[1]
        except IndexError:
            params = None
    return params

####
# Prompts the user for modifying headers
####

def getHeaders(prefill):
    return editor(prefill)

####
# Extractes header names & values
####

def extractHeaders(headers):
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers

####
# Handles response
####

def responseHandler(GET, current_value, current_param, url, inp, headers, hostname, params):
    if params:
        params[current_param] = inp
    new = requester(url, params, headers, hostname, GET)
    return new

####
# Display important information
####

def statusBar(o_status_code, o_headers, o_time, status_code, headers, time):
    changed_headers = []
    header_num = 0
    for o, n in zip(o_headers.values(), headers.values()):
        if o != n:
            changed_headers.append(list(o_headers.keys())[header_num])
        header_num += 1
    changed_headers = '|'.join(changed_headers)
    s_status = green_bar + white + str(status_code) + end
    s_time = green_bar + white + str(time) + end
    s_headers = green_bar + white + str(len(headers)) + end
    try:
        s_length = o_headers['content-length']
        new_length = headers['content-length']
    except KeyError:
        s_length, new_length = 'None', 'None'
    length = green_bar + white + str(s_length) + end
    if status_code != o_status_code:
        s_status = red_bar + white + str(status_code) + end
    if abs(time - o_time) > 1:
        s_time = red_bar + white + str(time) + end
    if len(changed_headers) != 0:
        s_headers = red_bar + white + changed_headers + end
    if s_length != new_length:
        length = red_bar + white + str(new_length) + end
    print('Status %s | Time %s | Headers %s | Content Length %s' % (s_status, s_time, s_headers, length))

####
# convert dict to a prettified string
####

def flatter(headers):
    flat_headers = []
    for header, value in zip(headers.keys(), headers.values()):
        flat_headers.append(header + ': ' + value)
    return '\n'.join(flat_headers)

####
# Returns payloads of the requested type
####

def getPayloads(payload_type):
    if payload_type in payloads:
        return payloads[payload_type]
    else:
        return False


####
# Prefilled input statement for URL tampering
####

def prefilledInput(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

####
# main console
####

def console(url, o_headers):
    GET = url[1]
    data = url[2]
    url = url[0]
    plain_url = False
    params = getParams(url, data, GET)
    try:
        current_param = list(params.keys())[0]
        current_value = list(params.values())[0]
        usable_inp = params[current_param]
    except AttributeError:
        current_param, current_value, usable_inp = '', '', ''
        plain_url = True
    headers = extractHeaders(o_headers)
    hostname = urlparse(url).hostname
    ip = socket.gethostbyname(hostname)
    original = requester(url, params, headers, hostname, GET)
    new = original
    statusBar(original[0], original[1], original[3], original[0], original[1], original[3])
    while True:
        if not plain_url:
            inp = input('%s%s%s>%s ' % (ired, current_param, iblue, iend))
        else:
            inp = prefilledInput('%s%s%s>%s ' % (ired, current_param, iblue, iend), url)
        if inp.startswith('switch '):
            current_param = inp[7:]
            current_value = params[current_param]
        elif inp.startswith('os '):
            os.system(inp[3:])
        elif inp == 'edit headers':
            headers = extractHeaders(getHeaders(flatter(headers)))
        elif inp == 'show headers':
            print(flatter(headers))
        elif inp == 'show rheaders':
            print(flatter(new[1]))
        elif inp == 'show tree':
            tree()
        elif inp == 'show params':
            print(flatter(params))
        elif inp.startswith('use '):
            pluginizer(new, original, params, ip, hostname, inp)
        elif inp.startswith('show '):
            inp = inp[5:]
            payloads = getPayloads(inp)
            for payload in payloads:
                print(payload.rstrip())
        elif inp.startswith('detect '):
            module = inp[7:]
            if module == 'cms':
                cms = detect_cms(hostname)
                if cms:
                    print(good + ' ' + cms)
                else:
                    print(bad + ' No CMS detected')
            elif module == 'tech':
                techs = detect_tech(url)
                if techs:
                    for tech in techs:
                        print (tech)
            elif module == 'waf':
                detect_waf(url, headers)
        elif inp == 'find subdomains':
            findsubdomains(hostname)
        elif inp == 'restart':
            start()
        elif inp == 'update':
            updater()
        elif inp.startswith('google '):
            googler(new, original, params, ip, hostname, inp)
        elif inp.startswith('bing '):
            binger(new, original, params, ip, hostname, inp)
        elif inp.startswith('decode '):
            dcode(inp[7:])
        elif inp.startswith('encode '):
            encode(inp[7:])
        else:
            if not plain_url:
                usable_inp = inp
                params[current_param] = inp
            else:
                url = inp
            new = responseHandler(GET, current_value, current_param, url, inp, headers, hostname, params)
            statusBar(original[0], original[1], original[3], new[0], new[1], new[3])
            diffs = comparer(original[2], new[2], inp)
            if diffs:
                for diff in diffs:
                    print (diff)

def start():
    console(getURL(), getHeaders(default_headers))
try:
    start()
except KeyboardInterrupt:
    quit()