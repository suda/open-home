# -*- coding: utf-8 -*-
import json
import subprocess
import tempfile
import wave
import audioop
import os
import urllib2
import time
from collections import deque
from pprint import pprint

import pyaudio
import requests

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
# The threshold intensity that defines silence signal (lower than).
THRESHOLD = 180
# Silence limit in seconds. The max amount of seconds where only silence is recorded.
# When this time passes the recording finishes and the file is delivered.
SILENCE_LIMIT = 2
# We need a WAV to FLAC converter.
FLAC_CONV = '/usr/local/bin/flac'
LANG_CODE = 'pl-PL'

API_URL = 'http://0.0.0.0:9876/api/v1/'
KEYWORD = 'darek'
ON_COMMAND = u'włącz'
OFF_COMMAND = u'wyłącz'

groups = []

def load_groups():
    global  groups
    request = requests.get(API_URL + 'group/')
    groups = request.json()

def listen_for_speech():
    """
    Does speech recognition using Google's speech recognition service.
    Records sound from microphone until silence is found and save it as WAV and then converts it to FLAC.
    Finally, the file is sent to Google and the result is returned.
    """

    # Open stream
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print "* listening. CTRL+C to finish."
    samples = []
    chunks_per_second = RATE / CHUNK
    # 2s buffer for checking sound is louder than threshold
    silence_buffer = deque(maxlen=SILENCE_LIMIT * chunks_per_second)
    # Buffer used to append data before detection
    samples_buffer = deque(maxlen=SILENCE_LIMIT * RATE)

    started = False

    while (True):
        data = stream.read(CHUNK)
        silence_buffer.append(abs(audioop.avg(data, 2)))
        samples_buffer.extend(data)
        if (True in [x > THRESHOLD for x in silence_buffer]):
            if (not started):
                print "starting record"
                started = True
                samples.extend(samples_buffer)
                samples_buffer.clear()
            else:
                samples.extend(data)


        elif (started == True):
            print "finished"
            # The limit was reached, finish capture and deliver
            stream.stop_stream()
            hypotheses = submit_samples(samples, audio)
            parse(hypotheses)
            # Reset all
            stream.start_stream()
            started = False
            silence_buffer.clear()
            samples = []
            print "listening ..."

    print "* done recording"
    stream.close()
    audio.terminate()


def submit_samples(data, audio):
    filename = tempfile.mkdtemp() + 'output_' + str(int(time.time()))
    # Write data to WAVE file
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    # Convert to flac
    FNULL = open(os.devnull, 'w')
    subprocess.call([FLAC_CONV, '-f', filename + '.wav'], stdout=FNULL, stderr=subprocess.STDOUT)
    f = open(filename + '.flac', 'rb')
    flac_contents = f.read()
    f.close()
    map(os.remove, (filename + '.flac', filename + '.wav'))

    # Post it
    google_speech_url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&pfilter=2&lang=%s&maxresults=6' % (
    LANG_CODE)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7',
        'Content-type': 'audio/x-flac; rate=%i' % RATE
    }

    request = urllib2.Request(google_speech_url, data=flac_contents, headers=headers)
    output = urllib2.urlopen(request).read()
    if output is not None:
        output = output.split("\n")[0]

    try:
        response = json.loads(output)
        return response['hypotheses']
    except:
        pprint(output)
        return None

def parse(hypotheses):
    if len(hypotheses) == 0:
        return

    most_sure = hypotheses[0]['utterance'].lower()
    kind = -1
    group_id = -1
    # Test keyword
    if most_sure.startswith(KEYWORD):
        most_sure = ' '.join(most_sure.split(' ')[1:])

        # Test command
        if most_sure.startswith(ON_COMMAND):
            kind = 1
        elif most_sure.startswith(OFF_COMMAND):
            kind = 2

        # Search for group
        for group in groups:
            if group['name'].lower() in most_sure:
                group_id = group['id']
                break

        if kind != -1 and group_id != -1:
            request = requests.post(API_URL + 'command/', data={
                'kind': kind,
                'group': group_id
            })
            print u'%s command sent to %s' % ('On' if kind == 1 else 'Off', group['name'])
        else:
            print u'Unknown command "%s"' % most_sure

if (__name__ == '__main__'):
    load_groups()
    listen_for_speech()