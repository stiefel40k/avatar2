from nose.tools import assert_equal

from avatar2 import *


avatar = Avatar(arch=archs.AVR_ATMEGA328P, console_log=True, output_directory="/tmp/avatar_out")

target = avatar.add_target(SimAvrTarget,
                           simavr_executable="/home/gabor/repos/simavr-with-uart/simavr/run_avr",
                           firmware="/tmp/gabor_challenge/challenge.ino.hex",
                           verbose_level=5,
                           gdb_executable="avr-gdb")

target.init()

ret = target.set_breakpoint_with_console_interpreter("*(void (*)())0x7aa")
assert_equal(ret, 1)
brkpnt = target.get_breakpoint_info(1)
assert_equal(isinstance(brkpnt, dict), True)
#print(hex(target.read_memory(0x7aa, 2)))
target.cont()
target.wait()
print(hex(target.read_register('pc')*2))
time.sleep(1)
ret = target.set_breakpoint_with_console_interpreter("*(void (*)())0x2e2")
#target.wait()
avatar.shutdown()
