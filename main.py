# CSE 3231 - Homework 1
# Sliding Window Algorithm Simulation
# Group Name: BAYRAK_ILDEM
# Student 1: Elif Dila Bayrak, ID
# Student 2: Zeynep Neva Ildem, 904034285

import sys

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
    pass

def generate_frame_sequence(sws):
    """
    Generate sequence number space based on window size.
    Typically:
    - sequence numbers wrap around
    - size is usually related to window size (e.g., sws + 1 or power of 2)
    Return a list or range of valid frame IDs.
    """
    pass

def sender_send_frames(sender, sws, current_time):
    """
    Decide which frames the sender transmits at this time step.
    Should:
    - check available space in sender window
    - send new frames if possible
    - update LFS (Last Frame Sent)
    - start timers for new frames
    Return:
    - list of frames sent in this time step
    """
    pass

def simulate_channel(frames, error_rate):
    """
    Simulate transmission over the channel.
    Should:
    - randomly decide if each frame is corrputed based on error_rate
    - mark corrputed frames (e.g., with '?'
    Return:
    - list of recieved frames (with corruption if applicable)
    """
    pass

def receiver_process_frames(reciever, frames):
    """
    Process incoming frames at the receiver.
    Should:
    - accept frames within receiver window
    - discard frame outside window
    - buffer out-of-order frames
    - update lat frame received in order
    - generate ACKs
    Return:
    - updates receiver state
    - ACK(s) to send back
    """
    pass

def sender_receive_ack(sender, ack, current_time):
    """
    Process ACK at sender.
    Should:
    - remove acknowledged frames from window
    - update sender state
    - reset timers as needed
    """
    pass

def check_timeouts(sender, timeout, current_time):
    """
    Check for frames that timed out.
    Should:
    - identify frames whose timers exceeded timeout
    - mark them for retransmission
    Return:
    - list of frames to retransmit
    """
    pass

def print_header(duration, sws, rws, error_rate, timeout, sequence):
    """
    Print simulation header.
    Should include:
    - student names/IDs
    - group name
    - parameters
    - sequence number space
    """
    pass

def print_timestep(t, sent_frame, ack_received, lfs, last_frame_received, largest_acceptable_frame, receiver_buffer):
    """
    Print one row of the simulation table.
    Columns should match assignment format:
    - time step
    - frame sent
    - ACK reseived
    - LFS
    - last frame recived
    - largest acceptable frame
    - receiver buffer contents
    """
    pass

def main():
    duration, sws, rws, error_rate, timeout = parse_arguments()

    sender = initialize_sender(sws)
    receiver = initialize_receiver(rws)

    sequence = generate_frame_sequence(sws)

    print_header(duration, sws, rws, error_rate, timeout, sequence)

    for t in range(duration):
        # 1. Sender sends frames
        sent_frames = sender_send_frames(sender, sws, t)

        # 2. Channel simulates transmission
        received_frames = simulate_channel(sent_frames, error_rate)

        # 3. Receiver processes incoming frames and generates ACK
        receiver, ack = receiver_process_frames(receiver, received_frames)

        # 4. Channel simulation (ACK back to sender)
        ack_received = simulate_channel([ack], error_rate)

        # 5. Sender processes ACK
        if ack_received:
            sender_receive_ack(sender, ack_received[0], t)

        # 6. Check for timeouts and mark frames for retransmission
        retransmissions = check_timeouts(sender, timeout, t)

        # 7. Print current time step status
        print_timestep(t, sent_frames, ack_received, sender.get("LFS", None), receiver.get("last_frame_received", None), receiver.get("largest_acceptable_frame", None), receiver.get("buffer", []))

if __name__ == "__main__":
    main()