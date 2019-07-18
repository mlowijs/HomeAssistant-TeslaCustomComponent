"""
Support for various Tesla sensors.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/climate.tesla/
"""
import logging

from custom_components.tesla_cc import (
    DATA_MANAGER, DOMAIN, PLATFORM_ID, TeslaDevice)
from homeassistant.const import (
    DEVICE_CLASS_BATTERY, DEVICE_CLASS_TEMPERATURE, LENGTH_KILOMETERS,
    LENGTH_MILES, TEMP_CELSIUS, TEMP_FAHRENHEIT)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [DOMAIN]
SENSOR_ID = PLATFORM_ID + '_{}'

def setup_platform(hass, config, add_entities, discovery_info):
    """Set up the Tesla sensor platform."""
    tesla_data = hass.data[DOMAIN]
    data_manager = tesla_data[DATA_MANAGER]

    all_sensors = []

    all_sensors.extend([TeslaBatterySensorDevice(hass, data_manager, vehicle)
                        for vehicle in data_manager.vehicles])

    all_sensors.extend([TeslaRangeSensorDevice(hass, data_manager, vehicle)
                        for vehicle in data_manager.vehicles])

    all_sensors.extend([TeslaOutsideTemperatureSensorDevice(hass, data_manager,
                                                            vehicle)
                        for vehicle in data_manager.vehicles])

    add_entities(all_sensors, True)

class TeslaSensorDevice(TeslaDevice, Entity):
    def __init__(self, hass, data_manager, vehicle, measured_value):
        super().__init__(hass, data_manager, vehicle)

        self._measured_value = measured_value

        _LOGGER.debug('Created ''{}'' sensor device for {}.'.format(
            measured_value, vehicle.vin))

    @property
    def name(self):
        return SENSOR_ID.format(self._vehicle.vin, self._measured_value)

class TeslaOutsideTemperatureSensorDevice(TeslaSensorDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle, 'outside_temp')

    @property
    def state(self):
        return self._data['climate']['outside_temp']

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS if self._data['gui']['gui_temperature_units'] == 'C' else TEMP_FAHRENHEIT

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE

class TeslaBatterySensorDevice(TeslaSensorDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle, 'soc')

    @property
    def state(self):
        return self._data['charge']['battery_level']

    @property
    def unit_of_measurement(self):
        return '%'

    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY

class TeslaRangeSensorDevice(TeslaSensorDevice):
    def __init__(self, hass, data_manager, vehicle):
        super().__init__(hass, data_manager, vehicle, 'range')

    @property
    def state(self):
        return round(self._data['charge']['battery_range'])

    @property
    def unit_of_measurement(self):
        return LENGTH_KILOMETERS if self._data['gui']['gui_distance_units'] == 'km/hr' else LENGTH_MILES
