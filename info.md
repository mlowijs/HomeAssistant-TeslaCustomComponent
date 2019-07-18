# Custom Tesla component. Controls and reads status of your Tesla.
The original Tesla component has issues with the wakeup feature. This component fixes that issue.

## Component configuration

To configure this component, follow these instructions (replacing the placeholders).

1. In the root of your /config folder, create a file called tesla.yaml

   ```
   username: <TeslaAccountEmailAdress>
   password: <TeslaAccountPassword>
   ```

2. In your configuration.yaml add the following:
  
   ```
   tesla_cc: !include tesla.yaml
   ```
3. Done