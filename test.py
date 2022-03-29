#!/usr/bin/env python3

import os
import platform
import socket
import subprocess
import tempfile
import time

import pymonetdb


def start_mserver(dbname, monetdbdir, farmdir, port):
    exe = os.path.join(monetdbdir, 'bin', 'mserver5')
    if platform.system() == 'Windows':
        exe += '.exe'
    dbpath = os.path.join(farmdir, dbname)
    try:
        os.mkdir(dbpath)
    except FileExistsError:
        pass
    #
    env = dict((k, v) for k, v in os.environ.items())
    path_components = [
        os.path.join(monetdbdir, "bin"),
        os.path.join(monetdbdir, "lib", "monetdb5"),
        env['PATH'],
    ]
    env['PATH'] = os.pathsep.join(path_components)
    sets = dict(
        prefix=monetdbdir,
        exec_prefix=monetdbdir,
        mapi_port=port,
    )
    cmdline = [
        exe,
        f'--dbpath={dbpath}',
    ]
    for k, v in sets.items():
        cmdline.append('--set')
        cmdline.append(f'{k}={v}')
    print()
    print('Starting mserver')
    print(f'PATH={env["PATH"]}')
    print(f'cmdline: {cmdline!r}0')
    t0 = time.time()
    verbose = t0 + 1
    proc = subprocess.Popen(cmdline, env=env, close_fds=True)
    #
    while True:
        try:
            code = proc.wait(timeout=0.1)
            exit(f'mserver unexpectedly exited with code {code}')
        except subprocess.TimeoutExpired:
            if os.path.exists(os.path.join(dbpath, '.started')):
                break
            t = time.time()
            if t >= verbose:
                print(f"Waited for {t - t0:.1f}s")
                verbose = t + 1
            if t > t0 + 30.1:
                print("Starting mserver took too long, giving up")
                proc.kill()
                exit("given up")
    print('mserver has started')
    return proc


db_name = 'demo'
db_port = 54321
proc = start_mserver(db_name, '/home/jvr/monets/Jan2022/inst', '/tmp/jvr/bla', db_port)
try:
    conn = pymonetdb.connect(db_name, host='localhost', port=db_port)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM environment")
    for k, v in cursor.fetchall():
        print(f"{k:>32}  {v}")
finally:
    if proc.returncode is None:
        print('Killing the server')
        proc.kill()
    else:
        print('Server has already terminated')

