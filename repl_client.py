import logging
import queue
import socket
from threading import Thread, Event

import tutkain.bencode as bencode


class ReplClient(object):
    '''
    Here's how ReplClient works:

    1. Open a socket connection to the given host and port.
    2. Start a worker that gets items from a queue and sends them over the
       socket for evaluation.
    3. Start a worker that reads bencode strings from the socket,
       parses them, and puts them into a queue.

    Calling `halt()` on a ReplClient will stop the background threads and close
    the socket connection. ReplClient is a context manager, so you can use it
    with the `with` statement.
    '''
    connection = None
    user_session = None
    plugin_session = None

    def connect(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(15)
        self.connection.connect((host, port))
        logging.debug({'event': 'socket/connect', 'host': host, 'port': port})

    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                logging.debug({'event': 'socket/disconnect'})
            except OSError as e:
                logging.debug({'event': 'error', 'exception': e})

    def __init__(self, host, port):
        self.connect(host, port)
        self.input = queue.Queue()
        self.output = queue.Queue()
        self.stop_event = Event()

    def go(self):
        Thread(daemon=True, target=self.eval_loop).start()
        Thread(daemon=True, target=self.read_loop).start()

        # https://nrepl.org/nrepl/building_clients.html#_basics
        self.input.put({'op': 'clone'})
        plugin_session = self.output.get().get('new-session')
        self.plugin_session = plugin_session
        logging.debug({'event': 'new-session/plugin', 'id': plugin_session})

        self.input.put({'op': 'clone'})
        user_session = self.output.get().get('new-session')
        self.user_session = user_session
        logging.debug({'event': 'new-session/user', 'id': user_session})

        self.input.put({'op': 'describe', 'session': plugin_session})

    def __enter__(self):
        self.go()
        return self

    def eval_loop(self):
        while True:
            item = self.input.get()
            if item is None:
                break

            print(bencode.write(item))
            self.connection.sendall(bencode.write(item))

        logging.debug({'event': 'thread/exit', 'thread': 'eval_loop'})

    def read_loop(self):
        try:
            while not self.stop_event.wait(0):
                item = bencode.read(self.connection)
                logging.debug({'event': 'read', 'item': item})

                self.output.put(item)
        except OSError as e:
            logging.debug({'event': 'error', 'exception': e})
        finally:
            # If we receive a stop event, put a None into the queue to tell
            # consumers to stop reading it.
            self.output.put_nowait(None)
            logging.debug({'event': 'thread/exit', 'thread': 'read_loop'})

    def halt(self):
        # Feed poison pill to input queue.
        if self.input is not None:
            self.input.put(None)

        # Trigger the kill switch to tell background threads to stop reading
        # from the socket.
        if self.stop_event is not None:
            self.stop_event.set()

        self.connection = None
        self.user_session = None
        self.plugin_session = None
        self.disconnect()

    def __exit__(self, type, value, traceback):
        self.halt()