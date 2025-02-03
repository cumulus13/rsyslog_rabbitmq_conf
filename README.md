# rsyslog for RabbitMQ (`omrabbitmq`) Config Maker

A command-line (CLI) tool to generate a `rabbitmq.conf` file for rsyslog with the `omrabbitmq` module activated.

## Usage

This tool allows you to create a new configuration file or automatically add a suffix number unless you use one of the following arguments:
- `-o` | `-q`: Overwrite an existing file.
- `-a`: Enable automatic numbering.

## Command-Line Usage

```bash
usage: make.py [-h] -n NAME -x EXCHANGE_NAME -t EXCHANGE_TYPE -r ROUTING_KEY -H HOST [-P PORT] [-v VIRTUAL_HOST] -u USERNAME -p PASSWORD [-d DURABLE] [-e DELIVERY_MODE] [-a AUTO_DELETE] [-q] [-o] [-A] [FILE]

positional arguments:
  FILE                  Full path of the output file. Default: current directory with the name 'rabbitmq.conf'.

options:
  -h, --help            Show this help message and exit.
  -n NAME, --name NAME  Name of the configuration.
  -x EXCHANGE_NAME, --exchange-name EXCHANGE_NAME
                        Name of the exchange.
  -t EXCHANGE_TYPE, --exchange-type EXCHANGE_TYPE
                        Type of the exchange.
  -r ROUTING_KEY, --routing-key ROUTING_KEY
                        Routing key.
  -H HOST, --host HOST  RabbitMQ host.
  -P PORT, --port PORT  Default: 5672.
  -v VIRTUAL_HOST, --virtual-host VIRTUAL_HOST
                        Virtual host. Default: "/".
  -u USERNAME, --username USERNAME
                        Username for RabbitMQ authentication.
  -p PASSWORD, --password PASSWORD
                        Password for RabbitMQ authentication.
  -d DURABLE, --durable DURABLE
                        Enable durable exchanges. Default: "on".
  -e DELIVERY_MODE, --delivery-mode DELIVERY_MODE
                        Delivery mode. Default: 2.
  -a AUTO_DELETE, --auto-delete AUTO_DELETE
                        Enable auto-delete. Default: "off".
  -q, --quiet           Overwrite an existing file.
  -o, --overwrite       Overwrite an existing file (same as "--quiet").
  -A, --auto            Automatically create files with sequential numbering.
```

## Support

- Python 2.7+, Python 3.x

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)

