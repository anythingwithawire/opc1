import logging
import asyncio
import sys

sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://gsim.opc.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root

    myobj = await server.nodes.objects.add_object(idx, 'MyObject')
    #myvar = await myobj.add_variable(idx, 'MyVariable', 6.7)

    # Set MyVariable to be writable by clients
    #await myvar.set_writable()
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func,
                                          [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')

    async with server:
        while True:
            await asyncio.sleep(1)
            #new_val = await myvar.get_value() + 0.1
            #_logger.info('Set value of %s to %.1f', myvar, new_val)
            #await myvar.write_value(new_val)
            # await myvar2.write_value(789)
            f = open("/home/gareth/PycharmProjects/asim006_chuditch/data/CALCsmVar.txt", "r")
            if f:
                vars = f.readlines()
                for v in vars:
                    x = v.split(',')
                    if len(x) >= 2:
                        vName = x[0].strip()
                        vValue = x[1].strip()
                        vNameObj= vName+'Ob'
                        try:
                            await myWriteValue(locals()[vNameObj], idx, vName, vValue)
                        except:
                            locals()[vNameObj] = await myMakeObject(myobj, idx, vName, vValue)
                            #await mySetWriteable(locals()[vNameObj], idx, vName, vValue)
            f.close()


async def aaa(myobj, idx, vName, vValue):
    return await myobj.add_variable(idx, f'{vName}', vValue)


async def myMakeObject(myobj, idx, vName, vValue):
    return await aaa(myobj, idx, vName, vValue)


async def bbb(myobj, idx, vName, vValue):
    return await myobj.write_value(vValue)


async def myWriteValue(myobj, idx, vName, vValue):
    await bbb(myobj, idx, vName, vValue)


async def ccc(myobj, idx, vName, vValue):
    return await myobj.set_writeable()


async def mySetWriteable(myobj, idx, vName, vValue):
    await ccc(myobj, idx, vName, vValue)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
