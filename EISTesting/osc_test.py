import usbtmc

addrs = usbtmc.list_resources()

assert "USB::1689::932::C030786::INSTR" in addrs, "no scope"


#dev.write("C1:OUTP ON")
