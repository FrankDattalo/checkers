import os
import importlib
import signal
import time

class SignalStopper(object):

    def __init__(self, sig=signal.SIGINT):
         signal.signal(sig, self._handler)
         self.hold_count = 0
         self._was_interrupted = False

    def _handler(self, ignore2, ignore3):
        self._was_interrupted = True

    def __enter__(self):
        self.hold_count += 1

    def __exit__(self, ignore1, ignore2, ignore3):
        self.hold_count -= 1
        if self.hold_count == 0 and self._was_interrupted:
            raise InterruptedError()
    
no_interrupt = SignalStopper()


def reload(lib):
    importlib.reload(lib)


def clear():
    if os.sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def unzip(iter):
    X = []
    Y = []
    for x, y in iter:
        X.append(x)
        Y.append(y)
    return X, Y


def choose(message, options):
    n = len(options)
    reverse_lookup = []
    choice = -1
    while True:
        clear()
        print(message)
        for index, key in enumerate(options):
            reverse_lookup.append(key)
            if index == 0:
                print('DEFAULT {}) - {}'.format(index, key))
            else:
                print('        {}) - {}'.format(index, key))
        print()
        choice = input('>>> ')
        try:
            if len(choice) == 0:
                choice = 0
                break
            choice = int(choice)
            if choice < 0 or choice >= n:
                print('Invalid Choice ', end='')
                continue
        except ValueError:
            print('Invalid Format ', end='')
            continue
        break
    return options[reverse_lookup[choice]]


class Timer(object):

    def __init__(self):
        self._start = 0
        self.reset()
    
    def reset(self):
        self._start = time.clock()

    def elapsed(self):
        end = time.clock()
        return end - self._start

    def eta(self, current, total):
        if current == 0:
            current += 1

        seconds = self.elapsed()
        seconds_per_run = seconds / current
        remaining_runs = total - current
        remaining_seconds = remaining_runs * seconds_per_run
        minutes = remaining_seconds / 60
        hours = minutes / 60
        days = hours / 24
        return 'ETA: {} days, {} hours, {} minutes, {} seconds'.format(
            round(days), 
            round(hours) % 24, 
            round(minutes) % 60, 
            round(remaining_seconds) % 60)
    