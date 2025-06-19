### Hello!  
My name is Nick Wright, and on June 17, 2025, I was given the following Coding Challenge for an interview:

>The Elevator  
>Provide code that simulates an elevator.  You may use any language (You can complete it in java(preferred) and Python if you would like to showcase your skills in both through separate elevator simulations).  
>Please upload your code Git Hub for a discussion during your interview with our team.  
>Additionally, document all assumptions and any features that weren't implemented.  
>Please be prepared to discuss the assumptions and features that were not implemented during your interview.  

After some time taken to code my answer to this challenge, I have uploaded both a Java and a Python version of the code here.  

Alongside the code in this repo (and matching information in this readme), I am also providing the requested Assumptions and Not-Implemented Features sections.  
_Note: most of these were written out during the initial brainstorming session; the rest of this brainstorming session will appear after these three sections._  

Thank you, and I hope you enjoy!  
Nick

## CODE  
-As stated, I have provided two implementations for this coding challenge, one in Java, and one in Python. They work almost identically, save for a few changes where necessary.  
_Note: These codebases do not interact; the Java files run completely independently from the Python file, and vice-versa._   
-In both cases, there are four "Elevator Brain" Solutions I provided, with slightly or largely varying behavior.  
_Note: Only one of these solutions should be uncommented at any one time when running either the Java or Python implementation. Please view the code for instructions on how to do this._  
-When the code is run, you will see a similar text-graphics-based "view" of the floors and the elevator, for both Java and Python.  
-The simulation is automatic once run; there is no runtime interactivity. However, before runtime, you are able to modify the "passenger_list" (a list of lists that provide the simulation time, the origin floor, and the destination floor for each passenger to add to the system.)  

