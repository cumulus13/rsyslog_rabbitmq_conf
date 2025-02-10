#!/usr/bin/env python3

import sys
import os
if os.getenv('DEBUG'):
    from ctraceback import CTraceback
    sys.excepthook = CTraceback()
    from ctraceback.custom_traceback import console
else:
    from rich.console import Console
    console = Console()
    
import argparse
from pathlib import Path
from rich.syntax import Syntax
import shutil

def maker():
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', nargs='?', help="Full path of file output, default is current dir with name 'rabbitmq.conf'")
    parser.add_argument('-n', '--name', required=True)
    parser.add_argument('-x', '--exchange-name', default='syslog', required=True)
    parser.add_argument('-t', '--exchange-type', default='fanout', required=True)
    parser.add_argument('-r', '--routing-key', default='syslog.all', required=True)
    parser.add_argument('-H', '--host', default='192.168.100.2', required=True)
    parser.add_argument('-P', '--port', help='default: 5672', type=int, default=5672)
    parser.add_argument('-v', '--virtual-host', help='default: "/"', default="/")
    parser.add_argument('-u', '--username', default='root', required=True)
    parser.add_argument('-p', '--password', default='root', required=True)
    parser.add_argument('-d', '--durable', help='default: "on"', default='on')
    parser.add_argument('-e', '--delivery-mode', help='default: "persistent"', default="persistent" )
    parser.add_argument('-a', '--auto-delete', help='default: "off"', default="off")
    parser.add_argument('-q', '--quite', help = 'Overwrite any file', action = 'store_true')
    parser.add_argument('-o', '--overwrite', help = 'Overwrite any file, same as "--quite"', action = 'store_true')
    parser.add_argument('-A', '--auto', help = 'Auto create file with sequence', action = 'store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        return
    else:
        args = parser.parse_args()
        FILE = args.FILE
        # if not args.FILE or not os.path.isfile(str(args.FILE)):
        #     FILE = Path.cwd() / 'rabbitmq.conf'
        # if FILE.is_file():
            # if args.quite or args.overwrite:
            #     FILE = Path.cwd() / 'rabbitmq.conf'
        if args.auto:
            n = 1
            while 1:
                if FILE.is_file():
                    FILE = Path(FILE).parent / f'rabbitmq{n}.conf'
                    n+=1
                else:
                    break
        elif (args.overwrite or args.quite) and Path(FILE).is_file():
            FILE = args.FILE
        else:
            q = console.input(f"[warning]'{FILE.__str__()}[/]' [error]is exits[/], [critical]auto create new/overwrite/read[/] ([alert]y[/]/[#FFAAFF bold]n[/]/[error]o[/]/[#00FFFF]r[/]): ")
            if q and q.lower() in ['y', 'yes']:
                n = 1
                while 1:
                    if FILE.is_file():
                        FILE = Path(FILE).parent / f'rabbitmq{n}.conf'
                        n+=1
                    else:
                        break
            elif q and q.lower() in ['o', 'overwrite']:
                FILE = args.FILE
            elif q and q.lower() in ['r', 'read']:
                console.print(Syntax(open(str(FILE), 'r').read(), "c#", theme = 'fruity', line_numbers=True, tab_size=2, code_width=shutil.get_terminal_size()[0], word_wrap = True))
                return
        
        CONFIG_STR = f'''
template(name="json" type="list") {{
    constant(value="{{")
    constant(value="\\\"tag\\\":\\\"") constant(value="{args.name}") constant(value="\\\",")
    constant(value="\\\"msg\\\":\\\"") property(name="msg" format="json") constant(value="\\\",")
    constant(value="\\\"rawmsg\\\":\\\"") property(name="rawmsg" format="json") constant(value="\\\",")
    constant(value="\\\"hostname\\\":\\\"") property(name="hostname") constant(value="\\\",")
    constant(value="\\\"fromhost\\\":\\\"") property(name="fromhost") constant(value="\\\",")
    constant(value="\\\"fromhost-ip\\\":\\\"") property(name="fromhost-ip") constant(value="\\\",")
    constant(value="\\\"syslogtag\\\":\\\"") property(name="syslogtag") constant(value="\\\",")
    constant(value="\\\"pri\\\":\\\"") property(name="pri") constant(value="\\\",")
    constant(value="\\\"syslogfacility\\\":\\\"") property(name="syslogfacility") constant(value="\\\",")
    constant(value="\\\"syslogfacility-text\\\":\\\"") property(name="syslogfacility-text") constant(value="\\\",")
    constant(value="\\\"syslogseverity\\\":\\\"") property(name="syslogseverity") constant(value="\\\",")
    constant(value="\\\"syslogseverity-text\\\":\\\"") property(name="syslogseverity-text") constant(value="\\\",")
    constant(value="\\\"timereported\\\":\\\"") property(name="timereported" dateFormat="rfc3339") constant(value="\\\",")
    constant(value="\\\"timegenerated\\\":\\\"") property(name="timegenerated" dateFormat="rfc3339") constant(value="\\\",")
    constant(value="\\\"programname\\\":\\\"") property(name="programname") constant(value="\\\",")
    constant(value="\\\"protocol-version\\\":\\\"") property(name="protocol-version") constant(value="\\\",")
    constant(value="\\\"inputname\\\":\\\"") property(name="inputname")
    constant(value="}}" )
}}

*.* action(
    type="omrabbitmq"
    host="{args.host}"
    port="{args.port}"
    user="{args.username}"
    password="{args.password}"
    virtual_host="{args.virtual_host}"
    exchange="{args.exchange_name}"
    exchange_type="{args.exchange_type}"
    routing_key="{args.routing_key}"
    durable="{args.durable}"
    delivery_mode="{args.delivery_mode}"
    auto_delete="{args.auto_delete}"
    action.resumeRetryCount="-1"
    action.reportSuspension="on"
    action.reportSuspensionContinuation="on"
    action.execOnlyWhenPreviousIsSuspended="off"
    body_template="json"
)
'''

        with open(str(FILE), 'w') as f:
            f.write(CONFIG_STR)

if __name__ == '__main__':
    maker()
