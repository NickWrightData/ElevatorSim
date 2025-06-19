import java.util.ArrayList;

public class ElevatorSim {
	public static void main(String[] args) {
		//Please set the total number of floors desired:
		int floorCount = 10;
		
		//Please set the time step in seconds:
		double timeStep = 0.1;
		
		//Please set the start time:
		int elapsedTime = 0;
		
		//Please set the timings for the passenger arrivals
		//(1, 2, 3) means at simulation time of 1, a passenger on floor 2 will request floor 3.
		int[][] passengerList = {{2,5,3},
			{20, 6, 9},
			{30, 10, 1},
			{40, 1, 10},
			{40, 2, 9},
			{40, 3, 8},
			{40, 4, 7},
			{40, 10, 1},
			{40, 9, 2},
			{40, 8, 3},
			{40, 7, 4},
			{46, 1, 7},
			{47, 3, 4},
			{48, 5, 3},
			{49, 8, 2},
			{50, 10, 7},
			{51, 7, 1},
			{52, 2, 8},
			{53, 8, 9}};
			
		//Now creating the floors as a doubly-linked list and returning the bottom floor...
		Floor bottomFloor = createFloors(floorCount);
		
		//Now creating the elevator and setting it at the bottom floor...
		Elevator elevator = new Elevator(bottomFloor);
		
		//Now creating the passenger list...
		ArrayList<Passenger> fullPassengerList = new ArrayList<Passenger>();
		
		//Now creating all the Passenger objects and adding them to the list...
		for (int[] set : passengerList) {
			int startTimeNumber = set[0];
			int startFloorNumber = set[1];
			int destFloorNumber = set[2];
			Floor startFloor = findFloor(bottomFloor, startFloorNumber);
			Floor destFloor = findFloor(bottomFloor, destFloorNumber);
			fullPassengerList.add(new Passenger(startFloor, destFloor, startTimeNumber));
		}
		
		ArrayList<Passenger> timingPassengerList = Passenger.ArrayListPassCopy(fullPassengerList);
		
		int[] counts = getAllUpDownCounts(elevator.getCurrentFloor());
		
		while (fullPassengerList.size() > 0 || elevator.getPassengerCount() > 0 || counts[0]+counts[1] > 0) {
			//Step 0: Initialize counts
			counts = getAllUpDownCounts(elevator.getCurrentFloor());
			
			//Step 1: If there are people getting out, let them out!
			while (elevator.peopleGettingOutHere()) {
				elevator.letPeopleOut();
				elapsedTime = displayAllFloorsAndData(bottomFloor, elevator, elapsedTime, timeStep, true);
			}
			
			//Step 2: If there are people getting in, let them in!
			while (elevator.peopleGettingInHere()) {
				elevator.letPeopleIn();
				elapsedTime = displayAllFloorsAndData(bottomFloor, elevator, elapsedTime, timeStep, true);
			}
			
			//Step 3: Check to see if any new people are waiting on any floor
			boolean newPeople = false;
			while (fullPassengerList.size() > 0 && fullPassengerList.get(0).getStartTime() <= elapsedTime) {
				Passenger currPassenger = fullPassengerList.get(0);
				currPassenger.getOriginFloor().addNewPassenger(currPassenger);
				currPassenger.requestTransport();
				fullPassengerList.remove(currPassenger);
				counts = getAllUpDownCounts(elevator.getCurrentFloor());
				newPeople = true;
			}
				
			if (newPeople) {
				elapsedTime = displayAllFloorsAndData(bottomFloor, elevator, elapsedTime, timeStep, true);
			}
			
			/* Step 4: If people are in the elevator, keep going.
			         Else, if we're going up and there are people above waiting,
			             OR going down and people below waiting:
			                keep going
			         ELSE, if people are waiting above or below, they must be "behind" us;
			                turn around!!
			         IF "ALL ELSE'S" FAIL:
			                do nothing; no one in elevator and no one waiting for it. Just wait.*/
			if (elevator.getPassengerCount() > 0) {
				if (elevator.getCurrentDirection()) {
					//true = Up
					elevator.goUp();
				} else {
					//false = Down
					elevator.goDown();
				}
				counts = getAllUpDownCounts(elevator.getCurrentFloor());
			} else if (elevator.getCurrentDirection() && peopleWaitingAbove(elevator.getCurrentFloor()) > 0) {
				//Keep going--there's more people to pick up above!
				elevator.goUp();
				counts = getAllUpDownCounts(elevator.getCurrentFloor());
			} else if (!(elevator.getCurrentDirection()) &&  peopleWaitingBelow(elevator.getCurrentFloor()) > 0) {
				//Keep going--there's more people to pick up below!
				elevator.goDown();
				counts = getAllUpDownCounts(elevator.getCurrentFloor());
			} else if (counts[0] > 0 || counts[1] > 0) {
				//There are only people waiting in the *opposite* direction!
				elevator.setDirection(!elevator.getCurrentDirection());
			} else {
				//Do nothing; no passengers left, and no one is waiting on any floor.
				//(or, move to center floor to minimize potential movement?)
				;
			}
			
			//Step 6: re-draw the scene and pause for a second
			elapsedTime = displayAllFloorsAndData(bottomFloor, elevator, elapsedTime, timeStep, true);
		}
		
		double totalPassengerWaitTime = 0;
		double longestWaitTime = 0;
		
		for (Passenger passenger : timingPassengerList) {
			double currPassWaitTime = passenger.getFinalWaitTime();
			totalPassengerWaitTime += currPassWaitTime;
			if (longestWaitTime < currPassWaitTime) {
				longestWaitTime = currPassWaitTime;
			}
		}
		
		System.out.println("FINAL COMBINED PASSENGERS' WAIT TIME: " + totalPassengerWaitTime);
		System.out.println("LONGEST WAIT TIME FOR ANY PASSENGER: " + longestWaitTime);
		System.out.println("TOTAL FLOORS MOVED: " + elevator.getTotalFloorsMoved());
		System.out.println("TOTAL PEOPLE MOVED: " + elevator.getTotalPeopleMoved());
	}

