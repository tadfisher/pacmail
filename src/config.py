import ConfigParser

class PacMailConfig(object):
    def parse_config(self, path, defaults):
        parser = ConfigParser.RawConfigParser(defaults)
        parser.read(path)

        config = {}

        try:
            # Daemon config
            config['check_interval'] = parser.getint('Daemon', 'check_interval')
            config['description'] = parser.getboolean('Daemon', 'description')
            config['changelog'] = parser.getboolean('Daemon', 'changelog')
            # Mail config
            config['sender'] = parser.get('Mail', 'sender')
            config['recipient'] = parser.get('Mail', 'recipient')
            config['smtp_host'] = parser.get('Mail', 'smtp_host')
            config['smtp_port'] = parser.getint('Mail', 'smtp_port')
            config['smtp_auth'] = parser.get('Mail', 'smtp_auth')
            config['smtp_user'] = parser.get('Mail', 'smtp_user')
            config['smtp_pass'] = parser.get('Mail', 'smtp_pass')
        except ConfigParser.NoSectionError:
            print "Malformed/missing config file."
            exit(1)

        return config
