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
#
from getpass import getpass


class User(object):
    def __init__(self, username, password):
        self.name = username
        self.password = password


def load_users(filename):
    users = dict()

    with open(filename, 'r') as f:
        for line in f:
            tmp = line.strip().split(':', 1) # [user, password]

            if tmp[0] not in users:
                users[tmp[0]] = User(username=tmp[0], password=tmp[1])

    return users


def is_authorized(filename, user):
    """
    PERMIT:username:filename
    DENY:username:filename
    PERMIT:username: -- user can access ALL files - ROOT
    PERMIT::filename -- ALL users can access file - UNIVERSAL
    DENY:username: -- user can access NO FILES
    DENY::filename: -- NO user can access file
    PERMIT:: -- ALL users can access ALL files
    DENY:: -- NO user can access ANY file

    first rule applies
    """
    auth_file = 'auth.txt'
    with open(auth_file, 'r') as f:
        for line in f:
            tmp = line.strip().split(':')
            if len(tmp) != 3:
                continue
            permission, username, fileline = tmp[0], tmp[1], tmp[2]

            # Rule does not apply
            if username and username != user:
                continue
            if fileline and fileline != filename:
                continue

            if permission == 'PERMIT':
                return True
            elif permission == 'DENY':
                return False
            else:
                continue

    return False


if __name__ == '__main__':
    import sys
    import os

    users = load_users('users.txt')

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
            user = users[username].name
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
            if not os.path.isfile(filename):
                print 'File \'%s\' does not exist' % (filename)
                continue

            if is_authorized(filename, user):
                try:
                    with open(filename, 'r') as f:
                        print f.read(),
                    continue
                except IOError:
                    print 'File %s does not exist' % (filename)
                    continue
            else:
                print 'Access to file %s denied' % (filename)
                continue
    except EOFError:
        print '\nThanks for playing.'
        sys.exit(0)

