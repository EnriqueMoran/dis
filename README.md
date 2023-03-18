# DIS

Suite of entity simulators and exercise tools designed to run wargames using the DIS7 standard. It includes simulators for tanks, warships, troops, and fighter aircraft, as well as exercise management tools, scenario generators, and exercise visualizers.

Each simulator and tool is contenerized

## Components

### Exercise Manager

Allows to Start, stop, resume and terminate exercises.

#### Specific Behavior

- The realWorldTime and *simulationTime* fields in the *StartResumePdu* won't be used. The exercise will start once the PDU is received.
- Exercise freeze will be triggered by the value of the *Frozen Behavior field* (a value of 1 inficates excercise freeze).
- Exercise termination will be triggered by the value of the *Reason field* (a value of 2 indicates exercise termination).

#### Changelog

- 2023/03/10: Version 0.1, basic functionalities implemented. Allows to manage exercise status.


### Tank Simulator

Simulate generic tank components and basic behaviour.

#### Changelog


## Others

To run the apps, you must run the following command in host machine:
xhost +