# Hanmatek Power Supplies



## HM310T

![HM310T](hm310t_image.jpg)

**WARNING! /dev/ttyUSB0 not present in Ubuntu 22.04**

On Ubuntu 22, there is an USB conflict.

```bash
# EDIT >>> 
/usr/lib/udev/rules.d/85-brltty.rules

# Search for this line and comment it out:
ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"

# reboot
```

**Panduza interface minimal template**

```json
{
    "name": "My Power Supply",
    "driver": "hm310t"
}
```

**Modbus Registers**

DeviceAddr default = 1 MODBUS slave ID address

| Name           | Address     | Mode | Description                                                                    |
| -------------- | ----------- | ---- | ------------------------------------------------------------------------------ |
| PS_PowerSwitch | 0x01        | R/W  | 0/1  Power output/stop setting                                                 |
| PS_ProtectStat | 0x02        | R    | Bit mask  SCP:OTP:OPP:OCP:OVP                                                  |
| PS_Model       | 0x03        | R    | 3010 (HM310P)                                                                  |
| PS_ClassDetial | 0x04        | R    | value 0x4b58 (19280)                                                           |
| PS_Voltage     | 0x0010 (16) | R    | 2Decimal Voltage display value                                                 |
| PS_Current     | 0x0011      | R    | 3Decimal Current display value                                                 |
| PS_PowerH      | 0x0012      | R    | 3Decimal Power display value 0012H(high 16 bit)/ 0013H( low 16 bit )           |
| PS_PowerL      | 0x0013      | R    | 3Decimal Power display value 0012H(high 16 bit)/ 0013H( low 16 bit )           |
| PS_PowerCal    | 0x0014      | ?    |                                                                                |
| PS_ProtectVol  | 0x0020      | RW   | 2Decimal OVP Set over volate protect value                                     |
| PS_ProtectCur  | 0x0021      | RW   | 2Decimal OCP Set over current protect value                                    |
| PS_ProtectPow  | 0x0022      | RW   | 2Decimal OPP Set over power protect value 0022H(high 16 bit)，023H(low 16 bit) |
| PS_SetVoltage  | 0x0030 (48) | RW   | 2Dec Set voltage                                                               |
| PS_SetCurrent  | 0x0031      | RW   | 3Dec Set current                                                               |
| PS_SetTimeSpan | 0x0032      | RW   | ????                                                                           |

<!-- 
  - Bit mask (OCP 0x02/OVP 0x01) Ptotect status<p>SCP:OTP:OPP:OCP:OVP<p>OVP：Over voltage protection<p>OCP：Over current protection<p>OPP：Over power protection<p>OTP：Over tempreture protection<p>SCP：short-circuit protection                          -->

<!-- 
PS_Decimals   | 0x0005      | R | Value 0x233 <p>Note 2: Decimal point digit capacity information as follow:<p>  voltage current power decimal point digit capacity <p>Dat=ShowPN /((2<<8)/(3<<4)/(3<<0)) =>0.00V 0.000A 0.000W <p> For example when read:0x0233 (563) <p>mean that voltage 2 decimal,current 3 decimal,power 3 decimal.<p>
PS_PowerStat | 0x8801 | ? |
PS_defaultShow | 0x8802 |? |
PS_SCP | 0x8803  |? |
PS_Buzzer | 0x8804  |RW | Buzzer enablement 
PS_Device | 0x9999        | R/W | Set communication address - SlaveID : 1 default  |
PS_SDTime | 0xCCCC |? |
PS_UL | 0xC110        |?     | 11d / xC111 = 1 |
PS_UH | 0xC11E        | ?    | 3200d / xC11F = 1 |
PS_IL | 0xC120          |?   | 21 / xC121=1  |
PS_IH | 0xC12E           |?  | 10100/ xC12F=1 |
PSM_Voltage | 0x1000 |RW
PSM_Current | 0x1001  |RW
PSM_TimeSpan | 0x1002 |R?
PSM_Enable | 0x1003 | ?
PSM_NextOffset | 0x10 |?-->

**Sources**

- https://github.com/notkevinjohn/HM310P
- https://github.com/hobbyquaker/hanmatek-hm310p
- https://github.com/mckenm/HanmaTekPSUCmd/wiki/Registers (to get the modbus registers full list)

