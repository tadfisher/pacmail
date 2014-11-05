#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import fork, system, waitpid, path
import sys

class ProcessUpdate():

    def db_islocked(self):
        """Check if we already have a db lock"""		
        path_db = '/var/lib/pacman/db.lck'
        if path.isfile(path_db):
            return True

    def run_background(self,cmd):
        """ run_background(cmd) -> exit_status 

            Runs cmd in background, processing gtk events in the
            meanwhile. The function returns only when the command is
            done.
        """

        pid = fork()
        if pid == 0:
            sys.exit(system(cmd))

        (wpid, wstatus) = waitpid(pid, 0)
        if wpid == pid:
            return wstatus
