from capstone import *
from keystone import *
from .architecture import Architecture
import avatar2

from avatar2.installer.config import QEMU, PANDA, OPENOCD, GDB_AVR, SIMAVR


class AVR(Architecture):
    get_qemu_executable = Architecture.resolve(QEMU)
    get_panda_executable = Architecture.resolve(PANDA)
    get_gdb_executable = Architecture.resolve(GDB_AVR)
    get_oocd_executable = Architecture.resolve(OPENOCD)
    get_simavr_executable = Architecture.resolve(SIMAVR)

    registers = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4, 'r5': 5, 'r6': 6,
                 'r7': 7, 'r8': 8, 'r9': 9, 'r10': 10, 'r11': 11, 'r12': 12,
                 'r13': 13, 'r14': 14, 'r15': 15, 'r16': 16, 'r17': 17,
                 'r18': 18, 'r19': 19, 'r20': 20, 'r21': 21, 'r22': 22,
                 'r23': 23, 'r24': 24, 'r25': 25, 'r26': 26, 'r27': 27,
                 'r28': 28, 'r29': 29, 'r30': 30, 'r31': 31, 'sreg': 32,
                 'sp': 33, 'pc': 34}
    # header files for avr sp=61 sreg=63 pc=?
    # simavr: https://github.com/buserror/simavr/blob/4c9efe1fc44b427a4ce1ca8e56e0843c39d0014d/simavr/sim/sim_gdb.c#L255
    sr_name = 'sreg'

    gdb_name = "avr"


AVR_ATMEGA328P = AVR
