import time
import os
import math

class Passenger:
    def __init__(self, origin_floor, destination_floor, start_wait_time):
        self._arrival_time = None
        self._boarding_time = None
        self._request_time = None
        self._origin_floor = origin_floor
        self._destination_floor = destination_floor
        self._direction = None
        self._start_time = start_wait_time

        # The following will set direction to True (Up) or False (Down) 
        # based on the provided floors.
        origin_floor_number = origin_floor.get_floor_number()
        destination_floor_number = destination_floor.get_floor_number()
        self._direction = (origin_floor_number < destination_floor_number)

    def get_start_time(self):
        return self._start_time

    def get_direction(self):
        return self._direction

    def get_starting_floor(self):
        return self._origin_floor

    def get_destination_floor(self):
        return self._destination_floor

    def request_transport(self):
        self._request_time = time.time()

    def boarded(self):
        self._boarding_time = time.time()

    def arrived(self):
        self._arrival_time = time.time()

    def get_curr_wait_time(self):
        return time.time() - self._request_time

    def get_final_wait_time(self):
        # Does not take into account boarding time, only button press time and arrival time
        if self._arrival_time is not None:
            return self._arrival_time - self._request_time
        else:
            return None


class Floor:
    def __init__(self, number, floor_below):
        # only setting the floor below, as the floor above hasn't been created yet
        self._number = number
        self._floor_below = floor_below
        self._floor_above = None
        self._going_ups = []
        self._going_downs = []
        self._arrived = []

    def set_floor_above(self, floor):
        if self._floor_above is None:
            self._floor_above = floor

    def get_floor_number(self):
        return self._number

    def get_floor_above(self):
        return self._floor_above

    def get_floor_below(self):
        return self._floor_below

    def get_arrived_count(self):
        return len(self._arrived)

    def add_new_passenger(self, new_passenger):
        if new_passenger.get_direction():
            # True = Up
            self._going_ups.append(new_passenger)
        else:
            # False = Down
            self._going_downs.append(new_passenger)

    def receive_passenger(self, received_passenger):
        self._arrived.append(received_passenger)

    def board_elevator(self, direction):
        if direction:
            # True = Up
            boarding_list = self._going_ups
            self._going_ups = []
            return boarding_list
        else:
            # False = Down
            boarding_list = self._going_downs
            self._going_downs = []
            return boarding_list

    def get_going_up_count(self):
        return len(self._going_ups)

    def get_going_down_count(self):
        return len(self._going_downs)

    def get_people_waiting_here(self):
        return self.get_going_up_count() + self.get_going_down_count()


class Elevator:
    def __init__(self, current_floor):
        self._current_floor = current_floor
        self._passengers = []
        self._direction = True  # True == Up, False == Down
        self._floors_moved = 0
        self._people_moved = 0

    def get_total_floors_moved(self) -> int:
        return self._floors_moved

    def get_total_people_moved(self) -> int:
        return self._people_moved

    def set_direction(self, direction):
        self._direction = direction

    def get_current_floor(self):
        return self._current_floor

    def get_current_direction(self):
        return self._direction

    def go_up(self):
        if self._current_floor.get_floor_above() is not None:
            self._current_floor = self._current_floor.get_floor_above()
            self._floors_moved += 1
        else:
            self._direction = False

    def go_down(self):
        if self._current_floor.get_floor_below() is not None:
            self._current_floor = self._current_floor.get_floor_below()
            self._floors_moved += 1
        else:
            self._direction = True

    def get_passengers(self):
        return self._passengers

    def get_passenger_count(self):
        return len(self._passengers)

    def let_people_out(self):
        for out_passenger in self._passengers:
            if out_passenger.get_destination_floor() == self._current_floor:
                self._current_floor.receive_passenger(out_passenger)
                self._passengers.remove(out_passenger)
                out_passenger.arrived()
                self._people_moved += 1

    def let_people_in(self):
        for in_passenger in self._current_floor.board_elevator(self._direction):
            self._passengers.append(in_passenger)
            in_passenger.boarded()
            # self._people_moved += 1

    def people_getting_out_here(self):
        for poss_pass in self._passengers:
            if poss_pass.get_destination_floor() == self._current_floor:
                return True
        return False

    def people_getting_in_here(self):
        if self.get_current_direction():
            # True = Up
            return self._current_floor.get_going_up_count() > 0
        else:
            # False = Down
            return self._current_floor.get_going_down_count() > 0


