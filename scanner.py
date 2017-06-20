import subprocess
import logging
import json
import time
import sys, getopt
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
es = Elasticsearch([{'host': '192.168.227.164', 'port': 9200}])

opts, args = getopt.getopt(sys.argv[1:],"",["hostfile="])
opts_dict = dict(opts)
HOSTFILE = opts_dict['--hostfile']


def scan(hostfile):
    args = ' '.join(["./ssllabs-scan --ignore-mismatch=true --hostfile=%s " % hostfile])
    ans = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    ans.poll()
    data = ans.communicate()
    logger.debug(data)
    results = json.loads(data[0].decode('utf-8'))
    return results


def parse_and_send(results):
    for result in results:
        logger.debug(result)
        if result['status'] == 'ERROR':
            return result
        try:
            for key in result['endpoints'][0]:
                result[key] = result['endpoints'][0][key]
                #result.pop('endpoints')
            details = result['endpoints'][0]['details']
            result['certNotAfter'] = details['cert']['notAfter']
            result['certNotBefore'] = details['cert']['notBefore']
            result['endpointsLength'] = len(result['endpoints'])
        except:
            logger.error('some keys havent been found [%s]' % str(result['host']))
        current_time = int(round(time.time() * 1000))
        result['latestRefresh'] = current_time
        es.index(index='ssl-scan', doc_type='typo', body=result )

if __name__ == '__main__':
    while True:
        logger.info('started scan')
        results = scan(HOSTFILE)
        parse_and_send(results)



