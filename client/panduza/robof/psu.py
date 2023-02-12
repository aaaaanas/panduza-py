from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of

class KeywordsPsu(object):

    @keyword
    def set_power_supply_voltage(self, name, voltage):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[name].volts.value.set(float(voltage))

    @keyword
    def power_supply_should_be(self, name, state):
        """Check power supply state
        """
        assert_that(state, any_of(equal_to("on"), equal_to("off")))
        pza = BuiltIn().get_variable_value("${__pza__}")
        read_state = pza[name].state.value.get()
        assert_that(read_state, equal_to(state))

    @keyword
    def turn_power_supply(self, name, state):
        """Turn on the psu
        """
        assert_that(state, any_of(equal_to("on"), equal_to("off")))
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[name].state.value.set(state)

    @keyword
    def turn_on_power_supply(self, name, ensure=False):
        """Turn on the psu
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[name].state.value.set("on", ensure)

    @keyword
    def turn_off_power_supply(self, name, ensure=False, teardown=False):
        """Turn on the psu
        """
        pza = BuiltIn().get_variable_value("${__pza__}")

        if pza == None:
            # It is ok if panduza is not initialized, only if in the teardown process
            assert not teardown
        else:
            pza[name].state.value.set("off", ensure)


