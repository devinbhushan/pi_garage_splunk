import json
import requests
from settings import Settings

class SplunkHCEClient(object):

    def __init__(self):
        settings = Settings()
        hosts_str = settings.get_field('SplunkHCE', 'hosts')
        index_token = settings.get_field('SplunkHCE', 'index_token')
        if hosts_str and index_token:
            hosts = [host.strip() for host in hosts_str.split(',')]
            self.splunk_urls = ['https://%s:8088/services/collector/event' % host for host in hosts]
            self.headers = {'Authorization': 'Splunk %s' % index_token}
            for splunk_url in self.splunk_urls:
                print("Splunk HCE Connected to Sensor Index: splunk_url=%s, headers=%s" % (splunk_url, self.headers))
        else:
            raise Exception("Unable to read host or token values!")

    def send_event(self, out):
        event = {'event': out}
        body = json.dumps(event).encode('ascii')
    
        return [requests.post(url=splunk_url,
                              headers=self.headers,
                              data=body,
                              verify=False,
                              timeout=10) for splunk_url in self.splunk_urls]
