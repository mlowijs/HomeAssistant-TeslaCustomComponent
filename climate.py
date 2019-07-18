"""
Support for Tesla HVAC system.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/climate.tesla/
"""
from datetime import timedelta
import logging

from custom_components.tesla_cc import (
    DATA_MANAGER, DOMAIN, PLATFORM_ID, TeslaDevice)
from homeassistant.components.climate import (ClimateDevice)
from homeassistant.components.climate.const import (SUPPORT_ON_OFF, SUPPORT_TARGET_TEMPERATURE)
from homeassistant.const import (ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [DOMAIN]

SUPPORT_FLAGS = SUPPORT_ON_OFF | SUPPORT_TARGET_TEMPERATURE

def setup_platform(hass, config, add_entities, discovery_info):
    """Set up the Tesla climate platform."""
    tesla_data = hass.data[DOMAIN]
    data_manager = tesla_data[DATA_MANAGER]

    climate_devices = [TeslaClimateDevice(hass, data_manager, vehicle)
                       for vehicle in data_manager.vehicles]

    add_entities(climate_devices, True)

def update_climate(func):
    def wrapper(self, **kwargs):
        from tesla_api import ApiError

        try:
            self._vehicle.wake_up()
            func(self, **kwargs)
            self._schedule_update(self._data_manager.update_climate)

            _LOGGER.debug('Turned climate on for {}.'.format(self._vehicle.vin))
        except ApiError:
            wrapper(self, **kwargs)

    return wrapper

class TeslaClimateDevice(TeslaDevice, ClimateDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle)

        _LOGGER.debug('Created climate device for {}.'.format(vehicle.vin))

    @update_climate
    def turn_on(self):
        self._vehicle.climate.start_climate()
        _LOGGER.debug('Turned climate on for {}.'.format(self._vehicle.vin))

    @update_climate
    def turn_off(self):
        self._vehicle.climate.stop_climate()
        _LOGGER.debug('Turned climate off for {}.'.format(self._vehicle.vin))

    @update_climate
    def set_temperature(self, **kwargs):
        if kwargs.get(ATTR_TEMPERATURE) is None:
            return

        temperature = kwargs.get(ATTR_TEMPERATURE)

        self._vehicle.climate.set_temperature(temperature)
        _LOGGER.debug('Set temperature for {}.'.format(self._vehicle.vin))

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return PLATFORM_ID.format(self._vehicle.vin)

    @property
    def supported_features(self):
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS if self._data['gui']['gui_temperature_units'] == 'C' else TEMP_FAHRENHEIT

    @property
    def is_on(self):
        return self._data['climate']['is_climate_on']

    @property
    def current_temperature(self):
        return self._data['climate']['inside_temp']

    @property
    def target_temperature(self):
        return self._data['climate']['driver_temp_setting']
