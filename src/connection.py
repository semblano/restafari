import output
import json
import sys
import urllib.parse
import http.client


def getRequest(id, conf):
    db = conf['db']
    headers = conf['headers']
    test = db[id]
    method = test['method'].upper()
    fullpath = conf['path'] + test['path']
    desc = test['desc']
    params = ''
    server = conf['domain'] + ':' + conf['port']
    try:
        conn = http.client.HTTPConnection(server)
    except IOError as err:
        conf['errors'].append("Server " + server + " not found!")
        output.validationError(conf)
        sys.exit(1)

    if method == 'GET':
        conn.request(method, fullpath)
    else:
        params = urllib.parse.urlencode(test['data'])
        res = conn.request(method, fullpath, params, headers)
    res = conn.getresponse()

    data = res.read().decode("utf-8").strip()
    if len(data) > 60:
        data = data[0:60] + '...'
    output.printRequest(method,
                        conf['domain'],
                        fullpath,
                        params,
                        desc,
                        data,
                        res.status)

    result = {}
    result['status'] = res.status
    result['header'] = res.getheaders()

    try:
        result['data'] = json.loads(data)
    except ValueError:
        print("Invalid JSON outout")
    # finally:
    #   result['data'] = None

    return result