	public static void sleep(int mils) {
		try {
			Thread.sleep(mils);
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
	}
	
	public static Floor getBottomFloor(Floor anyFloor) {
		Floor currFloor = anyFloor;
		//Go all the way down
		while (currFloor.getFloorBelow() != null) {
			currFloor = currFloor.getFloorBelow();
		}
		return currFloor;
	}
	
	public static Floor getTopFloor(Floor anyFloor) {
		Floor currFloor = anyFloor;
		//Go all the way down
		while (currFloor.getFloorAbove() != null) {
			currFloor = currFloor.getFloorAbove();
		}
		return currFloor;
	}
	
	public static int[] getAllUpDownCounts(Floor anyFloor) {
		Floor currFloor = anyFloor;
		int goingUp = 0;
		int goingDown = 0;
		
		goingUp += currFloor.getGoingUpCount();
		goingDown += currFloor.getGoingDownCount();
		
		//Starting at the bottom, go up and count the number of people who want to go up and who want to go down
		while (currFloor.getFloorAbove() != null) {
			currFloor = currFloor.getFloorAbove();
			goingUp += currFloor.getGoingUpCount();
			goingDown += currFloor.getGoingDownCount();
		}
		
		return new int[] {goingUp, goingDown};
	}
	
	public static int peopleWaitingAbove(Floor currFloor) {
		int waitingAboveCount = 0;
		
		while (currFloor.getFloorAbove() != null) {
			currFloor = currFloor.getFloorAbove();
			waitingAboveCount += currFloor.getPeopleWaitingHere();
		}
		
		return waitingAboveCount;
	}
	
	public static int peopleWaitingBelow(Floor currFloor) {
		int waitingBelowCount = 0;
		
		while (currFloor.getFloorBelow() != null) {
			currFloor = currFloor.getFloorBelow();
			waitingBelowCount += currFloor.getPeopleWaitingHere();
		}
		
		return waitingBelowCount;
	}
	
	public static int displayAllFloorsAndData(Floor anyFloor, Elevator elevator, int elapsed, double step, Boolean increase) {
		clearScreen();
		
		System.out.println("Elapsed Time: " + elapsed);
		System.out.println("Floor     Up Dn Arr");
		System.out.println("--------------------");
		
		Floor currFloor = getTopFloor(anyFloor);
		int elevatorFloor = elevator.getCurrentFloor().getFloorNumber();
		
		String elevatorAddon = "";
		
		while (currFloor != null) {
			if (currFloor.getFloorNumber() == elevatorFloor) {
				ArrayList<Passenger> currPassengers = elevator.getPassengers();
				elevatorAddon = "[" + elevator.getPassengerCount() + ": ";
				for (Passenger currPassenger : currPassengers) {
					elevatorAddon += currPassenger.getDestinationFloor().getFloorNumber() + " ";
				}
				elevatorAddon += "]";
			} else {
				elevatorAddon = "                ";
			}
			
			if (currFloor.getFloorNumber() < 10) {
				System.out.println("Floor 0" + currFloor.getFloorNumber() + ": " 
									+ currFloor.getGoingUpCount() + " "
									+ currFloor.getGoingDownCount() + " "
									+ currFloor.getArrivedCount() + " | " + elevatorAddon);
			} else {
				System.out.println("Floor " + currFloor.getFloorNumber() + ": " 
									+ currFloor.getGoingUpCount() + " "
									+ currFloor.getGoingDownCount() + " "
									+ currFloor.getArrivedCount() + " | " + elevatorAddon);
			}
			
			currFloor = currFloor.getFloorBelow();
		}
		
		if (increase) {
			sleep((int)(step * 1000.0));
			return elapsed + 1;
		}
		
		return -1;
	}
	
	public static Floor createFloors(int totalFloors) {
		int currFloorCount = 0;
		
		//Create a floor at the bottom
		Floor baseFloor = new Floor(1, null); //No floor below the bottom floor
		Floor currFloor = baseFloor;
		currFloorCount += 1;
		
		while (currFloorCount < totalFloors) {
			//Create the new floor with the current floor as its floor below
			Floor newFloor = new Floor(currFloorCount + 1, currFloor);
			
			//Set the new floor as the floor above the current floor
			currFloor.setFloorAbove(newFloor);
			
			//Set the new floor as the current floor
			currFloor = newFloor;
			
			//Increment the floor count
			currFloorCount += 1;
		}
		
		return baseFloor;
	}
	
	public static Floor findFloor(Floor anyFloor, int floorNumber) {
		Floor currFloor = getBottomFloor(anyFloor);
		while (currFloor != null && currFloor.getFloorNumber() != floorNumber) {
			currFloor = currFloor.getFloorAbove();
		}
		return currFloor;
	}
	
	public static void clearScreen() {  
		System.out.print("\033[H\033[2J");  
		System.out.flush();
	}  
}