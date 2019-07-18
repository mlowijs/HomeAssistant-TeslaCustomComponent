"""
Support for various Tesla switches.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/climate.tesla/
"""
import logging

from custom_components.tesla_cc import (
    DATA_MANAGER, DOMAIN, PLATFORM_ID, TeslaDevice)
from homeassistant.const import (DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE, LENGTH_KILOMETERS, LENGTH_MILES, TEMP_CELSIUS,
    TEMP_FAHRENHEIT)
from homeassistant.components.switch import SwitchDevice

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [DOMAIN]
SWITCH_ID = PLATFORM_ID + '_{}'

def setup_platform(hass, config, add_entities, discovery_info):
    """Set up the Tesla sensor platform."""
    tesla_data = hass.data[DOMAIN]
    data_manager = tesla_data[DATA_MANAGER]

    all_switches = []

    all_switches.extend([TeslaChargingSwitch(hass, data_manager, vehicle)
                         for vehicle in data_manager.vehicles])

    all_switches.extend([TeslaSunroofSwitch(hass, data_manager, vehicle)
                         for vehicle in data_manager.vehicles])

    add_entities(all_switches, True)

def update_charge(func):
    def wrapper(self, **kwargs):
        from tesla_api import ApiError

        try:
            self._vehicle.wake_up()
            func(self, **kwargs)
            self._schedule_update(self._data_manager.update_charge)
        except ApiError:
            wrapper(self, **kwargs)
    
    return wrapper

def update_state(func):
    def wrapper(self):
        from tesla_api import ApiError

        try:
            self._vehicle.wake_up()
            func(self)
            self._schedule_update(self._data_manager.update_state)
        except ApiError:
            wrapper(self)
    
    return wrapper

NOT_CHARGING_STATES = ['Disconnected', 'Stopped']

class TeslaSunroofSwitch(TeslaDevice, SwitchDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle)

        _LOGGER.debug('Created sunroof switch device for {}.'.format(
            vehicle.vin))

    @update_state
    def turn_on(self):
        self._vehicle.controls.vent_sunroof()
        _LOGGER.debug('Vent sunroof for {}.'.format(self._vehicle.vin))

    @update_state
    def turn_off(self):
        self._vehicle.controls.close_sunroof()
        _LOGGER.debug('Closed sunroof for {}.'.format(self._vehicle.vin))

    @property
    def should_poll(self):
        return False

    @property
    def is_on(self):
        return self._data['state']['sun_roof_percent_open'] > 0

    @property
    def name(self):
        return SWITCH_ID.format(self._vehicle.vin, 'sunroof')

class TeslaChargingSwitch(TeslaDevice, SwitchDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle)

        _LOGGER.debug('Created charging switch device for {}.'.format(
            vehicle.vin))

    @update_charge
    def turn_on(self):
        self._vehicle.charge.start_charging()
        _LOGGER.debug('Started charging for {}.'.format(self._vehicle.vin))

    @update_charge
    def turn_off(self):
        self._vehicle.charge.stop_charging()
        _LOGGER.debug('Stopped charging for {}.'.format(self._vehicle.vin))

    @property
    def should_poll(self):
        return False

    @property
    def is_on(self):
        return self._data['charge']['charging_state'] not in NOT_CHARGING_STATES

    @property
    def name(self):
        return SWITCH_ID.format(self._vehicle.vin, 'charging')
