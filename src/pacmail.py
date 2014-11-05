#!/usr/bin/env python

import sys, time
from socket import getfqdn
from daemon import Daemon
from config import PacMailConfig
from updatechecker import UpdateChecker
from mailer import Mailer

defaults = {
    'check_interval': 86400,
    'description': True,
    'changelog': True,
    'sender': 'pacmail@%s' % getfqdn(),
    'recipient': 'pacmail@%s' % getfqdn(),
    'smtp_host': getfqdn(),
    'smtp_port': 25,
    'smtp_auth': 'none',
    'smtp_user': 'pacmail',
    'smtp_pass': ''
}

config_path = '/etc/pacmail.conf'

class PacMail(Daemon):
    
    def run(self):
        # Get config
        config = PacMailConfig().parse_config(config_path, defaults)
        mailer = Mailer(config)
        checker = UpdateChecker()

        while True:
            # Grab updates
            checker.sync_db()
            updates = checker.get_updates()
            # Send email
            if updates is not None and len(updates) > 0:
                mailer.send(updates)
            # Sleep
            time.sleep(config['check_interval'])
            
if __name__ == "__main__":
    daemon = PacMail('/var/run/pacmail.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'test' == sys.argv[1]:
            daemon.run()
        else:
            print "Unknown option: %s\n" % sys.argv[1]
            print "Usage: %s {start|stop|restart|test}" % sys.argv[0]
        sys.exit(0)
    print "Usage: %s {start|stop|restart|test}" % sys.argv[0]
    sys.exit(2)
