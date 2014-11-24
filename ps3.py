#!/usr/bin/env python
#
#
#   Author: Ethan Lusterman
#   Created 11/23/2014
#
#   The Cooper Union
#   ECE305 Computer Security
#   Fall 2014
#   Professor Jeff Hakner
#
#   ps3
from getpass import getpass

class File(object):
    def __init__(self, filename):
        self.name = filename
        self.allow_all = False
        self.deny_all = False
        self.allow = dict()
        self.deny = dict()

    def __str__(self):
        return self.name

class User(object):
    def __init__(self, username, password):
        self.name = username
        self.password = password
        self.allow_all = False
        self.deny_all = False

def load_users(filename):
    users = dict()

    with open(filename, 'r') as f:
        for line in f:
            tmp = line.strip().split(':', 1) # [user, password]

            if tmp[0] not in users:
                users[tmp[0]] = User(username=tmp[0], password=tmp[1])

    return users

def load_auth(filename, users):
    """
    PERMIT:username:filename
    DENY:username:filename
    PERMIT:username: -- user can access ALL files - ROOT
    PERMIT::filename -- ALL users can access file - UNIVERSAL
    DENY:username: -- user can access NO FILES
    DENY::filename: -- NO user can access file

    In the case of a conflict, permit takes precedence over deny.
    For example, ROOT can access file even if file is DENY all.
    """
    files = dict()

    with open(filename, 'r') as f:
        for line in f:
            tmp = line.strip().split(':') # [permission, username, filename]
            if len(tmp) != 3:
                continue

            if tmp[0] == 'PERMIT':
                perm = 1
            elif tmp[0] == 'DENY':
                perm = 0
            else:
                continue
            username = tmp[1]
            if username and username not in users:
                continue

            filename = tmp[2]
            if filename and filename not in files:
                files[filename] = File(filename)

            if not username and not filename:
                continue

            if not username:
                if perm:
                    files[filename].allow_all = True
                else:
                    files[filename].deny_all = True

            if not filename:
                if perm:
                    users[username].allow_all = True
                else:
                    users[username].deny_all = False

            if username and filename:
                if perm:
                    files[filename].allow[username] = True
                else:
                    files[filename].deny[username] = True

    return files

if __name__ == '__main__':
    import sys

    users = load_users('users.txt')
    files = load_auth('auth.txt', users)

    tries = 0
    auth = False

    while tries < 3 and not auth:
        username = raw_input('Username: ')
        password = getpass(prompt='Password: ')

        if username not in users:
            print 'Login incorrect'
            tries += 1
            continue

        if users[username].password == password:
            user = users[username]
            auth = True
        else:
            print 'Login incorrect'

        tries += 1

    if tries == 3 and not auth:
        print 'Permission denied.'
        sys.exit(1)

    try:
        while True:
            filename = raw_input('Filename: ')

            curfile = files.get(filename, None)
            if not curfile:
                print 'File %s does not exist' % (filename)
                continue

            if user.allow_all or \
                    user.name in curfile.allow or \
                    curfile.allow_all:
                try:
                    with open(filename, 'r') as f:
                        print f.read(),
                    continue
                except IOError:
                    continue

            if user.deny_all or \
                    user.name not in curfile.allow or \
                    user.name in curfile.deny or \
                    curfile.deny_all:
                print 'Access to file %s denied' % (filename)
                continue
    except EOFError:
        print '\nThanks for playing.'
        sys.exit(0)

