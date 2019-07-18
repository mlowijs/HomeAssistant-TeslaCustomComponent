"""
Support for Tesla location tracking.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/climate.tesla/
"""
import logging

from custom_components.tesla_cc import (
    DATA_MANAGER, DOMAIN, PLATFORM_ID, TeslaDevice, VEHICLE_UPDATED)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [DOMAIN]

def setup_scanner(hass, config, see, discovery_info=None):
    tesla_data = hass.data[DOMAIN]
    data_manager = tesla_data[DATA_MANAGER]

    def update(vin):
        name = PLATFORM_ID.format(vin)
        vehicle = data_manager.data[vin]

        see(
            dev_id=name,
            gps=(vehicle['drive']['latitude'], vehicle['drive']['longitude'])
        )

    def vehicle_updated(event):
        update(event.data.get('vin'))

    hass.bus.listen(VEHICLE_UPDATED, vehicle_updated)

    for vehicle in data_manager.vehicles:
        update(vehicle.vin)
    
    return True
