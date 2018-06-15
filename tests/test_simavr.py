from nose.tools import assert_equal

from avatar2 import *


avatar = Avatar(arch=archs.AVR_ATMEGA328P, console_log=True, output_directory="/tmp/avatar_out")
#avatar = Avatar(arch=archs.AVR_ATMEGA328P, output_directory="/tmp/avatar_out")

target = avatar.add_target(SimAvrTarget,
                           simavr_executable="/home/gabor/repos/simavr-with-uart/simavr/run_avr",
                           firmware="/tmp/gabor_challenge/challenge.ino.hex",
                           verbose_level=5,
                           gdb_executable="avr-gdb")

target.init()

ret = target.set_breakpoint(0x7aa, relative_to_pc=True)
assert_equal(ret, 1)
brkpnt = target.get_breakpoint_info(1)
assert_equal(isinstance(brkpnt, dict), True)
assert_equal({'number': '1', 'type': 'breakpoint', 'disp': 'keep', 'enabled': 'y', 'addr': '0x000007aa', 'thread-groups': ['i1'], 'times': '0', 'original-location': '*($pc-(-0x7aa))'}, brkpnt)
print(hex(target.read_memory(0x7aa, 2, relative_to_pc=True)))
target.cont()
target.wait()
assert_equal(target.read_register('pc')*2, 0x7aa)
assert_equal(target.read_register('PC2'), 0x7aa)
avatar.shutdown()
