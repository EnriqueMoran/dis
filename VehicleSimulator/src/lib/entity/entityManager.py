import logging
import threading

from opendis.dis7 import (
    DeadReckoningParameters,
    EntityType,
    EntityMarking,
    EntityStatePdu,
    Vector3Float,
    Vector3Double,
    EulerAngles,
)

__author__ = "EnriqueMoran"

logger = logging.getLogger("EntityManager")

class EntityManager:

    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls) -> "EntityManager":
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):    # Check if instance has been already created
            self._capabilities = 0
            self._dead_reckoning_params = DeadReckoningParameters()
            self._entityAppearance = 0
            self._entityID = 0
            self._entityLinearVelocity = Vector3Float()
            self._entityLocation = Vector3Double()
            self._entityOrientation = EulerAngles()
            self._entityType = EntityType()
            self._forceId = 0
            self._marking = EntityMarking()
            self._numberOfVariableParameters = 0
            self._variableParameters = []
            self.initialized = True
        self._instance_lock = threading.Lock()
    
    def reset_data(self) -> None:
        with self._instance_lock:
            self._capabilities = 0
            self._dead_reckoning_params = DeadReckoningParameters()
            self._entityAppearance = 0
            self._entityID = 0
            self._entityLinearVelocity = Vector3Float()
            self._entityLocation = Vector3Double()
            self._entityOrientation = EulerAngles()
            self._entityType = EntityType()
            self._forceId = 0
            self._marking = EntityMarking()
            self._numberOfVariableParameters = 0
            self._variableParameters = []

    def set_data(self, pdu: EntityStatePdu) -> None:
        with self._instance_lock:
            self._capabilities = pdu.capabilities
            self._deadReckoningParameters = pdu.deadReckoningParameters
            self._entityAppearance = pdu.entityAppearance
            self._entityID = pdu.entityID.entityID
            self._entityLinearVelocity = pdu.entityLinearVelocity
            self._entityLocation = pdu.entityLocation
            self._entityOrientation = pdu.entityOrientation
            self._entityType = pdu.entityType
            self._forceId = pdu.forceId
            self._marking = pdu.marking
            self._numberOfVariableParameters = pdu.numberOfVariableParameters
            self._variableParameters = pdu.variableParameters
    
    def get_capabilities(self) -> int:
        with self._instance_lock:
            return self._capabilities

    def get_dead_reckoning_params(self) -> DeadReckoningParameters:
        with self._instance_lock:
            return self._dead_reckoning_params

    def get_entity_appearance(self) -> int:
        with self._instance_lock:
            return self._entityAppearance

    def get_entity_id(self) -> int:
        with self._instance_lock:
            return self._entityID

    def get_entity_linear_velocity(self) -> Vector3Float:
        with self._instance_lock:
            return self._entityLinearVelocity

    def get_entity_location(self) -> Vector3Double:
        with self._instance_lock:
            return self._entityLocation

    def get_entity_orientation(self) -> EulerAngles:
        with self._instance_lock:
            return self._entityOrientation
    
    def get_entity_type(self) -> EntityType:
        with self._instance_lock:
            return self._entityType
    
    def get_force_id(self) -> int:
        with self._instance_lock:
            return self._forceId
    
    def get_marking(self) -> EntityMarking:
        with self._instance_lock:
            return self._marking

    def get_number_of_variable_parameters(self) -> int:
        with self._instance_lock:
            return self._numberOfVariableParameters

    def get_variable_parameters(self) -> list:
        with self._instance_lock:
            return self._variableParameters
    
    def set_dead_reckoning_params(self, params: DeadReckoningParameters) -> None:
        with self._instance_lock:
            self._dead_reckoning_params = params

    def set_entity_appearance(self, appearance: int) -> None:
        with self._instance_lock:
            self._entityAppearance = appearance

    def set_entity_id(self, entity_id: int) -> None:
        with self._instance_lock:
            self._entityID = entity_id

    def set_entity_linear_velocity(self, velocity: Vector3Float) -> None:
        with self._instance_lock:
            self._entityLinearVelocity = velocity

    def set_entity_location(self, location: Vector3Double) -> None:
        with self._instance_lock:
            self._entityLocation = location

    def set_entity_orientation(self, orientation: EulerAngles) -> None:
        with self._instance_lock:
            self._entityOrientation = orientation

    def set_entity_type(self, entity_type: EntityType) -> None:
        with self._instance_lock:
            self._entityType = entity_type

    def set_force_id(self, force_id: int) -> None:
        with self._instance_lock:
            self._forceId = force_id

    def set_marking(self, marking: EntityMarking) -> None:
        with self._instance_lock:
            self._marking = marking

    def set_number_of_variable_parameters(self, num_params: int) -> None:
        with self._instance_lock:
            self._numberOfVariableParameters = num_params

    def set_variable_parameters(self, params: list) -> None:
        with self._instance_lock:
            self._variableParameters = params
    
    def set_capabilities(
        self,
        ammo_suply: bool = False,
        fuel_supply: bool = False,
        recovery: bool = False,
        repair: bool = False,
        ads_b: bool = False,
    ) -> None:
        with self._instance_lock:
            capabilities = 0b00000
            if ammo_suply:
                capabilities |= 0b00001
            if fuel_supply:
                capabilities |= 0b00010
            if recovery:
                capabilities |= 0b00100
            if repair:
                capabilities |= 0b01000
            if ads_b:
                capabilities |= 0b10000
            self.capabilities = capabilities
