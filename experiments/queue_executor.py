#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Jairo Sánchez
# @Date:   2018-01-22 21:39:14
# @Last Modified by:   Jairo Sánchez
# @Last Modified time: 2018-01-30 13:49:59

import os
import argparse
import csv
import queue
import threading
import subprocess
import signal
import fnmatch


class Progress(object):
    """Defines a synchronized counter to use as a multithreaded progress
       tracker. Makes increments of 1 for its internal counter (self.progress)
    """
    def __init__(self, total, initial_val=0):
        self.lock = threading.Lock()
        self.progress = initial_val
        self.completed_at = total

    def increment(self):
        with self.lock:
            self.progress += 1
            completed = (self.progress + 0.0) / (self.completed_at + 0.0)
            print('PROGRESS: {0}%'.format(completed * 100.0))


sim_queue = queue.Queue()
# ONE_EXECUTABLE = '/home/jairo/Software/the-one/one.sh'
ONE_EXECUTABLE = '/home/jairo/Software/one-scripts/experiments/random_wait.sh'
# TEMP_DIR = '/home/jairo/Simulaciones/config'
TEMP_DIR = '/home/jairo/test'
total_tasks = 0
finished_tasks = 0


def signal_handler(signum, frame):
    """Manages external signals (i.e. SIGTERM) to finish gracefully the
       current subprocesses in execution
    """
    global sim_queue
    global workers
    tasks_pending = sim_queue.qsize()
    for i in range(tasks_pending):
        task = sim_queue.get()
        print('Item {0} deleted: {1}'.format(task[0], task[1]))
        sim_queue.task_done()
        if task is None:
            print('Replacing None object')
            sim_queue.put(None)


def worker_thread(progress_tracker):
    """Worker thread, for each instance o
    """
    global ONE_EXECUTABLE
    global sim_queue
    while True:
        sim_item = sim_queue.get()
        if sim_item is None:
            break
        # Do the processing
        tmp_file = os.path.join(TEMP_DIR, '{0}.txt'.format(sim_item[0]))
        with open(tmp_file, 'w') as sim_file:
            sim_file.write(sim_item[1])

        completed = subprocess.run([ONE_EXECUTABLE, '-b', '50', tmp_file],
                                   cwd=os.path.dirname(ONE_EXECUTABLE))
        print('{0} returncode: {1}'.format(sim_item[0], completed.returncode))
        progress_tracker.increment()
        sim_queue.task_done()


def read_csv_parameters(csvfile):
    """ Parses a csv file into two lists, one with the parameter names and
        another with all the values that takes per run
    """
    col_names = []
    fields = []
    first_line = True
    with open(csvfile, 'r') as the_file:
        param_reader = csv.reader(the_file)
        for row in param_reader:
            if first_line:
                col_names = row
                first_line = False
                continue
            fields.append(row)

    return col_names, fields


def write_pid_file():
    pid = os.getpid()
    all_files = os.listdir('.')
    for f in fnmatch.filter(all_files, '*.pid'):
        print('Deleting {0}'.format(f))
        os.remove(f)

    with open('{0}.pid'.format(pid), 'wt') as pidfile:
        pidfile.write('{0}'.format(pid))


def main():
    global sim_queue
    global total_tasks
    global workers
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csvparam',
                        type=str,
                        help='CSV Parameter list', required=True)
    parser.add_argument('-w', '--workers',
                        type=int, required=True,
                        help='Number of worker threads to spawn')
    args = parser.parse_args()
    if not os.path.isfile(args.csvparam):
        print("ERROR: {0} is not a valid file".format(args.csvparam))
        exit(1)

    if args.workers <= 0:
        print("ERROR: Number of workers must be greater than 0")
        exit(4)

    names, values = read_csv_parameters(args.csvparam)
    if len(values) == 0:
        print("ERROR: No values found in the  file.")
        exit(2)

    if len(names) != len(values[0]):
        print("ERROR: Parameter names doesn't match with the available values")
        exit(3)

    # Saves the pid of this (parent) process in the same directory
    write_pid_file()

    # Register the signal handler
    signal.signal(signal.SIGTERM, signal_handler)

    workers = args.workers
    index = 0
    for row in values:
        sim_config = ''
        for config_i in range(len(row)):
            sim_config = sim_config + '{0}={1}\n'.format(names[config_i],
                                                         row[config_i])
        print('Task Added: {0}'.format([index, sim_config]))
        sim_queue.put([index, sim_config])
        index = index + 1

    threads = []
    prog = Progress(sim_queue.qsize())
    for t in range(args.workers):
        thread = threading.Thread(target=worker_thread, args=(prog, ))
        thread.start()
        threads.append(thread)

    sim_queue.join()

    for i in range(args.workers):
        sim_queue.put(None)
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
