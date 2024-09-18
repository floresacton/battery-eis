import struct
import time

import usbtmc


def parse_header(data):
    header_len = data[1]-46
    data_len = int(data[2:header_len])
    return data_len, data[header_len:data_len+header_len]

def parse_format(data, format):
    values = struct.unpack(format, data)
    fdata = []
    for i in range(len(values)):
        if isinstance(values[i], bytes):
            fdata.append(values[i].decode("utf-8").rstrip('\x00'))
        else:
            fdata.append(values[i])
    return fdata


class Scope:
    def __init__(self, addr):
        self.scope = usbtmc.Instrument(addr)
        self.hgrids = 10
        self.timebases = [
            200e-12,
            500e-12,
            1e-9,
            2e-9,
            5e-9,
            10e-9,
            20e-9,
            50e-9,
            100e-9,
            200e-9,
            500e-9,
            1e-6,
            2e-6,
            5e-6,
            10e-6,
            20e-6,
            50e-6,
            100e-6,
            200e-6,
            500e-6,
            1e-3,
            2e-3,
            5e-3,
            10e-3,
            20e-3,
            50e-3,
            100e-3,
            200e-3,
            500e-3,
            1,
            2,
            5,
            10,
            20,
            50,
            100,
            200,
            500,
            1000,
        ]

    def block_complete(self):
        response = self.scope.ask("*OPC?")
        if response == "1":
            return

        time.sleep(0.1)

    def reset(self):
        self.scope.write(f"*RST")
        self.block_complete()
        time.sleep(5)

    def get(self, group, cmd):
        return self.scope.ask(f":{group}:{cmd}?")

    def get_raw(self, group, cmd):
        return self.scope.ask(f":{group}:{cmd}?")

    def set(self, group, cmd, val):
        self.scope.write(f":{group}:{cmd} {val}")
        self.block_complete()

    #############

    def aquire_set(self, cmd, val):
        self.set("ACQ", cmd, val)

    def aquire_get(self, cmd):
        return self.get("ACQ", cmd)

    def waveform_set(self, cmd, val):
        self.set("WAV", cmd, val)

    def waveform_get(self, cmd):
        return self.get("WAV", cmd)

    def channel_set(self, num, cmd, val):
        self.set(f"CHAN{num}", cmd, val)
    
    def trigger_run(self):
        self.scope.write(f":TRIG:RUN")
        self.block_complete()
    
    def trigger_stop(self):
        self.scope.write(f":TRIG:STOP")
        self.block_complete()

    #############

    def waveform_preamble(self):
        self.scope.write(":WAV:PRE?")
        _, data = parse_header(self.scope.read_raw())
        return parse_format(
            data,
            "=16s16shhi20xi12x16s24xi12xii4xii4xfff4xhhfd136xhhfhh8xh"
        )

    def waveform_data(self, header):
        self.scope.write(":WAV:DATA?")
        length, data = parse_header(self.scope.read_raw())

        format = "=" + (("h" * (length // 2)) if header[2] else ("b" * length))
        values = parse_format(data, format)

        points = []
        for i in range(len(values)):
            voltage = (values[i]*(header[12]/header[14])-header[13])*header[21]
            timestamp = header[18] - (self.timebases[header[19]] * self.hgrids/2) + i*header[17]

            points.append((timestamp, voltage))

        return points
