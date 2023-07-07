# you should protect this endpoint with 
# a http server that can do authentication
# so only your SDK keys are allowed
# we can attach the authorization header to the event
# and use that for routing to the appopriate sink

# this example assumes you are routing only one SDK key to vector and only event schema 4
# other events should be directly proxied to LD
[sources.incoming_ld_server_side_sdk_events]
type = "http_server"
address = "0.0.0.0:8080"
decoding.codec = "json"
headers = ["authorization", "X-LaunchDarkly-Event-Schema", "user-agent"]
method = "POST"
path="/"
strict_path = false



[transforms.ld_sdk_event_route]
type = "route"
inputs = ["incoming_ld_server_side_sdk_events"]
route.forward_to_ld = '.kind != "feature" || .inExperiment == true || .path == "/diagnostic"'
route.export_from_ld = '.kind != "summary"' 

[transforms.ld_sdk_events_clean]
type = "remap"
inputs = ["ld_sdk_event_route.forward_to_ld"]
source = '''
del(.authorization)
del(.source_type)
del(.timestamp)
del(.path)
del(."X-LaunchDarkly-Event-Schema")
del(."user-agent")
'''


[transforms.ld_sdk_forward_route]
type = "route"
inputs = ["ld_sdk_events_clean"]
route.bulk = '.kind != "diagnostic" && .kind != "diagnostic-init"'
route.diagnostic = '.kind == "diagnostic" || .kind == "diagnostic-init"'

[sinks.ld_server_side_sdk_bulk]
type = "http"
inputs = ["ld_sdk_forward_route.bulk"]
encoding.codec = "json"
method = "post"
uri = "http://events.launchdarkly.com/bulk"
request.headers.authorization = "${LD_SDK_KEY:?err}"
request.headers.x-launchdarkly-event-schema = "4"
batch.max_events = 1000
batch.timeout_secs = 5

[sinks.ld_server_side_sdk_diagnostic]
type = "http"
inputs = ["ld_sdk_forward_route.diagnostic"]
encoding.codec = "json"
method = "post"
uri = "https://events.launchdarkly.com/diagnostic"
request.headers.authorization = "${LD_SDK_KEY:?err}"
request.headers.x-launchdarkly-event-schema = "4"
batch.max_events = 100
batch.timeout_secs = 5


[transforms.ld_sdk_events_export]
type = "remap"
inputs = ["ld_sdk_event_route.export_from_ld"]
source = '''
.sdkLast6, err = slice(.authorization, -6)
.ld_event_schema_version = del(."X-LaunchDarkly-Event-Schema")
del(.authorization)
'''



# These are the events we want to send to a data destination
[sinks.out]
  inputs         = ["ld_sdk_events_export"]
  type           = "console"
  encoding.codec = "json"
