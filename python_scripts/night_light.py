## Constants
ON_LIGHT = "light.bedroom_2"
OFF_LIGHTS = [
    "light.bedroom_1"
]

# Turn off the manual_flux automation first
hass.services.call("automation", "turn_off", {"entity_id": "automation.manual_flux"}, True)

# If we're already in light night mode, then turn off the lights
if (hass.states.is_state(ON_LIGHT, "on") and hass.states.is_state(OFF_LIGHTS[0], "off")):
    hass.services.call("light", "turn_off", {"entity_id": "light.bedroom_lamp"}, False)
else:
    hass.services.call("light", "turn_off", {"entity_id": OFF_LIGHTS}, False)
    time.sleep(1)
    service_data = {
        "entity_id": ON_LIGHT,
        "kelvin": 2200,
        "brightness_pct": 5
    }
    hass.services.call("light", "turn_on", service_data, False)

# Turn back on the manual_flux automation after a second
time.sleep(1)
hass.services.call("automation", "turn_on", {"entity_id": "automation.manual_flux"}, False)
