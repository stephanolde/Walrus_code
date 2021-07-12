# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started.

import octoprint.plugin
import serial
from octoprint.util import RepeatedTimer


BAUD		= 9600 # change if different baud-rate
PORT		=  "/dev/ttyS0"

UPDATE_INTERVAL = 1000

class SkeletonPlugin(octoprint.plugin.StartupPlugin,
					 octoprint.plugin.TemplatePlugin,
					 octoprint.plugin.AssetPlugin,
					 octoprint.plugin.SettingsPlugin
					 ):

	def __init__(self):
		self.last_update = time.time()
		self.current = 0
		self.filament = True
		self.serial_instance = ""
		self.received_data = ""
		self.timer = None
		self._baud = BAUD
		self._port = PORT
		self.serial_instance = serial.Serial(self._port, self._baud)
		self._updateInterval = UPDATE_INTERVAL
		#self._logger.info("Serial started")


	def restartSerial(self):
		## close and destroy serial
		self.serial_instance.close()
		self.serial_instance.__del__()

		## open serial with new settings.
		self.serial_instance = serial.Serial(self._port, self._baud)


	def update_data(self):
		self.serial_instance.write(1)
		self.received_data = self.serial_instance.readline()
		parser = None
		parser = self.received_data.split(";")

		self.current = parser[0].split(=)[1]
		self.filament = parser[1].split(=)[1]

		self._logger.info("current is")
		self._logger.info(self.current)
		self._logger.info("filament is")
		self._logger.info(self.filament)

		self._plugin_manager.send_plugin_message(self._identifier, dict(current=self.current, filament = self.filament ))





	def startupTimer(self, UPDATE_INTERVAL):

		if self.timer:
			self.timer.cancel()
		self.timer = RepeatedTimer(UPDATE_INTERVAL, self.updateData, None, None, True)
		self.timer.start()


	## SettingsPlugin
	def get_settings_defaults(self):
		return dict(UPDATE_INTERVAL=self._updateInterval, BAUD = self._baud, PORT = self._port )

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

		self._updateInterval = self._settings.get(["UPDATE_INTERVAL"])
		self._baud = self._settings.get(["BAUD"])
		self._port = self._settings.get(["PORT"])

		self.restartSerial()

		self.startupTimer(self._updateInterval)


	pass

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "walrus"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = SkeletonPlugin()


