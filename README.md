# HomeAssistant-TeslaCustomComponent
Custom Tesla component written in Python3 for Home Assistant. Controls and reads status of your Tesla.
The original Tesla component has issues with the wakeup feature. This component fixes that issue.
NOTE: The climate works only for Home Assistant 0.96 and later due to the climate platform redo the core developers did.

Tested on:
* Tesla Model S late 2018
* Home-Assistant 
    - 0.96.x

 **If you are experiencing issues please be sure to provide details about your device, Home Assistant version and what exactly went wrong.**

**Sources used:**
 - https://www.teslaapi.io/
 - https://tesla-api.timdorr.com
 
## HACS
This component will be submitted to HACS in the near future.

## Custom Component Installation
!!! PLEASE NOTE !!!: Don't use this method if you are using HACS.
1. Copy the custom_components folder to your own hassio /config folder.

2. In the root of your /config folder, create a file called tesla.yaml

   ```yaml
   username: <TeslaAccountEmailAdress>
   password: <TeslaAccountPassword>
   ```

3. In your configuration.yaml add the following:
  
   ```yaml
   tesla_cc: !include tesla.yaml
   ```
