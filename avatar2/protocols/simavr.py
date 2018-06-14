import logging
import subprocess
import distutils.spawn

import serial


class SimAvrProtocol(object):

    def __init__(self, firmware, simavr_executable="simavr",
                 flash=None,
                 eeprom=None,
                 additional_args=None,
                 verbose_level=0,
                 serial_terminator=b'\r\n',
                 pty_number=0,
                 serial_baud_rate=115200,
                 core_frequency=16000000,
                 core="atmega328p",
                 output_dir="/tmp",
                 origin=None):

        self._firmware = firmware
        self._flash = flash
        self._eeprom = eeprom

        self._simavr_executable = distutils.spawn.find_executable(
            simavr_executable)
        self._additional_args = (additional_args if additional_args is not None
                                 else [])

        for vlevel in range(0, verbose_level):
            self._additional_args.append("-v")

        self._additional_args.append(firmware)
        self._serial_terminator = serial_terminator
        self._serial_path = '/tmp/simavr-uart' + str(pty_number)
        self._serial_baud_rate = serial_baud_rate
        self._serial_conn = None

        self._core = core
        self._core_frequency = core_frequency

        env_var = {"SIMAVR_UART_XTERM": "uart{}".format(pty_number)}

        self._cmd_line = [simavr_executable]
        if self._flash is not None:
            self._cmd_line.append("--ff")
            self._cmd_line.append(flash)

        if eeprom is not None:
            self._cmd_line.append("--ee")
            self._cmd_line.append(eeprom)

        self._cmd_line.append("-pty{}".format(pty_number))
        self._cmd_line.append("-m")
        self._cmd_line.append(core)
        self._cmd_line.append("-f")
        self._cmd_line.append(str(core_frequency))
        self._cmd_line.append("-g")

        self._cmd_line += self._additional_args

        if origin:
            self._log = logging.getLogger('%s.%s' % (origin.log.name,
                                                     self.__class__.__name__))
        else:
            self._log = logging.getLogger(self.__class__.__name__)

        self._log.debug(" ".join(self._cmd_line))
        with open("%s/simavr_out.txt" % output_dir, "wb") as out, \
                open("%s/simavr_err.txt" % output_dir, "wb") as err:
            self._simavr = subprocess.Popen(self._cmd_line, stdout=out,
                                            stderr=err, env=env_var)

    def serial_connect(self, read_timeout=1, write_timeout=1):
        self._serial_conn = serial.Serial(self._serial_path,
                                          baudrate=self._serial_baud_rate,
                                          timeout=read_timeout,
                                          write_timeout=write_timeout)
        self._serial_conn.open()
        return self._serial_conn.is_open

    def serial_send_message(self, message):
        if self._serial_conn is not None and self._serial_conn.is_open:
            byte_message = bytearray()
            byte_message.extend(map(ord, message))
            byte_message.extend(self._serial_terminator)
            try:
                written = self._serial_conn.write(byte_message) - \
                          len(self._serial_terminator)
            except serial.SerialTimeoutException:
                self._log.error('Timeout sending message "{}"'.format(message))
                written = -1
            return written

        else:
            raise ConnectionError("Serial connection is not initialized.")

    def serial_receive_message(self):
        recv = "".join(map(chr, self._serial_conn.read()))
        str_terminator = "".join(map(chr, self._serial_terminator))
        if str_terminator not in recv:
            raise serial.SerialTimeoutException("Timeout exceeded for read.")
        return recv.replace(str_terminator, "")

    def is_running(self):
        if self._simavr.poll() is None:
            return True
        else:
            self._log.error("Failed to start simavr")
            return False

    def shutdown(self):
        """
        Shuts down SimAvr
        returns: True on success, else False
        """
        if self._serial_conn is not None and self._serial_conn.is_open:
            self._serial_conn.close()
        if self._simavr is not None:
            self._simavr.terminate()
            self._simavr = None
