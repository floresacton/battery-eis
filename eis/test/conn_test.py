import usbtmc

addrs = usbtmc.list_resources()

for addr in addrs:
    dev = usbtmc.Instrument(addr)
    print(addr)
    print(dev)
    print(dev.ask("*IDN?"))
    print()


#dev.write("C1:OUTP ON")
