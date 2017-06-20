import subprocess
import logging
import json
import time
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
es = Elasticsearch([{'host': '192.168.227.164', 'port': 9200}])


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
        res_id = result['host'].replace('.', '').replace('/', '')
        try:
            t = es.get(index='hosts', doc_type='typo', id=res_id)
        except:
            result['dateFirstAdded'] = current_time
        else:
            result['dateFirstAdded'] = t['_source']['dateFirstAdded']
        finally:
            result['latestRefresh'] = current_time
            es.index(index='ssl-scan', doc_type='typo', id=res_id, body=result )

if __name__ == '__main__':
    while True:
        logger.info('started scan')
        results = scan('all_domains')
        parse_and_send(results)