def get_bottom_floor(any_floor):
    curr_floor = any_floor
    # Go all the way down
    while curr_floor.get_floor_below() is not None:
        curr_floor = curr_floor.get_floor_below()
    return curr_floor


def get_top_floor(any_floor):
    curr_floor = any_floor
    # Go all the way down
    while curr_floor.get_floor_above() is not None:
        curr_floor = curr_floor.get_floor_above()
    return curr_floor


def get_all_up_down_counts(any_floor):
    curr_floor = get_bottom_floor(any_floor)
    going_up = 0
    going_down = 0

    going_up += curr_floor.get_going_up_count()
    going_down += curr_floor.get_going_down_count()

    # Starting at the bottom, go up and count the number of people who want to go up and who want to go down
    while curr_floor.get_floor_above() is not None:
        curr_floor = curr_floor.get_floor_above()
        going_up += curr_floor.get_going_up_count()
        going_down += curr_floor.get_going_down_count()

    return going_up, going_down


def people_waiting_above(curr_floor):
    waiting_above_count = 0

    while curr_floor.get_floor_above() is not None:
        curr_floor = curr_floor.get_floor_above()
        waiting_above_count += curr_floor.get_people_waiting_here()

    return waiting_above_count


def people_waiting_below(curr_floor):
    waiting_below_count = 0

    if curr_floor.get_floor_below() is not None:
        curr_floor = curr_floor.get_floor_below()

    while curr_floor.get_floor_below() is not None:
        waiting_below_count += curr_floor.get_people_waiting_here()
        curr_floor = curr_floor.get_floor_below()

    return waiting_below_count


def display_all_floors_and_data(any_floor, elevator_display, elapsed,
                                step, increase=False):
    os.system("cls")

    print("Elapsed Time:", elapsed)
    print("Floor     Up Dn Arr")
    print("--------------------")

    curr_floor = get_top_floor(any_floor)
    elevator_floor = elevator_display.get_current_floor().get_floor_number()

    while curr_floor is not None:
        if curr_floor.get_floor_number() == elevator_floor:
            curr_passengers = elevator_display.get_passengers()
            elevator_addon = "[" + str(elevator_display.get_passenger_count()) + ": "
            for curr_pass in curr_passengers:
                elevator_addon += str(
                    curr_pass.get_destination_floor().get_floor_number()) + " "
            elevator_addon += " ] "
        else:
            elevator_addon = "                "
        if curr_floor.get_floor_number() < 10:
            print("Floor  " + str(curr_floor.get_floor_number()) + ":",
                  curr_floor.get_going_up_count(),
                  " " + str(curr_floor.get_going_down_count()),
                  " " + str(curr_floor.get_arrived_count()),
                  " | " + elevator_addon)
        else:
            print("Floor", str(curr_floor.get_floor_number()) + ":",
                  curr_floor.get_going_up_count(),
                  " " + str(curr_floor.get_going_down_count()),
                  " " + str(curr_floor.get_arrived_count()),
                  " | " + elevator_addon)
        curr_floor = curr_floor.get_floor_below()

    if increase:
        time.sleep(step)
        return elapsed + 1
    return None


def create_floors(total_floors):
    curr_floor_count = 0

    # Create a floor at the bottom
    base_floor = Floor(1, None)  # No floor below bottom floor
    curr_floor = base_floor
    curr_floor_count += 1

    # Until there are no more floors to be created, create them
    while curr_floor_count < total_floors:
        # Create the new floor with the current floor as its floor below
        new_floor = Floor(curr_floor_count + 1, curr_floor)

        # Set the new floor as the floor above the current floor
        curr_floor.set_floor_above(new_floor)

        # Set the new floor as the current floor
        curr_floor = new_floor

        # Increment the floor count
        curr_floor_count += 1

    return base_floor


def find_floor(any_floor, floor_number):
    curr_floor = get_bottom_floor(any_floor)
    while (curr_floor is not None
           and curr_floor.get_floor_number() != floor_number
           and curr_floor.get_floor_above() is not None):
        curr_floor = curr_floor.get_floor_above()

    return curr_floor


