import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;

public class Passenger {
	private LocalDateTime arrivalTime;
	private LocalDateTime boardingTime;
	private LocalDateTime requestTime;
	private Floor originFloor;
	private Floor destinationFloor;
	private Boolean direction; //True = Up; False = Down
	private int startTime;
	
	public Passenger(Floor originFloor, Floor destinationFloor, int startWaitTime) {
		this.originFloor = originFloor;
		this.destinationFloor = destinationFloor;
		this.direction = (this.originFloor.getFloorNumber() < this.destinationFloor.getFloorNumber());
		this.startTime = startWaitTime;
	}
	
	public static ArrayList<Passenger> ArrayListPassCopy(ArrayList<Passenger> toCopy) {
		ArrayList<Passenger> copy = new ArrayList<Passenger>(toCopy.size());
		for (Passenger pass : toCopy) {
			copy.add(pass);
		}
		return copy;
	}
	
	public int getStartTime() {
		return this.startTime;
	}
	
	public Boolean getDirection() {
		return this.direction;
	}
	
	public Floor getOriginFloor() {
		return this.originFloor;
	}
	
	public Floor getDestinationFloor() {
		return this.destinationFloor;
	}
	
	public void requestTransport() {
		LocalDateTime snapshot = LocalDateTime.now();
		this.requestTime = snapshot;
	}
	
	public void boarded() {
		LocalDateTime snapshot = LocalDateTime.now();
		this.boardingTime = snapshot;
	}
	
	public void arrived() {
		LocalDateTime snapshot = LocalDateTime.now();
		this.arrivalTime = snapshot;
	}
	
	public double getCurrentWaitTime() {
		return (double)ChronoUnit.MILLIS.between(this.requestTime, LocalDateTime.now())/1000;
	}
	
	public double getFinalWaitTime() {
		if (this.arrivalTime != null) {
			return (double)ChronoUnit.MILLIS.between(this.requestTime, this.arrivalTime)/1000;
		}
		return -1;
	}
}