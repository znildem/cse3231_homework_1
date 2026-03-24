# CSE 3231 - Homework 1
# Sliding Window Algorithm Simulation
# Group Name: BAYRAK_ILDEM
# Student 1: Elif Dila Bayrak, 904086652
# Student 2: Zeynep Neva Ildem, 904034285

import sys
import random

def parse_arguments():
    """
    Parse command-line arguments.

    Expected inputs:
    - Duration: Total number of time steps
    - SWS: Sender Window Size
    - RWS: Receiver Window Size
    - error_rate: timeout duration for retranmission
    
    Return all values in appropriate types.
    """
    if len(sys.argv) != 6:
        print("Usage: python main.py <duration> <sws> <rws> <error_rate> <timeout>")
        sys.exit(1)

    try:
        duration = int(sys.argv[1])
        sws = int(sys.argv[2])
        rws = int(sys.argv[3])
        error_rate = float(sys.argv[4])
        timeout = int(sys.argv[5])
    except ValueError:
        print("Invalid argument types. Please ensure duration, sws, rws, and timeout are integers, and error_rate is a float.")
        sys.exit(1)

    return duration, sws, rws, error_rate, timeout

def initialize_sender(sws):
    """
    Initialize sender's state.

    Should include:
    - Current window (frames in flight)
    - Last Frame Sent (LFS)
    - Timers for each frame (for timeout tracking)

    Return a sender state object (dict or custom structure).
    """
    sender = {}

    # List to store frames currently in the sender window (frames in flight)
    sender["window"] = []

    # Last Frame Sent (LFS)
    # Starts at -1 because no frames have been sent yet
    sender["LFS"] = -1

    # Dictionary to track timers for each frame in the sender window
    # Key: frame ID
    # Value: time step when the frame was sent (for timeout tracking)
    sender["timers"] = {}

    # Store sender window size (useful later for checking limits)
    sender["sws"] = sws

    return sender

def initialize_receiver(rws):
    """"
    Initialize receiver's state.

    Should include:
    - receiver window range
    - last frame received in order
    - buffer for out-of-order frames

    Return a receiver state object .
    """
    receiver = {}

    # Receiver Window Size
    receiver["rws"] = rws

    # Last Frame Received in order (LFR)
    # Starts at -1 because no frames have been received yet
    receiver["last_frame_received"] = -1

    # Largest Acceptable Frame (LAF)
    # Defines the upper bound of the receiver window
    receiver["largest_acceptable_frame"] = receiver["last_frame_received"] + rws

    # Buffer to store out-of-order frames
    # Using a list
    receiver["buffer"] = []

    return receiver

def generate_frame_sequence(sws):
    """
    Generate sequence number space based on window size.
    
    Typically:
    - Sequence numbers wrap around
    - Size is usually related to window size (e.g., sws + 1 or power of 2)
    
    Return a list or range of valid frame IDs.
    """
    # Sequence number space size
    # Using sws + 1 to avoid ambiguity between full and empty window
    seq_size = sws + 1

    # Generate sequence numbers from 0 to seq_size - 1
    sequence = list(range(seq_size))

    return sequence

def sender_send_frames(sender, sws, current_time):
    """
    Decide which frames the sender transmits at this time step.
    
    Should:
    - Check available space in sender window
    - Send new frames if possible
    - Update LFS (Last Frame Sent)
    - Start timers for new frames
    
    Return:
    - List of frames sent in this time step
    """
    sent_frames = []

    # Keep sending new frames until the sender window is full
    while len(sender["window"]) < sws:
        next_frame = sender["LFS"] + 1

        sender["window"].append(next_frame)
        sender["LFS"] = next_frame
        # Start timer for this frame
        sender["timers"][next_frame] = current_time
        sent_frames.append(next_frame)

        # Return the list of frames sent during this time step
    return sent_frames

def simulate_channel(frames, error_rate):
    """
    Simulate transmission over the channel.
    
    Should:
    - Randomly decide if each frame is corrputed based on error_rate
    - Mark corrputed frames (e.g., with '?'
    
    Return:
    - List of recieved frames (with corruption if applicable)
    """
    received_frames = []

    # Loop through each frame being transmitted
    for frame in frames:
        # Generate a random number between 0 and 1
        random_value = random.random()

        # If the random value is less than error_rate, mark as corrupted
        if random_value < error_rate:
            # Mark the frame as corrupted (using '?')
            received_frames.append('?')
        else:
            # Otherwise, the frame is received correctly
            received_frames.append(frame)

    return received_frames

def receiver_process_frames(receiver, frames):
    """
    Process incoming frames at the receiver.
    
    Should:
    - Accept frames within receiver window
    - Discard frame outside window
    - Buffer out-of-order frames
    - Update last frame received in order
    - Generate ACKs
    
    Return:
    - Updates receiver state
    - ACK(s) to send back
    """
    # Default ACK = last frame received in order (cumulative ACK)
    ack = receiver["last_frame_received"]

    for frame in frames:
        # If frame is corrupted, ignore it (no update)
        if frame == '?':
            continue

        # Compute current receiver window bounds
        lower_bound = receiver["last_frame_received"] + 1
        upper_bound = receiver["largest_acceptable_frame"]

        # Check if frame is within the receiver window
        if lower_bound <= frame <= upper_bound:
            # If frame is the next expected frame (in order)
            if frame == lower_bound:
                receiver["last_frame_received"] = frame

                # Check buffer for the next in-order frames
                # Keep advancing LFR if buffered frames are available
                while (receiver["last_frame_received"] + 1) in receiver["buffer"]:
                    next_in_order = receiver["last_frame_received"] + 1
                    receiver["buffer"].remove(next_in_order)
                    receiver["last_frame_received"] = next_in_order

            else:
                # Out-of-order frame, store in buffer if not already there
                if frame not in receiver["buffer"]:
                    receiver["buffer"].append(frame)

                    # Keep buffer sorted for easier processing
                    receiver["buffer"].sort()
        else:
            # Frame is outside the receiver window, so discard it
            pass

    # Update largest acceptable frame (LAF)
    receiver["largest_acceptable_frame"] = receiver["last_frame_received"] + receiver["rws"]

    # Update ACK (cumulative ACK = last in-order frame)
    ack = receiver["last_frame_received"]

    return receiver, ack


