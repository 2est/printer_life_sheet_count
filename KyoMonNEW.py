# import selection
from pysnmp.hlapi import *
import time
import win32ui
import configparser

# var section
oid = '1.3.6.1.2.1.43.10.2.1.4.1.1'
log = open('life_count.txt', 'a')
config = configparser.ConfigParser()


# definition section
def get(ip, oids, credential, port=161, engine=SnmpEngine(), contexts=ContextData()):
    try:
        handler = getCmd(
            engine,
            credential,
            UdpTransportTarget((ip, port)),
            contexts,
            ObjectType(ObjectIdentity(oids))
        )
        return fetch(handler, 1)[0]
    except Exception as error:
        win32ui.MessageBox('Ошибочка - %s' % str(error))



def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items = var_bind[1]
                result.append(items)
            else:
                error = 'Got SNMP error: {0}'.format(error_indication)
                result.append(error)
        except StopIteration:
            break
    return result


# executable section
try:
    with open('KyoMon.ini') as configfile:
        log.write('\n' + time.ctime() + '\n')
        config.read('KyoMon.ini')
        community = config['Recepient_Settings']['Community']
        targets_ip = config['Targets']['Ip_list']
        oid_list = config['OIDs']['oids']
        for target_ip in targets_ip.splitlines():
            for oid in oid_list.splitlines():
                response = get(target_ip, oid, CommunityData(community, mpModel=0))
                log.write(str(target_ip) + ' - ' + str(response) + '\n')
except KeyError as error:
    win32ui.MessageBox('Ошибка в - "%s", смотри KeyMon.ini!!!' % str(error))
except IOError:
    win32ui.MessageBox('Файл "KyoMon.ini" не найден')
finally:
    log.close()
