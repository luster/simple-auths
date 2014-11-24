simple-auths
============

Simple Authentication and Authorization Framework

Allow authentication for users based on `users.txt` consisting of entries `username:password` and authorization for basic read permissions on files in `auth.txt` consisting of entries `PERMISSION:username:filename` with PERMISSION being PERMIT or DENY. Omission of `username` applies to ALL users accessing `filename`. Similarly, omission of `filename` applies to ALL files accessed by `user`.

This code was written for ECE305 Computer Security, Fall 2014 at The Cooper Union.
