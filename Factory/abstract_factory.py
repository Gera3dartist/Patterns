import abc
from urllib import request as urrlib2
from bs4 import BeautifulSoup

__author__ = 'agerasym'


# create abstract factory
# will use later for factories and products
class AbstractFactory(metaclass=abc.ABCMeta):
    def __init__(self, is_secure=False):
        self.is_secure = is_secure

    @abc.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def create_parser(self):
        pass


# The HTTPFactory class creates its family of related objects:
# HTTPPort, HTTPSecurePort and HTTPParser
# Whereas FTPFactory creates FTPPort and FTPParser
class HTTPFactory(AbstractFactory):
    def create_parser(self):
        return HTTPParser()

    def create_port(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def create_protocol(self):
        if self.is_secure:
            return 'https'
        return 'http'


class FTPFactory(AbstractFactory):
    def create_port(self):
        return FTPPort()

    def create_protocol(self):
        return 'ftp'

    def create_parser(self):
        return FTPParser()


# abstract parser
class Port(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    def __str__(self):
        return '443'


class FTPPort(Port):
    def __str__(self):
        return '21'

# abstract parser
class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, content):
        pass


class HTTPParser(Parser):
    def __call__(self, content):
        filenames = []
        soup = BeautifulSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link.text)
        return '\n'.join(filenames)


class FTPParser(Parser):
    def __call__(self, content):
        lines = str(content).split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


# Connector is a class that accepts factory and this factory is used to inject
# the components protocol, port and method to parser
class Connector(object):
    """A client"""
    def __init__(self, factory: AbstractFactory):
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parse = factory.create_parser()

    def read(self, host, path):
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print('Connecting to ', url)
        return urrlib2.urlopen(url, timeout=2).read()


def main():
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'
    
    protocol = input('Connecting to {}. Select protocol: 0-http, 1-ftp'.format(domain))
    if int(protocol) not in [0,1]:
        print('Sorry, wrong answer')
        return

    if int(protocol) == 0:
        is_secure = bool(int(input('Use secure conn? (1-yes, 0-no)')))
        factory = HTTPFactory(is_secure=is_secure)
    else:
        factory = FTPFactory()


    # create connector based on factory
    connector = Connector(factory)
    try:
        content = connector.read(domain, path)
    except urrlib2.URLError:
        print('Cannot access resource with this method')
    else:
        print(connector.parse(content))


if __name__ == '__main__':
    main()









































