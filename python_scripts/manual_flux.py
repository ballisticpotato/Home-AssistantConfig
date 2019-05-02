LIGHTS = [
        "light.jerry_s_floor_lamp",
        "light.jerry_s_bathroom_lights",
        "light.jerry_bedside"]

WARM_GLOW_EVENING = datetime.time(22,00,00)
WARM_GLOW_MORNING = datetime.time(5,00,00)

now = datetime.datetime.now().time()

sun_state = hass.states.get("sun.sun").state

if (sun_state == 'above_horizon'):
    temp = 4000
elif(now < WARM_GLOW_MORNING or now > WARM_GLOW_EVENING):
    temp = 2200
else:
    temp = 2700

for light in LIGHTS:
    if (hass.states.is_state(light, "on")):
        service_data = {
                "entity_id": light,
                "kelvin": temp
                }
        hass.services.call("light", "turn_on", service_data, False)