## ASSUMPTIONS  
-I believe "Simulates an elevator" means to simulate the behavior of an elevator as it picks up and transports users.  
-I want to come up with my own solutions, so I did not look up popular/common/well-known elevator algorithms.  
-one elevator, one elevator shaft  
-ten floors (Floors 1-9 and Basement)* [Note: I ended up just using Floors 1-10]  
-normal controls (elevator does NOT know what exact floor a user wants to get to before picking them up, only knows "Up" or "Down" from a user's current floor)  
-requests for new floor transports can come in at any time  
-moving up or down requires no difference in power (counterweight means it's balanced already/not "easier" to let go slightly to allow the elevator to go down essentially "unpowered")  
-Elevator does not need to KNOW if there is anyone currently in the elevator (via weight sensors), it only needs to know if there are active transports.  
-Elevator does not get "overloaded" (too many people).  

## NOT-IMPLEMENTED FEATURES  
-Any user-facing functionality like lights, audible dings, doors opening and closing, "door close"/"door open" buttons, emergency buttons, etc.  
-Comparing all incoming requests and choose the "better/best one" based on overall wait time (might require a condition where if a user has been waiting on a floor for X amount of time, then stop everything and go serve them? Comparing and choosing might cause the elevator to get "caught in a loop" of quick, close tasks far away from another user.)  
-Emergency (Evacuate) button (also with below?)  
	--If pressed, Call operator (& 911?), Stop at next floor, Open doors  
-Emergency STOP button (also with above?)  
	--If pressed, Elevator stops immediately, Call operator (& 911?)  
-multiple elevator shafts  
-multiple elevators in the same shaft  
-memory of past usage (i.e. what time of day has most users likely to be on which floors)  
-slipping in "quicker and closer" elevator movements if no one is in the elevator and it's on the way to someone further away?  
-floor sensor to check total weight and refuse new passengers if over a specified amount  
	--also to see if users are in the elevator, otherwise cancel all in-progress transports and go get the person who's been waiting the longest?  
-lights on each floor signaling when an elevator is arriving (NOT when an elevator is coming to get you)  
-secure floors (where only some are allowed to go)  
-run-time interactivity (as in, "I want to add 20 people with random destinations to this floor all at once and see what happens".  

## Notes/The Rest of the Brainstorming Session  
GOAL: Minimize user wait time (INCLUDING time waiting for elevator to arrive after pressing a button), then distance traveled/time in use.  

Let's go through some common situations to get a feel for what this elevator will act like (parentheses after going Up/Down mean elevator won't know that until reaching the user):  

=1=  
-Elevator at F1, waiting  
Requests:  
-User A: F2 going Up (F7)  
A: Obviously, go to F2, pick up User A, go to F7, drop off User A.  

=2=  
-Elevator at F5, waiting  
Requests (almost simultaneous):  
-User A: F6 going Up (F8)  
-User B: F3 going Down (F1)  
A: IF I knew what floors users were going to, I'd probably go pick up User A for the quick drop-off, then get User B for the longer travel to minimize total user wait.  
IF comparing and choosing, then knowing just F6-up and F4-down, it depends on floor counts. There are 3 destinations above F6 (F7, F8, F9) and 3 below F3 (F2, F1, B), meaning it's a wash, and go fetch the person who pressed the button first. (Even if User B is closer--see =7=)  
Otherwise: FCFS (just go to the first person who pressed the button (User A), even if it resulted in a longer wait for User B)  

=3=  
-Elevator at F4, waiting  
Requests (almost simultaneous):  
-User A: F5 going Up (F8)  
-User B: F3 going Down (B)  
A: IF comparing & choosing: Knowing just F5-up and F3-down: There are 3 below F3 and 4 above F5, so get user B first since there's fewer floors below (the travel will likely be shorter--even though that's not actually true in this scenario)  
Otherwise: FCFS  

=4=  
-Elevator at F5  
-user A at F6 going Up (F8)  
-user B at F4 going Up (F7)  
A: IF comparing & choosing: DEFINITELY get user B first, since when done I'll already be on floor 7, for a quick 6-to-8.  
	-Math:  
		getting user A first: 1 up, then 2 up, then 4 down, then 3 up  
			=10 floors moved (4 down, 6 up)  
		getting user B first: 1 down, then 3 up, then 1 down, then 2 up  
			=7 floors moved (2 down, 5 up)  
Otherwise: FCFS  
(This also shows that I want to stay in the middle of the floors while waiting (quickest access to any floor) unless I have data regarding time of day and likelihood of floors I'll be picking up from/dropping off at.)  

=5=  
-Elevator at floor 5  
-user A: F4 going down (F1)  
-Elevator picks up user A and moves down  
-when Elevator at F2, User B: F3 going Down (F1)  
I've never had an elevator stop, *reverse course*, pick someone up, and then go back to its original destination. This would probably make people extremely annoyed or honestly even scared. "What is this elevator even doing??"  
A: Therefore, regardless: DON'T BREAK THE ELEVATOR PROMISE. Even if it would be just one floor of backtracking, do NOT interrupt a user's current transport to another floor to go *backwards*. (You absolutely can pick up new users that are going in the same direction, regardless of if their destination is before, at, or after the original destination; see =6=)  

=6=  
-Elevator at floor 7  
-user A at F6 going Down (F2)  
-Elevator picks up user A and moves Down  
-when Elevator at floor 5, User B requests floor 4 going Down.  
A: Pick up user B on the way. Regardless of whether user B wants to get off at floor 1, 2, or 3 (This is no longer in the elevator's hands; User B will press the button after boarding the elevator. That way, user A will know the next steps, that is, if there is another stop coming up before their destination related to the new passenger.)  

=7=  
-Elevator at F8  
-User A at F1 going Down (B)  
-Elevator begins to move down  
-When Elevator at F6: User B at F7 going up (F8)  
A: Elevator should NOT reverse course.  
	Math:  
		If reversing course:  
			User A: 8->7->6->7->8->1->B => 12 floors wait time + reverse + 2 pu/do  
			User B: 6->7->8 => 2 floors wait time + 1 pu/do  
		If not reversing course:  
			User A: 8->1->B => 8 floors wait time + 1 pu/do  
			User B: 7->B->7->8 => 15 floors wait time + 2 pu/do  
Unless I have values for pickup/dropoff, time taken to travel between floors, and time taken to reverse course (all would be required to prove that it's truly better to reverse course), I should stay the course and not reverse; User A requested the elevator first anyways.  

The rules SEEM to be:  
-If waiting: First come, first serve  
-If already going in a direction: keep picking up/dropping off people who are going in that direction (for now, ignoring people who want to go the opposite direction) until no more people want to go in that direction who are in that direction from you (above you for up, below for down)  
	-Then switch to the other direction and repeat until no more users are requesting transports  
(...but regardless of what they SEEM to be, what's great is we can use this simulation to test and find the optimal rules!)  

## Object-Oriented Design Brainstorming

Objects:  
-Floors  
	-floor ID (#)  
	-floor above  
	-floor below  
	-list of Passengers now waiting to go up  
	-list of Passengers now waiting to go down  
	-Bool for up button pressed (up_passengers > 0)  
	-Bool for down button pressed (down_passengers > 0)  
	-list of future Passengers who will request up or down  
	-list of Passengers who have arrived  
	
-Passenger  
	-starting floor  
	-desired floor  
	-up/down based on the above two  
	-up/down button press time  
	-arrival time  
	-total time waited  

-Elevator  
	-current floor  
	-going up or down  
	-list of Passengers aboard  
	
