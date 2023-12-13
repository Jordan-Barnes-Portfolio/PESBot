import ctypes

# Replace this with the actual address you want to read from
address = 0x71A7FD590

try:
    print("Reading float value...")
    # Define the structure that matches the data layout at the specified address
    class FloatStruct(ctypes.Structure):
        _fields_ = [("value", ctypes.c_float)]

    # Create an instance of the structure at the given address
    float_at_address = FloatStruct.from_address(address)

    # Access the float value
    float_value = float_at_address.value
    print("Done.")
    print(f"Float value at address {hex(address)}: {float_value}")

except Exception as e:
    print(f"Error: {e}")