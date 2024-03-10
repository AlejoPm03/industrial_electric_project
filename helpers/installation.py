from enum import Enum
from typing import List

from helpers.environment import Environment

class InstallationType(Enum):
	SINGLE_PHASE = 1,
	TWO_PHASE = 2,
	THREE_PHASE = 3,
	EXCLUSIVE_TRANSFORMER = 4

	def __gt__(self, other):
		return self.value > other.value
	
	def __lt__(self, other):
		return self.value < other.value

class Installation():

	def __init__(self, environments: List[Environment], installation_type: InstallationType = None) -> None:
		self.environments = environments
		if installation_type and installation_type > self.minimum_installation_type():
			self.installation_type = installation_type
		else:
			self.installation_type = self.minimum_installation_type()
	
	@property
	def light_power(self):
		return sum([environment.light_power() for environment in self.environments])
	
	@property
	def light_number(self):
		return sum([environment.minimum_light_points() for environment in self.environments])
	
	@property
	def tug_power(self):
		return sum([environment.minimum_tug_power() for environment in self.environments])
	
	@property
	def tug_number(self):
		return sum([environment.minimum_tug_number() for environment in self.environments])
	
	@property
	def tue_power(self):
		return sum([environment.tue_power for environment in self.environments])
	
	@property
	def tue_number(self):
		return sum([environment.tue_number for environment in self.environments])

	@property
	def total_demanded_power(self):
		return (self.light_power + self.tug_power) * self.demand_factor_for_lighting_tug() + self.tue_power * self.demand_factor_for_tue(self.tue_number)

	@property
	def total_demanded_apparent_power(self):
		return self.total_demanded_power / 0.95
	
	@property
	def total_demanded_current(self):
		return self.total_demanded_power / (220 * self.phases)

	@property
	def input_branch_current(self):
		return self.total_demanded_current * 1.25

	@property
	def phases(self):
		if self.installation_type == InstallationType.SINGLE_PHASE:
			return 1
		if self.installation_type == InstallationType.TWO_PHASE:
			return 2
		return 3


	def minimum_installation_type(self) -> InstallationType:
		if self.total_demanded_power <= 15000:
			return InstallationType.SINGLE_PHASE
		if self.total_demanded_power <= 25000:
			return InstallationType.TWO_PHASE
		if self.total_demanded_power <= 50000:
			return InstallationType.THREE_PHASE
		return InstallationType.EXCLUSIVE_TRANSFORMER

	def demand_factor_for_lighting_tug(self):
		power = self.light_power + self.tug_power

		if power <= 1000:
			return 0.86
		if power <= 2000:
			return 0.75
		if power <= 3000:
			return 0.66
		if power <= 4000:
			return 0.59
		if power <= 5000:
			return 0.52
		if power <= 6000:
			return 0.45
		if power <= 7000:
			return 0.40
		if power <= 8000:
			return 0.35
		if power <= 9000:
			return 0.31
		if power <= 10000:
			return 0.27
		return 0.24

	def demand_factor_for_tue(self, number_of_tue):

		demand_factor_map = {
			1: 1.00,
			2: 1.00,
			3: 0.84,
			4: 0.76,
			5: 0.70,
			6: 0.65,
			7: 0.60,
			8: 0.57,
			9: 0.54,
			10: 0.52,
			11: 0.49,
			12: 0.48,
			13: 0.46,
			14: 0.45,
			15: 0.44,
			16: 0.43,
			17: 0.42,
			18: 0.41,
			19: 0.40,
			20: 0.40,
			21: 0.39,
			22: 0.39,
			23: 0.39,
			24: 0.38,
			25: 0.38
		}

		return demand_factor_map.get(number_of_tue, 0.38)

	def __str__(self) -> str:
		description = f"""
Installation:
	Light Power: {round(self.light_power, 2)}W
	Light Number: {round(self.light_number, 2)}
	Tug Power: {round(self.tug_power, 2)}W
	Tug Number: {round(self.tug_number, 2)}
	Tue Power: {round(self.tue_power, 2)}W
	Tue Number: {round(self.tue_number, 2)}
	Total Demanded Power: {round(self.total_demanded_power, 2)}W
	Installation Type: {self.installation_type}
	Phases: {self.phases}
	Total Demanded Apparent Power: {round(self.total_demanded_apparent_power, 2)}VA
	Total Demanded Current: {round(self.total_demanded_current, 2)}A
	Input Branch Current: {round(self.input_branch_current, 2)}A
"""
		environment_description = "\n".join([str(environment) for environment in self.environments])
		return description.strip() + "\n" + environment_description.strip()

