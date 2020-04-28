
# Author: Terry Cox
# GitHub: https://github.com/KeckObservatory/KeckKeywordInterface
# Email: tcox@keck.hawaii.edu, tfcox1703@gmail.com

__author__ = ['Terry Cox', 'Luca Rizzi']
__version__ = '1.0.1'
__email__ = ['tcox@keck.hawaii.edu', 'tfcox1703@gmail.com', 'lrizzi@keck.hawaii.edu']
__github__ = 'https://github.com/KeckObservatory/KeckKeywordInterface'

import requests
import datetime
class Keywords(object):
    '''
    This class is strucutured to read the keywords from Keck instruments

    ***

    Attributes
    ----------
    _servers : list
        A list of servers to receive correct keyword (server that is correlated to the keyworks in '_keywords').
    _keywords : list
        A list of keywords to get value.
    _mode : str
        The vechical at which a keyword is to be obtained.

    Methods
    -------
    get_keywords()
        The method to get all the keywords in '_keywords' from servers in '_servers' and returns a dictionary of the values.
    get_keyword(server, keyword)
        The method to get fetch a single keyword.
    server_up(server, keyword)
        Checks to see if the server is up and will return a boolean.
    get_keyword_history(server, keyword, time, label='')
        The method to get the history of the given keyword
    ping_computer(instrument, server)
        The method to ping a computer to make sure the computer given has a heartbeat (will return a boolean)
    ps_process(instrument, process)
        The method to check to see if a process is running or not (will return a boolean)
    '''

    def __init__(self, servers=None, keywords=None, mode='web'):

        if keywords is None:
            keywords = []
        if servers is None:
            servers = []

        try:
            should_be_int = len(servers)
            if isinstance(servers, str):
                print('\'servers\' need to be a list of strings.')
                exit()
            if should_be_int > 0:
                if not isinstance(servers[0], str):
                    print('\'servers\' need to be a list of strings.')
                    exit()
        except:
            print('\'servers\' need to be a list of strings.')
            exit()

        try:
            should_be_int = len(keywords)
            if isinstance(keywords, str):
                print('\'keywords\' need to be a list of strings.')
                exit()
            if should_be_int > 0:
                if not isinstance(keywords[0], str):
                    print('\'keywords\' need to be a list of strings.')
                    exit()
        except:
            print('\'keywords\' need to be a list of strings.')
            exit()

        if len(servers) != len(keywords):
            print('\'servers\' (length = %s) and \'keywords\' (length = %s) need to be the same size.'%(len(servers), len(keywords)))
            exit()

        if not mode in ['web', 'local', 'ktlpython', 'simulate']:
            print('\'mode\' must be one of the following: web, local, ktlpython, or simulate.')
            print('Resetting to \'web\'...')
            mode = 'web'

        self._servers = servers
        self._keywords = keywords
        self._mode = mode

    def get_keywords(self):
        '''
        The method to get all the keywords in '_keywords' from servers in '_servers' and returns a dictionary of the values.

        Returns
        -------
        dict
            A dictionary with the keys as the keywords in list '_keywords' and the values as the values of the keywords.
        '''
        counter = 0
        keyword_dict = dict()
        for pname in self._keywords:
            server = self._servers[counter]
            if pname[0:6] == 'uptime':
                pname = pname[0:6]
                if self.server_up(server, pname):
                    keyword_dict.update({pname+server : '1'})
                else:
                    keyword_dict.update({pname+server : '0'})
            elif pname == 'TESTINT':
                if self.server_up(server, pname[:-1]):
                    keyword_dict.update({pname : '1'})
                else:
                    keyword_dict.update({pname : '0'})
            else:
                if self.server_up(server, pname[:-1]):
                    keyword_dict.update({pname : self.__find_keyword(server, pname[:-1])})
            counter += 1
        return keyword_dict

    def get_keyword(self, server, keyword):
        '''
        The method to get fetch a single keyword.

        Parameters
        ----------
        server : str
            the server at which the keyword will be located.
        keyword : str
            the keyword that is being requested

        Returns
        -------
        str
            returns a string of the keyword value
        '''
        if self.server_up(server, keyword):
            return self.__find_keyword(server, keyword)
        else:
            print("Error in getting data from the server \'%s\' reading keyword \'%s\'" % (server, keyword))
            return -8675309

    def __find_keyword(self, server, keyword):
        '''
        The private function to go get the keyword value.

        Parameters
        ----------
        server : str
            the server at which the keyword will be located.
        keyword : str
            the keyword that is being requested

        Returns
        -------
        str
            returns a string of the keyword value
        '''
        if self._mode == 'local':
            proc = subprocess.Popen("show -terse -s %s %s " % (server, keyword), stdout=subprocess.PIPE, shell=True)
            result = proc.communicate()
        elif self._mode == 'ktlpython':
            proc = ktl.cache(server, keyword)
            result = proc.read()
        elif self._mode == 'web':
            url = 'http://host.docker.internal:5002/show?server=%s&keyword=%s' % (server, keyword)
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print("Error in getting data from the server \'%s\' reading keyword \'%s\'" % (server, keyword))

            result = response.json()
        elif self._mode == 'simulate':
            return 164
        return result

    def server_up(self, server, keyword):
        '''
        Checks to see if the server is up.  (This is mostly used before asking for a keyword.)

        Parameters
        ----------
        server : str
            the server at which the keyword will be located.
        keyword : str
            the keyword that is being requested

        Returns
        -------
        boolean
            returns whether or not the server is up.
        '''
        try:
            temp = self.__find_keyword(server, keyword)
            return True
        except:
            return False

    def get_keyword_history(self, server, keyword, time, label=''):
        '''
        The method to get the history of the given keyword.

        Parameters
        ----------
        server : str
            the server at which the keyword will be located.
        keyword : str
            the keyword that is being requested
        time : str
            the time of how far back what is being looked at ('second', 'day', 'week', 'month', etc.)
        label : str, optional (default = '')
            the label of for the keyword history values.

        Returns
        -------
        dict
            returns as dictionary of x (keyword value) and y (timestamp of value) lists.
        '''
        data = {'x' : [], 'y' : [], 'name' : label}
        if(self.server_up(server, keyword)):
            url = 'http://host.docker.internal:5002/showHistory?server=%s&keyword=%s&time=%s' % (server, keyword, time)
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print("Error in getting data from the server \'%s\' reading keyword \'%s\'" % (server, keyword))
                return data
            result = response.json()
            if(result[:6] == 'unable'):
                return data

            for row in result.split("\\n"):
                if len(row) == 0:
                    return data
                if row[0] == "#":
                    return data
                if row[0] == ' ':
                    continue
                x, y = row.split(",")
                x = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
                data["x"].append(x)
                data['y'].append(float(y))
        return data

    def ping_computer(self, instrument, server):
        '''
        The method to ping a computer to make sure the computer given has a heartbeat (will return a boolean)

        Parameters
        ----------
        instrument : str
            the instrument in the server is contained
        server : str
            the server in which is in question of being up.

        Returns
        -------
        boolean
            returns whether or not their is a heartbeat to the server.
        '''
        #*******************************************************************************
        # Once show -s kcwi_ping is a thing, UNCOMMENT and COMMENT the BOTTOM
        #*******************************************************************************
        # result = self.get_keyword('%s_ping'%(instrument), server)
        # thresh = 20
        # resultTime = datetime.datetime.strptime(result, '%Y-%m-%dT%H:%M:%S.%f')
        # if resultTime < datetime.datetime.now()-datetime.timedelta(seconds=thresh):
        #     return True
        # else:
        #     return False
        #*******************************************************************************
        url = 'http://host.docker.internal:5002/ping?server=%s' % (server)
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print("Error in getting data from the server \'%s\' reading keyword \'%s\'" % (server, keyword))

        result = response.json()

        if result == "":
            return False
        else:
            return True

    def ps_process(self, instrument, process):
        '''
        The method to ping a computer to make sure the computer given has a heartbeat (will return a boolean)

        Parameters
        ----------
        instrument : str
            the instrument in the server is contained
        process : str
            the process in which is in question of running.

        Returns
        -------
        boolean
            returns whether or not the process is running from the given instrument.
        '''
        if self.get_keyword('%s_ps'%(instrument), process) == "":
            return False
        else:
            return True
