import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;

public class Elevator {
	private Floor currentFloor;
	private ArrayList<Passenger> passengers;
	private Boolean direction;
	private int floorsMoved;
	private int peopleMoved;
	
	public Elevator(Floor currentFloor) {
		this.currentFloor = currentFloor;
		this.passengers = new ArrayList<Passenger>();
		this.direction = true;
		this.floorsMoved = 0;
		this.peopleMoved = 0;
	}
	
	public int getTotalFloorsMoved() {
		return this.floorsMoved;
	}
	
	public int getTotalPeopleMoved() {
		return this.peopleMoved;
	}
	
	public void setDirection(Boolean newDirection) {
		this.direction = newDirection;
	}
	
	public Floor getCurrentFloor() {
		return this.currentFloor;
	}
	
	public Boolean getCurrentDirection() {
		return this.direction;
	}
	
	public void goUp() {
		if (this.currentFloor.getFloorAbove() != null) {
			this.currentFloor = this.currentFloor.getFloorAbove();
		} else {
			//We are at the top and need to switch directions
			this.direction = false; //true = Up, false = Down
		}
		this.floorsMoved++;
	}
	
	public void goDown() {
		if (this.currentFloor.getFloorBelow() != null) {
			this.currentFloor = this.currentFloor.getFloorBelow();
		} else {
			//We are at the top and need to switch directions
			this.direction = true; //true = Up, false = Down
		}
		this.floorsMoved++;
	}
	
	public ArrayList<Passenger> getPassengers() {
		return this.passengers;
	}
	
	public int getPassengerCount() {
		return this.passengers.size();
	}
	
	public void letPeopleOut() {
		for (int i = this.passengers.size() - 1; i >= 0; i--) {
			Passenger outPass = this.passengers.get(i);
			if (outPass.getDestinationFloor() == this.currentFloor) {
				this.currentFloor.receivePassenger(outPass);
				this.passengers.remove(outPass);
				outPass.arrived();
				this.peopleMoved++;
			}
		}
	}
	
	public void letPeopleIn() {
		ArrayList<Passenger> boardingThisWay = this.currentFloor.boardElevator(this.direction);
		for (int i = boardingThisWay.size() - 1; i >= 0; i--) {
			Passenger inPass = boardingThisWay.get(i);
			this.passengers.add(inPass);
			inPass.boarded();
			this.peopleMoved++;
		}
	}
	
	public Boolean peopleGettingOutHere() {
		for (Passenger possPass : this.passengers) {
			if (possPass.getDestinationFloor() == this.currentFloor) {
				return true;
			}
		}
		return false;
	}
	
	public Boolean peopleGettingInHere() {
		if (this.direction) {
			//true = Up
			return (this.currentFloor.getGoingUpCount() > 0);
		} else {
			//false = Down
			return (this.currentFloor.getGoingDownCount() > 0);
		}
	}
	
}