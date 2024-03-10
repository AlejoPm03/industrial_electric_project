from enum import Enum

class Device:
	def __init__(self, name: str, power: float = None, power_factor: float = None, apparent_power: float = None) -> None:
		self.name = name
		self.power = self.get_power(power, power_factor, apparent_power)
		self.power_factor = self.get_power_factor(power, power_factor, apparent_power)
		self.apparent_power = self.get_apparent_power(power, power_factor, apparent_power)

		if not self.power:
			raise ValueError(f"Power not defined on {self.name}, two of the following must be defined: power, power_factor, apparent_power")
		
		if not self.power_factor:
			raise ValueError(f"Power factor not defined on {self.name}, two of the following must be defined: power, power_factor, apparent_power")
		
		if not self.apparent_power:
			raise ValueError(f"Apparent power not defined  on {self.name}, two of the following must be defined: power, power_factor, apparent_power")

	def get_apparent_power(self, power: float, power_factor: float, apparent_power: float) -> float:
		if apparent_power:
			return self.apparent_power
		
		if power and power_factor:
			return power / power_factor
		
		return None
	
	def get_power(self, power: float, power_factor: float, apparent_power: float) -> float:
		if power:
			return power
		
		if apparent_power and power_factor:
			return apparent_power * power_factor
		
		return None
	
	def get_power_factor(self, power: float, power_factor: float, apparent_power: float) -> float:
		if power_factor:
			return power_factor
		
		if power and apparent_power:
			return power / apparent_power
		
		return None
	
	def __str__(self) -> str:
		return f"{self.name} - {self.power} W - {self.power_factor} - {self.apparent_power} VA"

class LightType(Enum):
	INCANDESCENT = 0
	LED = 1
	COMPACT_FLUORESCENT = 2
	MIXED = 3
	LOW_PRESSURE_SODIUM = 4
	HIGH_PRESSURE_SODIUM = 5
	METAL_HALIDE = 6
	FLUORESCENT_WITH_STARTER_LOW_PF = 7
	QUICK_START_FLUORESCENT_LOW_PF = 8
	MERCURY_VAPOR_LOW_PF = 9
	FLUORESCENT_WITH_STARTER_HIGH_PF = 10
	QUICK_START_FLUORESCENT_HIGH_PF = 11
	MERCURY_VAPOR_HIGH_PF = 12

class Light(Device):
	def __init__(self, power: float, light_type: LightType, name: str = "Lampada") -> None:
		
		self.light_type = light_type

		super().__init__(name, power, self.get_power_factor_from_light_type())  

	def get_power_factor_from_light_type(self):
		return {
			LightType.INCANDESCENT: 1.0,
			LightType.LED: 0.65,  
			LightType.COMPACT_FLUORESCENT: 0.7,
			LightType.MIXED: 1.0,
			LightType.LOW_PRESSURE_SODIUM: 0.85,
			LightType.HIGH_PRESSURE_SODIUM: 0.4,
			LightType.METAL_HALIDE: 0.6,
			LightType.FLUORESCENT_WITH_STARTER_LOW_PF: 0.5,
			LightType.QUICK_START_FLUORESCENT_LOW_PF: 0.5,
			LightType.MERCURY_VAPOR_LOW_PF: 0.5,
			LightType.FLUORESCENT_WITH_STARTER_HIGH_PF: 0.85,
			LightType.QUICK_START_FLUORESCENT_HIGH_PF: 0.85,
			LightType.MERCURY_VAPOR_HIGH_PF: 0.85,
		}.get(self.light_type, 0.8)
	
	def __str__(self) -> str:
		return f"{self.name} - {round(self.power, 2)} W - PF: {round(self.power_factor, 2)} - {round(self.apparent_power, 2)} VA"


class Motor(Device):
	def __init__(self, power: float = None, power_factor: float = None, horse_power: float = None, efficiency: float = None,  name: str = "Motor") -> None:
		
		self.horse_power = self.get_horse_power(power, power_factor, horse_power, efficiency)

		if not self.horse_power:
			raise ValueError(f"Horse power not defined on {self.name}, two of the following must be defined: power, horse_power")

		power = self.horse_power * 746

		if not power_factor:
			power_factor = self.get_motor_power_factor(power, self.horse_power)

		super().__init__(name, power, power_factor)


	def get_horse_power(self, power: float, power_factor: float, horse_power: float, efficiency) -> float:
		if horse_power:
			return horse_power

		if power:
			power = power / 746
			return power + (power * (1 - efficiency))

		return None

	def get_motor_power_factor(self, power: float, horse_power: float) -> float:
		if (power < 600.0):
			return 0.5
		if (horse_power < 4.0):
			return 0.75
		if (horse_power < 50.0):
			return 0.85
		return 0.9


class AirConditioned(Device):
	def __init__(self, name: str = "Ar Condicionado", power: float = None, btu: float = None) -> None:
		if power and not btu:
			btu = power * 3412.14
		
		if btu and not power:
			power = btu / 3412.14
		
		if not power and not btu:
			raise ValueError(f"Power or BTU must be defined on {name}")

		self.btu = btu

		super().__init__(name, power, 0.8)