from avatar2.targets import Target
from avatar2.protocols.gdb import GDBProtocol
from avatar2.protocols.simavr import SimAvrProtocol


class SimAvrTarget(Target):

    def __init__(self,
                 avatar,
                 simavr_executable=None,
                 firmware=None,
                 flash=None,
                 eeprom=None,
                 verbose_level=0,
                 serial_terminator=b'\r\n',
                 pty_number=0,
                 serial_baud_rate=115200,
                 core='atmega328p',
                 core_frequency=16000000,
                 additional_args=None,
                 gdb_executable=None,
                 gdb_additional_args=None,
                 **kwargs):
        super(SimAvrTarget, self).__init__(avatar, **kwargs)

        self.serial_baud_rate = serial_baud_rate
        self.pty_number = pty_number
        self.serial_terminator = serial_terminator

        self.firmware = firmware
        self.flash = flash
        self.eeprom = eeprom

        if simavr_executable is not None:
            self.simavr_executable = simavr_executable
        else:
            self.simavr_executable = self._arch.get_simavr_executable()

        self.additional_args = additional_args if additional_args else []
        self.verbose_level = verbose_level

        self.gdb_executable = (gdb_executable if gdb_executable is not None
                               else self._arch.get_gdb_executable())
        if gdb_additional_args:
            self.gdb_additional_args = gdb_additional_args
        else:
            self.gdb_additional_args = []

        self.gdb_port = 1234

        self.core = core
        self.core_frequency = core_frequency

    def init(self):
        gdb = GDBProtocol(gdb_executable=self.gdb_executable,
                          arch=self._arch,
                          additional_args=self.gdb_additional_args,
                          avatar=self.avatar, origin=self)

        simavr = SimAvrProtocol(self.firmware,
                                simavr_executable=self.simavr_executable,
                                flash=self.flash, eeprom=self.eeprom,
                                additional_args=self.additional_args,
                                verbose_level=self.verbose_level,
                                serial_terminator=self.serial_terminator,
                                pty_number=self.pty_number,
                                serial_baud_rate=self.serial_baud_rate,
                                core_frequency=self.core_frequency,
                                core=self.core,
                                origin=self,
                                output_dir=self.avatar.output_directory)

        if simavr.is_running() and gdb.remote_connect(port=self.gdb_port):
            self.log.info("Connected to target")
        else:
            self.log.warning("Connection failed")

        self.protocols.set_all(gdb)
        self.protocols.monitor = simavr

        self.wait()

    def __str__(self):
        return str(vars(self))