def sender_receive_ack(sender, ack, current_time):
    """
    Process ACK at sender.
    
    Should:
    - Remove acknowledged frames from window
    - Update sender state
    - Reset timers as needed
    """
    # If ACK is corrupted or missing, ignore it
    if ack == '?' or ack is None:
        return
    
    # Remove all frames from the sender window that are:
    # less than or equal to the ACK value
    acknowledged_frames = []

    for frame in sender["window"]:
        if frame <= ack:
            acknowledged_frames.append(frame)

    # Remove acknowledged frames from the sender window
    for frame in acknowledged_frames:
        sender["window"].remove(frame)

        # Remove timers for acknowledged frames
        if frame in sender["timers"]:
            del sender["timers"][frame]

def check_timeouts(sender, timeout, current_time):
    """
    Check for frames that timed out.
    
    Should:
    - Identify frames whose timers exceeded timeout
    - Mark them for retransmission
    
    Return:
    - List of frames to retransmit
    """
    retransmit_frames = []

    # Loop through all active timers
    for frame, send_time in sender["timers"].items():

        # Check if the frame has exceeded the timeout
        if current_time - send_time >= timeout:
            # Mark the frame for retransmission
            retransmit_frames.append(frame)

    # Reset timers for retransmitted frames
    # Since they are being "resent" at current_time
    for frame in retransmit_frames:
        sender["timers"][frame] = current_time

    return retransmit_frames

def print_header(duration, sws, rws, error_rate, timeout, sequence):
    """
    Print simulation header.
    
    Should include:
    - Student names/IDs
    - Group name
    - Parameters
    - Sequence number space
    """
    print("CSE 3231 - Homework 1")
    print("Sliding Window Algorithm Simulation")

    print("Group Name: BAYRAK_ILDEM")
    print("Student 1: Elif Dila Bayrak, 904086652")
    print("Student 2: Zeynep Neva Ildem, 904034285")

    print("\nSimulation Parameters:")
    print(f"Duration: {duration} time steps")
    print(f"Sender Window Size (SWS): {sws}")
    print(f"Receiver Window Size (RWS): {rws}")
    print(f"Error Rate: {error_rate}")
    print(f"Timeout Duration: {timeout} time steps")

    print(f"Sequence Number Space: ")
    print(sequence)

    print("\nSimulation Start...\n")

def print_timestep(t, sent_frame, ack_received, lfs, last_frame_received, largest_acceptable_frame, receiver_buffer):
    """
    Print one row of the simulation table.
    
    Columns should match assignment format:
    - Time step
    - Frame sent
    - ACK reseived
    - LFS
    - Last frame recived
    - Largest acceptable frame
    - Receiver buffer contents
    """
    # Format sent frames to strings from a list
    sent_str = ", ".join(str(frame) for frame in sent_frame) if sent_frame else "None"

    # Format ACK
    if isinstance(ack_received, list):
        ack_str = ", ".join(str(ack) for ack in ack_received)
    elif ack_received is None:
        ack_str = "-"
    else:
        ack_str = str(ack_received)

    # Format receiver buffer contents
    buffer_str = ", ".join(str(frame) for frame in receiver_buffer) if receiver_buffer else "Empty"

    # Print row
    print(f"{t:<5} | {sent_str:<10} | {ack_str:<10} | {lfs:<5} | {last_frame_received:<10} | {largest_acceptable_frame:<10} | {buffer_str}")

def main():
    duration, sws, rws, error_rate, timeout = parse_arguments()

    sender = initialize_sender(sws)
    receiver = initialize_receiver(rws)

    sequence = generate_frame_sequence(sws)

    print_header(duration, sws, rws, error_rate, timeout, sequence)
    print(f"{'t':<5} | {'Sent':<10} | {'ACK':<10} | {'LFS':<5} | {'LFR':<10} | {'LAF':<10} | {'Buffer'}")
    print("-" * 80)

    for t in range(duration):
        # 1. Check for timeouts and mark frames for retransmission
        retransmissions = check_timeouts(sender, timeout, t)

        # 2. Send new frames if there is still room in the sender window
        new_frames = sender_send_frames(sender, sws, t)

        # 3. Frames actually sent this time step = retransmissions + new frames
        sent_frames = retransmissions + new_frames

        # 4. Channel simulates transmission
        received_frames = simulate_channel(sent_frames, error_rate)

        # 5. Receiver processes incoming frames and generates ACK
        receiver, ack = receiver_process_frames(receiver, received_frames)

        # 6. Channel simulation (ACK back to sender)
        ack_result = simulate_channel([ack], error_rate)

        if ack_result:
            ack_received = ack_result[0]
        else:
            ack_received = None

        # 7. Sender processes ACK if not corrupted
        sender_receive_ack(sender, ack_received, t)

        # 8. Print current time step status
        print_timestep(t, sent_frames, ack_received, sender["LFS"], receiver["last_frame_received"], receiver["largest_acceptable_frame"], receiver["buffer"])

if __name__ == "__main__":
    main()