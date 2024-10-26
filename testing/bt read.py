import bleak

# Initialize the BLE device
device = bleak.BLEDevice('your_esp32_board')

# Set up the BLE service and characteristic
service = device.service('your_service_uuid')
characteristic = service.characteristic('your_characteristic_uuid')

# Read data from the characteristic
data = characteristic.read()

print(data)