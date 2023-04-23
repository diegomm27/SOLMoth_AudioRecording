import pyaudio
import wave
import os
import struct
import math
import time


SHORT_NORMALIZE = (1.0/32768.0)
THRESHOLD = 500  # Adjustable value for recording sound
RECORD_DURATION = 5  # Record for 5 seconds
DIRECTORY_PATH = '.'  # Current directory
CHANNELS = 2
FS = 44100
CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16


class Recorder:
    """
    A class to record sound from microphone and save it to a WAV file.
    """

    @staticmethod
    def rms(frame):
        """
        Calculate Root Mean Square value of given audio frame.

        Args:
            frame: A byte string representing audio data.

        Returns:
            rms: Root Mean Square value of the given audio frame.
        """
        count = len(frame) / CHUNK
        format = "%dh" % count
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 100

    def __init__(self):
        """
        Constructor method to initialize Recorder class.
        """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=SAMPLE_FORMAT, channels=CHANNELS, rate=FS, input=True, output=True, frames_per_buffer=CHUNK)

    def record(self):
        """
        Start recording sound from microphone and save it to a WAV file.

        Returns:
            None
        """
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + RECORD_DURATION

        while current <= end:
            data = self.stream.read(CHUNK)
            if self.rms(data) >= THRESHOLD:
                end = time.time() + RECORD_DURATION

            current = time.time()
            rec.append(data)

        self.write(b''.join(rec))

    def write(self, recording):
        """
        Write recorded sound to a WAV file.

        Args:
            recording: A byte string representing recorded sound.

        Returns:
            None
        """
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(DIRECTORY_PATH, '{}.wav'.format(timestr))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(recording)
        wf.close()

        print('Written to file: {}'.format(filename))
        print('Returning to listening')

    def listen(self):
        """
        Start listening to sound from microphone.

        Returns:
            None
        """
        print('Listening beginning')
        while True:
            input = self.stream.read(CHUNK)
            rms_val = self.rms(input)
            if rms_val > THRESHOLD:
                self.record()
