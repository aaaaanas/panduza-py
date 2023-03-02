*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config

*** Test Cases ***

Basic tests
    Turn on power supply       psu_1
    Power Supply Should Be    psu_1    on
    Turn off power supply       psu_1
    Power Supply Should Be    psu_1    off
    Turn Power Supply    psu_1    on
    Power Supply Should Be    psu_1    on
    Turn Power Supply    psu_1    off
    Power Supply Should Be    psu_1    off
    Set Power Supply Voltage Goal    psu_1    3.3
    Set Power Supply Voltage Goal    psu_1    10
    Set Power Supply Current Goal    psu_1    2

Test polling cycles
    Set Power Supply Voltage Polling Cycle    psu_1    2

Test polling cycles max
    Set Power Supply Voltage Polling Cycle    psu_1    0

Test polling cycles disbale
    Set Power Supply Voltage Polling Cycle    psu_1    -1

Enable settings
    Turn Power Supply Ovp Setting    psu_1    True
    Turn Power Supply Ocp Setting    psu_1    True
    
    