# VLESS Key/Link to XRay-config Converter (parser)

• Simple Python tool to convert VLESS URLs and subscription links into ready-to-use XRay configuration files. 

• Easy to use, no extra dependencies. Ideal for quickly generating XRay configs from various input formats.

## Features:

• Supports parsing both single VLESS links (keys) and base64-encoded subscriptions with Reality protocol parameters. 

• Generates configs with handling of `sni`, `fp`, `pbk`, `sid` parameters.

• No dependencies on Docker or other complex tools.

## Installation and Usage:

1. Download the script 'parser.py' and save it in your XRay config folder (e.g. '~/.config/xray/').
2. Create a file 'input.txt' in the same folder and put your VLESS URL or subscription link inside.
3. Run the script:
   
   python3 ./parser.py
   
4. The generated config will be saved as xray_config.json

### License:
GPLv3
