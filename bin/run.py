#!/usr/bin/env python

import argparse
import boto.ec2
import os
import simplejson
import subprocess
import sys
import time
import urllib2
import random

cli = argparse.ArgumentParser(description='Utility for mounting or unmounting a volume.')
cli.add_argument('action', help='Action to perform (i.e. attach, detach)')
cli.add_argument('volumeid', help='Volume ID (e.g. vol-abcd1234)')
cli.add_argument('--remap-device', help='Remap AWS device to a local name')
cli.add_argument('--env-file', help='Write mount environment variables file')
cli.add_argument('--env-prefix', help='Prefix for mount environment variables', default='MOUNT_')
cli.add_argument('--verbose', '-v', action='count', help='Use multiple times to increase verbosity: none = quiet, 1 = completions, 2 = summaries, 3 = details')

cliargs = cli.parse_args()


#
# setup our basics
#

devices = [
  '/dev/sdf',
  '/dev/sdg',
  '/dev/sdh',
  '/dev/sdi',
  '/dev/sdj',
  '/dev/sdk',
  '/dev/sdl',
  '/dev/sdm',
  '/dev/sdn',
  '/dev/sdo',
  '/dev/sdp',
]

devicesRemap = {
  'ubuntu' : {
    '/dev/sdf' : '/dev/xvdf',
    '/dev/sdg' : '/dev/xvdg',
    '/dev/sdh' : '/dev/xvdh',
    '/dev/sdi' : '/dev/xvdi',
    '/dev/sdj' : '/dev/xvdj',
    '/dev/sdk' : '/dev/xvdk',
    '/dev/sdl' : '/dev/xvdl',
    '/dev/sdm' : '/dev/xvdm',
    '/dev/sdn' : '/dev/xvdn',
    '/dev/sdo' : '/dev/xvdo',
    '/dev/sdp' : '/dev/xvdp',
  },
}

DEVNULL = open(os.devnull, 'w')

if cliargs.verbose > 2:
  TASK_STDOUT = None
  TASK_STDERR = None
else:
  TASK_STDOUT = DEVNULL
  TASK_STDERR = DEVNULL

ec2instance = simplejson.loads(urllib2.urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read())
ec2api = boto.ec2.connect_to_region(ec2instance['region'])


#
# verify we can/should mount
#

mounted = False

if cliargs.verbose > 1:
  sys.stderr.write('enumerating volumes...\n')

volumes = ec2api.get_all_volumes(filters = {
  'attachment.instance-id' : ec2instance['instanceId'],
})

for volume in volumes:
  if cliargs.verbose > 2:
    sys.stderr.write(' + %s -> %s\n' % ( volume.attach_data.device, volume.id ))

  if cliargs.volumeid == volume.id:
    mounted = volume

  devices = filter(lambda a: a != volume.attach_data.device, devices)

if cliargs.verbose > 0:
  sys.stderr.write('enumerated volumes\n')
  

#
# attach if necessary
#

if 'attach' == cliargs.action:
  if False == mounted:
    device = random.choice(devices)
    remapdevice = devicesRemap[cliargs.remap_device][device]

    if cliargs.verbose > 2:
      sys.stderr.write('remapping aws %s to local %s\n' % ( device, remapdevice ))

    if cliargs.verbose > 1:
      sys.stderr.write('physically mounting (%s)...\n' % device)

    ec2api.attach_volume(cliargs.volumeid, ec2instance['instanceId'], device)

    while True:
      statuscheck = ec2api.get_all_volumes([ volume.id ]).pop()

      if 'in-use' == statuscheck.status:
        break

      time.sleep(2)

    # just because aws says it's available, doesn't mean the os sees it yet

    while True:
      if 0 == subprocess.call('/sbin/fdisk -l %s | /bin/grep "%s"' % ( remapdevice, remapdevice ), shell=True, stdout=TASK_STDOUT, stderr=TASK_STDERR):
        break

      time.sleep(2)

    if cliargs.verbose > 0:
      sys.stderr.write('physically mounted (%s)\n' % device)
  else:
    device = mounted.attach_data.device
    remapdevice = devicesRemap[cliargs.remap_device][device]

  if None != cliargs.env_file:
    f = open(cliargs.env_file, 'w')
    f.write('%sDEVICE=%s\n' % ( cliargs.env_prefix, remapdevice ))
    f.close()

elif 'detach' == cliargs.action:
  if False != mounted:
    if cliargs.verbose > 1:
      sys.stderr.write('physically unmounting (%s)...\n' % mounted.attach_data.device)

    ec2api.detach_volume(mounted.id)

    while True:
      statuscheck = ec2api.get_all_volumes([ mounted.id ]).pop()

      if 'available' == statuscheck.status:
        break

      time.sleep(2)

    if cliargs.verbose > 0:
      sys.stderr.write('physically unmounted (%s)\n' % mounted.attach_data.device)
