# Intercept LaunchDarkly Events with Vector

## Usage
1. Clone this repo locally
1. In your terminal, run `curl --proto '=https' --tlsv1.2 -sSf https://sh.vector.dev | bash` to install Vector
1. Verify that it's working with `vector --version`
1. Run `export LD_SDK_KEY='YOUR-LD-SDK-KEY'`
1. Run `export LD_MOBILE_KEY='YOUR-LD-MOBILE-KEY`
1. Run `export LD_CLIENT_SIDE_ID='YOUR-CLIENT-SIDE-ID`
1. Run `vector --config vector.toml` to start Vector.

Leave that terminal instance running. This is the Vector service that's listening for LaunchDarkly events.

1. In a separate terminal window, navigate to your project directory
1. Run `export LD_SDK_KEY='YOUR-LD-SDK-KEY'` again
1. Run `python main.py`
1. Look in your Vector terminal window to ensure LaunchDarkly events were captured and printed by Vector.

If it ran successfully, you should see a `configuration` event, followed by `context` and `contextKeys` events.