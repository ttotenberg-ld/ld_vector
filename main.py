import json
import ldclient
from ldclient.config import Config
import os


'''
Set sdk_key and feature_flag_key, then initialize the LD client.
'''
sdk_key = os.environ['LD_SDK_KEY']
feature_flag_key = "vector-test" # NOTE: The flag must have 'send detailed events' enabled in its settings
ldclient.set_config(Config(sdk_key,events_uri='http://0.0.0.0:8080'))


'''
Load the contexts used for this, evaluate the flag for each context, flush events, and shut down the SDK
'''
data = json.load(open("data/contexts.json"))

if __name__ == '__main__':
    for i in data:
        feature = ldclient.get().variation(feature_flag_key, i, False)
    ldclient.get().flush()
    ldclient.get().close()