#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import os
import argparse

dirPath='/etc/'
listDirConfig=[
	'rc0.d',
	'rc1.d',
	'rc2.d',
	'rc3.d',
	'rc4.d',
	'rc5.d',
	'rc6.d',
	'rcS.d',
]


def get_enable_daemon():
	"""Obtenir la liste des daemons actifs."""
	global dirPath
	global listDirConfig
	activeDaemon = []

	for d in listDirConfig:
		for ad in os.listdir(dirPath+d):
			if ad[0] == 'S' and not ad in activeDaemon:
				activeDaemon.append(ad)

	return activeDaemon


def get_disable_daemon():
	"""Obtenir la liste des daemons actifs."""
	global dirPath
	global listDirConfig
	activeDaemon = [x[3:] for x in get_enable_daemon()]
	inactiveDaemon = []

	for d in listDirConfig:
		for ad in os.listdir(dirPath+d):
			if ad[0] == 'K' and not ad[3:] in activeDaemon:
				if not ad in inactiveDaemon:
					inactiveDaemon.append(ad)

	return inactiveDaemon

	
def set_disable_daemon(daemons):
	"""Désactiver les daemons passés en argument."""
	global listDirConfig
	global dirPath
	enableDaemon=get_enable_daemon()

	for nameDaemon in daemons:
		exist =False

		for ed in enableDaemon:
			if nameDaemon == ed[3:]:
				nameDaemon = ed
				exist = True
				break

		if not exist:
			continue

		for dc in listDirConfig:
			if nameDaemon in os.listdir(dirPath+dc):
				os.rename(
					dirPath + dc + '/' + nameDaemon, 
					dirPath + dc + '/K' + nameDaemon[1:]
				)
		os.system('update-rc.d {} defaults 2> /dev/null'.format(nameDaemon[3:]))
		print('* {} [disabled]'.format(nameDaemon[3:]))


def set_enable_daemon(daemons):
	"""Activer les daemons passés en argument."""
	global listDirConfig
	global dirPath
	disableDaemon=get_disable_daemon()

	for nameDaemon in daemons:
		exist=False

		for ed in disableDaemon:
			if nameDaemon == ed[3:]:
				nameDaemon, exist=ed, True
				break

		if not exist:
			continue

		for dc in listDirConfig:
			if nameDaemon in os.listdir(dirPath+dc):
				os.rename(
					dirPath+dc+'/'+nameDaemon, 
					dirPath+dc+'/S'+nameDaemon[1:]
				)
		os.system('update-rc.d {} defaults 2> /dev/null'.format(nameDaemon[3:]))
		print('* {} [enabled]'.format(nameDaemon[3:]))


def display_daemon(listDaemon):
	"""Afficher proprement la liste de daemons actifs."""
	print()

	for d in sorted([x[3:] for x in listDaemon]):
		print('* {}'.format(d))
 

def change_now(listDaemon, action):
	from subprocess import Popen, PIPE

	for d in listDaemon:
		cmd=Popen(['service', d, action], stdout=PIPE, stderr=PIPE)
		stdout, stderr=cmd.communicate()

		if stderr:
			print(stderr)


def have_right():
	"""Savoir si le script est lancé avec les bons droits."""
	global listDirConfig
	global dirPath
	access = True

	for d in listDirConfig:
		if not os.access(dirPath+d, os.W_OK):
			access = False
			break

	if not access:
		print('Permission denied (use sudo).')

	return access


if __name__ == '__main__':
	parser=argparse.ArgumentParser(prog='dsda')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-n', '--now', action='store_true',
		help='enable or disable daemon immediatly (service <daemon> start/stop)')
	parser.add_argument('-d', '--disable', nargs='*', 
		help='daemons to disable at boot (without arg, display disabled daemon)')
	parser.add_argument('-e', '--enable', nargs='*', 
		help='daemons to enable at boot (without arg, display enable daemon)')

	args = parser.parse_args()

	if args.disable != None:
		if len(args.disable) >= 1:
			if have_right():
				set_disable_daemon(args.disable)
				if args.now:
					change_now(args.disable, 'stop')
		else:
			display_daemon(get_disable_daemon())

	elif args.enable != None:
		if len(args.enable) >= 1:
			if have_right():
				set_enable_daemon(args.enable)
				if args.now:
					change_now(args.enable, 'start')
		else:
			display_daemon(get_enable_daemon())
	else:
		parser.print_help()

