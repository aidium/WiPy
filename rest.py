import socket
import re

__pattern = re.compile('http://([a-zA-Z0-9\\.]+)(.*)')

def parseUrl(url):
    match = __pattern.search(url);
    host = match.group(1)
    resource = match.group(2) if match.group(2) != '' else '/'
    return (host, resource)

def sendRequest(host, port, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(socket.getaddrinfo(host, port)[0][4])

    #print(request)
    s.sendall(request)
    
    data = s.recv(20480).decode('utf-8')
    s.close()

    #print(data)
    
    return (data[9:12], data.split('\r\n\r\n')[1:])

def get(url, accept = 'application/json, text/html, text/plain, */*', port = 80):
    host, resource = parseUrl(url)

    request = 'GET ' + resource + ' HTTP/1.1\r\n' + \
              'Host: ' + host + '\r\n' + \
              'Accept: ' + accept + '\r\n\r\n'
    
    return sendRequest(host, port, request)

def post(url, data, port = 80):
    host, resource = parseUrl(url)

    request = 'POST ' + resource +' HTTP/1.1\r\n' + \
              'Host: ' + host + '\r\n' + \
              'Content-Type: application/x-www-form-urlencoded\r\n' + \
              'Content-Length: ' + str(len(data)) + '\r\n\r\n' + \
              data + '\r\n\r\n'

    return sendRequest(host, port, request)
