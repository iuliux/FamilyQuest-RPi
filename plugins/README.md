Add a new plugin
----------------

1. Create a new file `<actuator>.py` (where `<actuator>` is the name of the new
actuator
2. Implement a class that defines the following methods:
	- `start()` - RaspberryPi gives a start signal to the actuator
	- `stop()` - RaspberryPi gives a stop signal to the actuator
3. Open `__init__.py` and add two lines:
	- An import line like:

		import <actuator>

	- A new entry in the `plugins` list, like

		```
		plugins = [
		    tv.TvActuator,
		    game_console.GameConsoleActuator,
			<actuator>.<Actuator>Actuator,  # This line was added
		]
		```

		Remember to place the new actuator at the index of it's corresponding
		reward type
