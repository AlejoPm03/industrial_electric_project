from enum import Enum
from typing import List

from helpers.device import Light, Device
import math

class EnvironmentType(Enum):
	OFFICES_AND_CLASSROOMS = 0
	BEDROOMS = 1
	KITCHENS_AND_DINING_ROOMS = 2
	BATHROOMS_AND_OTHER_FACILITIES = 3
	VARIOUS = 4
	SHOPS_AND_COMMERCIAL_ESTABLISHMENTS = 6
	RESTAURANTS_CAFETERIAS_BARS_AND_HOTELS = 7
	WAITING_ROOMS_AND_COMMUNAL_AREAS = 8
	MACHINE_ROOMS_AND_EQUIPMENT = 9
	BANKS_AND_LIBRARIES = 10
	CHURCHES_AND_TEMPLES = 11
	LABORATORIES = 12
	CORRIDORS_STAIRCASES_CIRCULATION_AREAS_AND_LOCKER_ROOMS = 13
	WAREHOUSES_DEPOSITS_AND_STORAGE_AREAS = 14
	LAUNDRIES_AND_WORKSHOPS = 15
	MUSEUMS_EXHIBITIONS_AND_ART_GALLERIES = 16
	AUDITORIUMS_CINEMAS_AND_THEATRES = 17
	HOSPITALS = 18
	GARAGES = 19
	GYMS_AND_SPORTS_FACILITIES = 20
	TRANSPORT_TERMINALS = 21

class Environment:
	def __init__(self, name: str, w: float, h: float, type: EnvironmentType, light: Light, specific_devices: List[ Device ]) -> None:
		self.name = name
		self.width = w
		self.height = h
		self.type = type
		self.light = light
		self.specific_devices = specific_devices

	@property
	def area(self):
		return self.width * self.height

	@property
	def perimeter(self):
		return 2 * (self.width + self.height)
	
	@property
	def tug_power(self):
		return self.minimum_tug_power()
	
	@property
	def tug_number(self):
		return self.minimum_tug_number()
	
	@property
	def tue_number(self):
		return self.minimum_tue_number()
	
	@property
	def tue_power(self):
		return sum([device.power for device in self.specific_devices])


	@property
	def light_density_per_square_meter(self):
		density = {
			EnvironmentType.OFFICES_AND_CLASSROOMS: 12,
			EnvironmentType.BEDROOMS: 4,
			EnvironmentType.KITCHENS_AND_DINING_ROOMS: 10,
			EnvironmentType.BATHROOMS_AND_OTHER_FACILITIES: 10,
			EnvironmentType.VARIOUS: 14,
			EnvironmentType.SHOPS_AND_COMMERCIAL_ESTABLISHMENTS: 15,
			EnvironmentType.RESTAURANTS_CAFETERIAS_BARS_AND_HOTELS: 12,
			EnvironmentType.WAITING_ROOMS_AND_COMMUNAL_AREAS: 8,
			EnvironmentType.MACHINE_ROOMS_AND_EQUIPMENT: 6,
			EnvironmentType.BANKS_AND_LIBRARIES: 15,
			EnvironmentType.CHURCHES_AND_TEMPLES: 14,
			EnvironmentType.LABORATORIES: 20,
			EnvironmentType.CORRIDORS_STAIRCASES_CIRCULATION_AREAS_AND_LOCKER_ROOMS: 8,
			EnvironmentType.WAREHOUSES_DEPOSITS_AND_STORAGE_AREAS: 10,
			EnvironmentType.LAUNDRIES_AND_WORKSHOPS: 6,
			EnvironmentType.MUSEUMS_EXHIBITIONS_AND_ART_GALLERIES: 13,
			EnvironmentType.AUDITORIUMS_CINEMAS_AND_THEATRES: 18,
			EnvironmentType.HOSPITALS: 16,
			EnvironmentType.GARAGES: 2,
			EnvironmentType.GYMS_AND_SPORTS_FACILITIES: 20,
			EnvironmentType.TRANSPORT_TERMINALS: 9
		}

		return density.get(self.type, 13)

	def minimum_light_points(self):
		n = math.floor((self.recommended_power() * math.exp(-0.09 * self.area)) / self.light.power)
		return n + 1 if n & 1 else n

	def recommended_power(self):
		return self.area * self.light_density_per_square_meter

	def minimum_light_power(self):
		if self.area < 6:
			return 100
		return 100 + (math.floor((self.area - 6) / 4) * 60)

	def light_power(self):
		return max(self.minimum_light_power(), self.recommended_power())

	def minimum_tug_number(self):
		if self.type in [EnvironmentType.KITCHENS_AND_DINING_ROOMS, EnvironmentType.LAUNDRIES_AND_WORKSHOPS]:
			return max(math.ceil(self.perimeter / 3.5), 2)
		elif self.type in [EnvironmentType.BATHROOMS_AND_OTHER_FACILITIES]:
			return max(math.ceil(self.perimeter / 6), 2)
		elif self.type in [EnvironmentType.VARIOUS, EnvironmentType.GARAGES, EnvironmentType.CORRIDORS_STAIRCASES_CIRCULATION_AREAS_AND_LOCKER_ROOMS]:
			return max(math.ceil(self.perimeter / 6), 2)
		elif self.type in [EnvironmentType.SHOPS_AND_COMMERCIAL_ESTABLISHMENTS]:
			if self.area <= 40:
				return max(math.ceil(self.perimeter / 3), math.ceil(self.area / 4))
			else:
				return 10 + math.ceil((self.area - 40) / 10)
		else:
			if self.area <= 6:
				return 2
			else:
				return 1 + math.ceil(self.perimeter / 5)

	def minimum_tug_power(self):
		if self.type in [EnvironmentType.KITCHENS_AND_DINING_ROOMS, EnvironmentType.BATHROOMS_AND_OTHER_FACILITIES, EnvironmentType.LAUNDRIES_AND_WORKSHOPS]:
			tug_number = self.minimum_tug_number()
			if tug_number <= 3:
				return 600 * tug_number
			else:
				return 1800 + ((tug_number - 3) * 100)
		elif self.type == EnvironmentType.SHOPS_AND_COMMERCIAL_ESTABLISHMENTS:
			return 200 * self.minimum_tug_number()
		else:
			return 100 * self.minimum_tug_number()

	def minimum_tue_number(self):
		return len(self.specific_devices)
	
		
	
	def __str__(self) -> str:
		description = f"""
Enviroment: 
	Name: {self.name} - Area: {round(self.area, 2)}m² - Perimeter: {round(self.perimeter, 2)}m
	Light: 
		Light: {self.light}
		Recommended Power: {round(self.recommended_power(), 2)}W
		Minimum Light Power: {round(self.minimum_light_power(), 2)}W
		Light Power: {round(self.light_power(), 2)}W
		Minimum Light Points: {round(self.minimum_light_points(), 2)}
	Tug: 
		Minimum Tug Number: {round(self.minimum_tug_number(), 2)}
		Minimum Tug Power: {round(self.minimum_tug_power(), 2)}W
	Tue: 
		Minimum Tue Number: {round(self.minimum_tue_number(), 2)}
"""
		return description.strip()
	
