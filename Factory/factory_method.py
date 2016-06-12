import abc
import urllib.request as urllib2
from bs4 import BeautifulSoup

__author__ = 'agerasym'

# Abstract classes

class Connector(metaclass=abc.ABCMeta):
    """
    Abstract class to connect to remoter resources

    """

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self, content):
        """
        This method should be redefined at runtime
        """
        pass

    def read(self, host, path):
        """
        A generic method for all subclasses, read web content
        """
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print('Connecting to ', url)
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        """
        A factory method, must be redefined in subclass
        :return:
        """
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        """
        A factory method, must be redefined in subclass
        :return:
        """
        pass


class Port(metaclass=abc.ABCMeta):
    """
    Abstract port, will become concrete in its childs
    """

    @abc.abstractmethod
    def __str__(self):
        pass


# Concrete classes

# Connectors
class HTTPConnector(Connector):
    """
    A concrete connector that creates a HTTP connector
    and sets in runtime all its attributes

    """

    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        """
        Here HTTPPort and HTTPSecurePort are concrete objects
        created by factory method
        :return:
        """
        if self.is_secure:
            return HTTPSSecurePort()
        return HTTPPort()

    def parse(self, content):
        """
        Parses web content
        :param content:
        :return: list of file names
        """

        filenames = []
        soup = BeautifulSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(str(link))
        return '\n'.join(filenames)


class FTPConnector(Connector):
    """
    A concrete creator that crates a FTP connector
    and sets in runtime all its attributes
    """

    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = str(content).split('\n')
        filenames = []

        for line in lines:
            # The ftp format typically has 8 column, split them
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])

        return '\n'.join(filenames)

# Ports
class HTTPSSecurePort(Port):
    def __str__(self):
        return '443'


class HTTPPort(object):
    def __str__(self):
        return '80'


class FTPPort(object):
    def __str__(self):
        return '21'


def main():
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD'

    protocol = \
        input(('Connecting to {}. Which protocol'
               'to use? (0-http, 1-ftp)'.format(domain)))

    if int(protocol) == 0:
        is_secure = bool(int(input('Use secure connection? (1-yes, 0-no): ')))
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)
    try:
        content = connector.read(domain, path)
    except urllib2.URLError:
        print('cannot access resources with this method')
    else:
        print(connector.parse(content))

if __name__ == '__main__':
    main()
