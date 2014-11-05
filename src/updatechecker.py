#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import popen
from re import compile, split, sub, findall, M
from process import ProcessUpdate

class UpdateChecker:
    def add_info(self, updates):
        for idx, pkg in enumerate(updates):
            info = popen('LC_ALL="C" pacman -Qi %s' % pkg['package']).read().strip()
            description = findall('^Description    :.*', info, M)[0].split(': ')[1]
            installed = findall('^Version        :.*', info, M)[0].split(': ')[1]
            changelog = popen('LC_ALL="C" pacman -Qc %s' % pkg['package']).read().strip()
            if '' == changelog:
                changelog = 'No changelog entries found.'
            updates[idx]['installed'] = installed
            updates[idx]['description'] = description
            updates[idx]['changelog'] = changelog

    def cut_packages(self, targets_list):
        pkgs = []
        for item in targets_list:
            pkg, ver = split('-(?=\d)', item, 1)
            pkgs.append({'package': pkg, 'version': ver})
        return pkgs

    def get_updates(self):
        command = popen('LC_ALL="C" pacman -Qu | egrep -vi "^(Checking|warning|Remove|Total)"').read().strip()
        if compile('Targets \(.*\):').match(command,0):
            targets_list = sub('Targets \(.*\):','',command).split()
            updates = self.cut_packages(targets_list)
            self.add_info(updates)
            return updates
        else:
            return None
        
    def get_totaldownload(self):
        print _('Getting total download size')
        command = popen('LC_ALL="C" pacman -Qu | egrep -i ^"Total Download Size"').read().strip()
        return  command.split(':')[1].strip()

    def sync_db(self):
        if not ProcessUpdate().db_islocked():
            ProcessUpdate().run_background('sudo pacman -Sy')

