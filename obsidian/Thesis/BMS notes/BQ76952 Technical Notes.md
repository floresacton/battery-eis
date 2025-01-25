https://www.ti.com/lit/ug/sluuby2b/sluuby2b.pdf?ts=1726594300232
### Startup Behavior
On startup, or exiting from SHUTDOWN, all registers and data memory reads from OTP xor memory.  This means that without flashing, the IC will not power the REG1 line with 5V necessary to power the STM, and the BMS will remain disabled until manually waking the BMS and programming REG1 with 5V.

### Command Structure
The device I2C bus supports direct commands and subcommands.  The default write address is 0x10 and the default read address is 0x11

###### Direct Commands
Direct commands use the 7-bit command address and can either trigger an action, provide data to be written, or instruct the device to report back data.  Direct commands are defined as single byte commands.  Longer commands or commands that read or write large blocks of data are considered subcommands.  

The list of direct commands is listed in table 12.1.  Each entry also lists how many bytes is associated with that command and how the data is encoded in those bytes.  Direct commands are limited to 2 bytes of read or write max.

###### Subcommands
Subcommands are additional commands that are accessed indirectly using the 7-bit command address space and provide the capability for block data transfers.  Subcommands are selected using a 16-bit command address.  To initiate a subcommand, you must write the upper and lower half of the address to the 7-bit addresses 0x3E (lower) and 0x3F(upper) as if you were writing data using direct commands.

Upon writing the subcommand address, the device will assume a read operation is taking place even though it is not yet known whether the operation will be a read or write.  It will populate addresses 7-bit addresses 0x40 - 0x5F with 32 bytes of data according to the address specified by the subcommand.  

If attempting to read from a subcommand, continuously read 0x3E and 0x3F after writing to them to see if 0xFF is returned.  If so, the device is not done getting the data.  Once the values return to their original value can we proceed.  The device can now read from the data buffer in the case of a read operation.  The checksum for this data will be stored in 0x60.  The length of the data in bytes is stored in 0x61.  The length returned is the sum of the buffer length plus four (0x3E 0x3F 0x60 0x61 included).

If the checksum (0x60) and length (0x61) are read together, this can trigger an auto increment in some cases, in which case the buffer will be populated with another block's data.  Read 0x61 before reading the data buffer to avoid this.

 It also writes a checksum for the data in 0x60.  This is calculated as follows:
 1) Get the 8-bit sum of 0x3E and 0x3F.
 2) Add the length of the data in the buffer in bytes plus four.
 3) Finally bitwise invert the result.

If a write operation is desired, the host will overwrite the 32 bytes of data to be the data written.  The host will write the corresponding checksum into 0x60, then the length of the byte array into 0x61.  After writing to 0x61, the device will check the checksum to be correct, and if so it will write the buffer into memory.  The checksum and data length must be written sequentially as a word in order for this process to occur.


## Alarm Raw Status vs Alarm Status vs Alarm Enable

Alarm raw status is whether or not the event or condition is currently being met.  The event will show in the raw status no matter the configuration of the BMS.  Alarm enable is the mask the user sets to configure which of the alarm conditions will cause the system to have an alarm.  Bitwise anding the raw status and the enable gives the alarm status.  The Alarm status is latched, meaning the raw status and the enable bitfields for an event only need to be active at the same time for an instant for the alarm status to be latched high until manually reset by the user.  This is done by using the direct command to read the alarm status followed by a bitmask which resets all the bits irrespective if the condition to cause the alarm to status to latch is currently being met, since the alarm status will only latch on the transition.  Thus you should make sure that the alarm status bit you are clearing is also not simultaneously in the raw status and the enable.

## Safety Alert vs Safety Alert Mask vs Safety Status
Safety Alert

### Random
Command or subcommand bits denoted RSVD_0 should only be written as a "0", while bits denoted RSVD_1
should only be written as a "1"


using CRC8 polynomial x^8 + x^2 + x + 1 (0b100000111) with initial value 0.  The checksum is calculated over 0x3E, 0x3F, and the buffer data.  This does not include the checksum or length.