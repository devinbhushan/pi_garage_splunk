import time
from splunk_hce_client import SplunkHCEClient
from settings import Settings
from lxml.html import parse


class IotEmitter(object):

    def __init__(self):
        settings = Settings()
        self.url = settings.get_field('IOT', 'source_url')
        print "IOT source_url=%s" % self.url

    def get_sensor_values(self):
        doc = parse(self.url).getroot()
        vars = doc.find_class('var')
        dict = {}
        for tr in vars:
            values = tr.find_class('vartable_static_field updatable readonly')
            if values:
                value = str(values[0].text_content().strip())

            names = tr.find_class('vartable_static_field readonly')
            if names:
                name = str(names[0].text_content().replace('"', ''))

            if value and name:
                dict[name] = value

        if dict:
            dict['time'] = int(round(time.time()))

        return dict

    def get_sensor_output_event(self):
        sensor_values = self.get_sensor_values()
        return sensor_values

    def get_computed_output_event(self):
        sensor_values = self.get_sensor_values()
        sensor_values.pop('Sensor_P8_Count')
        sensor_values.pop('Sensor_P8_Proximity')
        return sensor_values

def run():
    iot_emitter = IotEmitter()
    hce_client = SplunkHCEClient()
    while True:
        try:
            sensor_out = iot_emitter.get_sensor_output_event()
            print("Sensor Event: %s" % sensor_out)
            response = hce_client.send_event(sensor_out, SplunkHCEClient.EventType.Sensor)
            print("Sensor Response: %s" % response)

            computed_out = iot_emitter.get_computed_output_event()
            print("Computed Event: %s" % computed_out)
            response = hce_client.send_event(computed_out, SplunkHCEClient.EventType.Computed)
            print("Computed Response: %s" % response)
            
            time.sleep(1)
        except Exception as e:
            print("Exception: %s" % str(e))


def main():
    run()


if __name__ == '__main__':
    main()
