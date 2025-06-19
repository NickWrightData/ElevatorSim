import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;

public class Floor {
	private int floorNumber;
	private Floor floorBelow;
	private Floor floorAbove;
	private ArrayList<Passenger> goingUps;
	private ArrayList<Passenger> goingDowns;
	private ArrayList<Passenger> arrived;
	
	public Floor(int floorNumber, Floor floorBelow) {
		this.floorNumber = floorNumber;
		this.floorBelow = floorBelow;
		this.floorAbove = null;
		this.goingUps = new ArrayList<Passenger>();
		this.goingDowns = new ArrayList<Passenger>();
		this.arrived = new ArrayList<Passenger>();
	}
	
	public void setFloorAbove(Floor aboveFloor) {
		this.floorAbove = aboveFloor;
	}
	
	public int getFloorNumber() {
		return this.floorNumber;
	}
	
	public Floor getFloorAbove() {
		return this.floorAbove;
	}
	
	public Floor getFloorBelow() {
		return this.floorBelow;
	}
	
	public int getArrivedCount() {
		return this.arrived.size();
	}
	
	public void addNewPassenger(Passenger newPassenger) {
		if (newPassenger.getDirection()) {
			this.goingUps.add(newPassenger);
		} else {
			this.goingDowns.add(newPassenger);
		}
	}
	
	public void receivePassenger(Passenger receivedPassenger) {
		this.arrived.add(receivedPassenger);
	}
	
	public ArrayList<Passenger> boardElevator(Boolean direction) {
		if (direction) {
			ArrayList<Passenger> boardingList = Passenger.ArrayListPassCopy(this.goingUps);
			this.goingUps = new ArrayList<Passenger>();
			return boardingList;
		} else {
			ArrayList<Passenger> boardingList = Passenger.ArrayListPassCopy(this.goingDowns);
			this.goingDowns = new ArrayList<Passenger>();
			return boardingList;
		}
	}
	
	public int getGoingUpCount() {
		return this.goingUps.size();
	}
	
	public int getGoingDownCount() {
		return this.goingDowns.size();
	}
	
	public int getPeopleWaitingHere() {
		return this.getGoingUpCount() + this.getGoingDownCount();
	}
	
}