if __name__ == '__main__':
    # Please set the total number of floors desired:
    floor_count = 10

    # Please set the time step in seconds:
    time_step = 0.5

    # Please set the start time:
    elapsed_time = 0

    # Please set the timings for the passenger arrivals
    # (1, 2, 3) means at simulation time of 1, a passenger on floor 2 will request floor 3.
    passenger_list = [
        (2, 5, 3),
        (20, 6, 9),
        (30, 10, 1),
        (40, 1, 10),
        (40, 2, 9),
        (40, 3, 8),
        (40, 4, 7),
        (40, 10, 1),
        (40, 9, 2),
        (40, 8, 3),
        (40, 7, 4),
        (46, 1, 7),
        (47, 3, 4),
        (48, 5, 3),
        (49, 8, 2),
        (50, 10, 7),
        (51, 7, 1),
        (52, 2, 8),
        (53, 8, 9),

    ]

    # Now creating the floors as a doubly-linked list and returning the bottom floor...
    bottom_floor = create_floors(floor_count)

    # Now creating the elevator and setting it at the bottom floor...
    elevator = Elevator(bottom_floor)

    # Now creating the passenger list...
    full_passenger_list = []

    # Now creating all the Passenger objects and adding them to the list...
    for (start_time, start_floor, dest_floor) in passenger_list:
        start_floor = find_floor(bottom_floor, start_floor)
        dest_floor = find_floor(bottom_floor, dest_floor)
        full_passenger_list.append(Passenger(start_floor, dest_floor, start_time))

    timing_passenger_list = full_passenger_list

    (up_counts, down_counts) = get_all_up_down_counts(
        elevator.get_current_floor())

    # Beginning the simulation...
    # NOTE: This is the "brains" of the elevator.
    # To try out different solutions, change the code below!
    while len(full_passenger_list) > 0 or elevator.get_passenger_count() > 0 or up_counts + down_counts > 0:

        # WARNING: PLEASE ENSURE ALL SOLUTIONS BELOW EXCEPT ONE IS COMMENTED OUT!
        # NOTE: There are four (4) solutions below.
        # INFO: To COMMENT OUT an entire Solution, simply remove the hash ('#') from in front of the solution.
        #		e.g. change "#''''SOLUTION #1: (...)"
        #			  ...to "''''SOLUTION #1: (...)"
        #		To UN-COMMENT OUT an entire Solution, simply add the forward slash back in:
        #		e.g. change "''''SOLUTION #1: (...)"
        #             ...to "#''''SOLUTION #1: (...)"

        # SOLUTION #1
        #''''SOLUTION #1: "Smart" solution (deciding to stop when no passengers are asking for transport;
        #				going up all the way until no more users above want to get picked up, repeat for down;
        #				checking if there are only users behind us; etc.)
        # Step 0: Initialize counts
        (up_counts, down_counts) = get_all_up_down_counts(
            elevator.get_current_floor())

        # Step 1: If there are people getting out, let them out!
        while elevator.people_getting_out_here():
            elevator.let_people_out()

            # Show all the floors, the elevator, and all their passenger data
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 2: If there are people getting in, let them in!
        while elevator.people_getting_in_here():
            elevator.let_people_in()
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 3: Check to see if any new people are waiting on any floor
        new_people = False
        while len(full_passenger_list) > 0 and full_passenger_list[0].get_start_time() <= elapsed_time:
            curr_passenger = full_passenger_list[0]
            curr_passenger.get_starting_floor().add_new_passenger(
                curr_passenger)
            curr_passenger.request_transport()
            full_passenger_list = full_passenger_list[1:]
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())
            new_people = True
        if new_people:
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 4: If people are in the elevator, keep going.
        #        Else, if we're going up and there are people above waiting,
        #            OR going down and people below waiting:
        #               keep going
        #        ELSE, if people are waiting above or below, they must be "behind" us;
        #               turn around!!
        #        IF "ALL ELSE'S" FAIL:
        #               do nothing; no one in elevator and no one waiting for it. Just wait.
        if elevator.get_passenger_count() > 0:
            if elevator.get_current_direction():
                # True = Up
                elevator.go_up()
            else:
                # False = Down
                elevator.go_down()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif elevator.get_current_direction() and people_waiting_above(
                elevator.get_current_floor()) > 0:
            # Keep going--there's more people to pick up above!
            elevator.go_up()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif elevator.get_current_direction() == False and people_waiting_below(
                elevator.get_current_floor()) > 0:
            # Keep going--there's more people to pick up below!
            elevator.go_down()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif up_counts > 0 or down_counts > 0:
            # There are only people waiting in the *opposite* direction!
            elevator.set_direction(not elevator.get_current_direction())

        else:
            # Do nothing; no passengers left, and no one is waiting on any floor.
            # (or, move to center floor to minimize potential movement?)
            pass

        # Step 6: re-draw the scene and pause for a second
        elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                   elapsed_time, time_step,
                                                   True)
        # '''

        # SOLUTION #2
        ''''SOLUTION #2: Ignore where possible passengers are;
        #                 just cocktail-shake the elevator back and forth until we're done.

        # Step 0: Initialize counts
        (up_counts, down_counts) = get_all_up_down_counts(
           elevator.get_current_floor())

        # Step 1: If there are people getting out, let them out!
        while elevator.people_getting_out_here():
            elevator.let_people_out()

            # Show all the floors, the elevator, and all their passenger data
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                      elapsed_time, time_step,
                                                      True)

        # Step 2: If there are people getting in, let them in!
        while elevator.people_getting_in_here():
            elevator.let_people_in()
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                      elapsed_time, time_step,
                                                      True)

        # Step 3: Check to see if any new people are waiting on any floor
        new_people = False
        while len(full_passenger_list) > 0 and full_passenger_list[0].get_start_time() <= elapsed_time:
            curr_passenger = full_passenger_list[0]
            curr_passenger.get_starting_floor().add_new_passenger(
                curr_passenger)
            curr_passenger.request_transport()
            full_passenger_list = full_passenger_list[1:]
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())
            new_people = True
        if new_people:
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 4: Keep moving the elevator, regardless of anything else.
        if elevator.get_current_direction():
            # True = Up
            elevator.go_up()
        else:
            # False = Down
            elevator.go_down()

        # Step 5: re-draw the scene and pause for a second
        elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                  elapsed_time, time_step,
                                                  True)
        # '''

        # SOLUTION #3
        ''''SOLUTION #3: The same as Solution 1, except we additionally move to the middle floor when no users are asking for transport
        # Step 0: Initialize counts
        (up_counts, down_counts) = get_all_up_down_counts(
            elevator.get_current_floor())

        # Step 1: If there are people getting out, let them out!
        while elevator.people_getting_out_here():
            elevator.let_people_out()

            # Show all the floors, the elevator, and all their passenger data
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 2: If there are people getting in, let them in!
        while elevator.people_getting_in_here():
            elevator.let_people_in()
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 3: Check to see if any new people are waiting on any floor
        new_people = False
        while len(full_passenger_list) > 0 and full_passenger_list[0].get_start_time() <= elapsed_time:
            curr_passenger = full_passenger_list[0]
            curr_passenger.get_starting_floor().add_new_passenger(
                curr_passenger)
            curr_passenger.request_transport()
            full_passenger_list = full_passenger_list[1:]
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())
            new_people = True
        if new_people:
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 4: If people are in the elevator, keep going.
        #        Else, if we're going up and there are people above waiting,
        #            OR going down and people below waiting:
        #               keep going
        #        ELSE, if people are waiting above or below, they must be "behind" us;
        #               turn around!!
        #        IF "ALL ELSE'S" FAIL:
        #               do nothing; no one in elevator and no one waiting for it. Just wait.
        if elevator.get_passenger_count() > 0:
            if elevator.get_current_direction():
                # True = Up
                elevator.go_up()
            else:
                # False = Down
                elevator.go_down()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif elevator.get_current_direction() and people_waiting_above(
                elevator.get_current_floor()) > 0:
            # Keep going--there's more people to pick up above!
            elevator.go_up()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif elevator.get_current_direction() == False and people_waiting_below(
                elevator.get_current_floor()) > 0:
            # Keep going--there's more people to pick up below!
            elevator.go_down()
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())

        elif up_counts > 0 or down_counts > 0:
            # There are only people waiting in the *opposite* direction!
            elevator.set_direction(not elevator.get_current_direction())

        else:
            # No passengers left, and no one is waiting on any floor.
            # Move to the (lower) middle floor.
            #	e.g. 10 floors? move to 5, not 6. (floor 5 would be the exact and only middle floor with 9 floors total)
            goal_floor = math.floor(floor_count/2)
            if elevator.get_current_floor().get_floor_number() < goal_floor:
                elevator.go_up()
            elif elevator.get_current_floor().get_floor_number() > goal_floor:
                elevator.go_down()
            else:
                # We're were we need to be. Do nothing.
                pass

        # Step 5: re-draw the scene and pause for a second
        elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                   elapsed_time, time_step,
                                                   True)
        # '''

        # SOLUTION #4
        ''''SOLUTION #4: Same as Solution #2, except we move to the middle and stop if there are no users left to pick up at the moment

        # Step 0: Initialize counts
        (up_counts, down_counts) = get_all_up_down_counts(
           elevator.get_current_floor())

        # Step 1: If there are people getting out, let them out!
        while elevator.people_getting_out_here():
            elevator.let_people_out()

            # Show all the floors, the elevator, and all their passenger data
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                      elapsed_time, time_step,
                                                      True)

        # Step 2: If there are people getting in, let them in!
        while elevator.people_getting_in_here():
            elevator.let_people_in()
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                      elapsed_time, time_step,
                                                      True)

        # Step 3: Check to see if any new people are waiting on any floor
        new_people = False
        while len(full_passenger_list) > 0 and full_passenger_list[0].get_start_time() <= elapsed_time:
            curr_passenger = full_passenger_list[0]
            curr_passenger.get_starting_floor().add_new_passenger(
                curr_passenger)
            curr_passenger.request_transport()
            full_passenger_list = full_passenger_list[1:]
            (up_counts, down_counts) = get_all_up_down_counts(
                elevator.get_current_floor())
            new_people = True
        if new_people:
            elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                       elapsed_time, time_step,
                                                       True)

        # Step 4:  If there are people waiting above or below, or people in the elevator, just keep moving!
        #			Else, move to the middle and stop.
        (up_counts, down_counts) = get_all_up_down_counts(
            elevator.get_current_floor())
        if (up_counts > 0 or down_counts > 0 or elevator.get_passenger_count() > 0
                or elevator.get_current_floor().get_people_waiting_here() > 0):
            # Keep moving!
            if elevator.get_current_direction():
                elevator.go_up()
            else:
                elevator.go_down()
        elif up_counts == 0 and down_counts == 0 and elevator.get_passenger_count() == 0:
            # No passengers left, and no one is waiting on any floor.
            # Move to the (lower) middle floor.
            #	e.g. 10 floors? move to 5, not 6. (floor 5 would be the exact and only middle floor with 9 floors total)
            goal_floor = math.floor(floor_count / 2)
            if elevator.get_current_floor().get_floor_number() < goal_floor:
                elevator.go_up()
                elevator.set_direction(True)
            elif elevator.get_current_floor().get_floor_number() > goal_floor:
                elevator.go_down()
                elevator.set_direction(False)
            else:
                # We're were we need to be. Do nothing.
                pass

        # Step 5: re-draw the scene and pause for a second
        elapsed_time = display_all_floors_and_data(bottom_floor, elevator,
                                                  elapsed_time, time_step,
                                                  True)
        # '''

    total_passenger_wait_time = 0
    longest_wait_time = 0

    for passenger in timing_passenger_list:
        curr_pass_wait_time = passenger.get_final_wait_time()
        total_passenger_wait_time += curr_pass_wait_time
        if longest_wait_time < curr_pass_wait_time:
            longest_wait_time = curr_pass_wait_time

    print("FINAL COMBINED PASSENGERS' WAIT TIME: ", total_passenger_wait_time)
    print("LONGEST WAIT TIME FOR ANY ONE PASSENGER: ", longest_wait_time)
    print("TOTAL FLOORS MOVED: ", elevator.get_total_floors_moved())
    print("TOTAL PEOPLE MOVED: ", elevator.get_total_people_moved())
