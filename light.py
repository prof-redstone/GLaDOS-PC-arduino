import threading
#USER NAME ET PASSWORD c'est celui de Smart life, le reste c'est sur Tuya api developer


def light_bureau(state):
    def send(stateT):
        try:
            from Tuya import Key
            from tuya_iot import TuyaOpenAPI, TUYA_LOGGER
            import logging
            TUYA_LOGGER.setLevel(logging.DEBUG)
            openapi = TuyaOpenAPI(Key.ENDPOINT, Key.ACCESS_ID, Key.ACCESS_KEY)
            openapi.connect(Key.USERNAME, Key.PASSWORD, "33", 'smartlife')
            commands = {'commands': [{'code': 'switch_led', 'value': stateT}]}
            openapi.post('/v1.0/devices/{}/commands'.format(Key.DEVICE_ID_BUREAU), commands)
        except:
            pass

    thread = threading.Thread(target=send, args=(state,))
    thread.start()


def light_plafond(state):
    def send(stateT):
        try:
            from Tuya import Key
            from tuya_iot import TuyaOpenAPI, TUYA_LOGGER
            import logging
            TUYA_LOGGER.setLevel(logging.DEBUG)
            openapi = TuyaOpenAPI(Key.ENDPOINT, Key.ACCESS_ID, Key.ACCESS_KEY)
            openapi.connect(Key.USERNAME, Key.PASSWORD, "33", 'smartlife')
            commands = {'commands': [{'code': 'switch_led', 'value': stateT}]}
            openapi.post('/v1.0/devices/{}/commands'.format(Key.DEVICE_ID_PLAFOND), commands)
        except:
            pass

    thread = threading.Thread(target=send, args=(state,))
    thread.start()


if __name__ == "__main__":
    try:
        light_bureau(True)
        light_plafond(True)
    except KeyboardInterrupt:
        pass