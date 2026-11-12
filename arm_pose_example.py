#!/usr/bin/env python3
"""
COSC 3P71 - Final Lab, Part 3: arm example.

Shows the two things every grab or drop routine is built from:

    1. move_servos()  - send one arm pose (any number of servos at once)
    2. play()         - step through a list of poses, waiting between them

The example sequence only wiggles the arm's base a little, so it is safe to
run with the arm in any position. A real grab sequence is the same idea with
more servos and more steps - or something else entirely, if you have a better
plan. Nothing here is required; it is a starting point.

    python arm_pose_example.py                       # play the wiggle
    python arm_pose_example.py --servo 1 --pos 500   # move one servo and exit
    python arm_pose_example.py --servo 1 --pos 500 --time 2.0

Before you run it: clear the space around the arm and keep your hands out.

Requires:  pip install websocket-client
"""
import argparse
import json
import sys
import time

try:
    import websocket                    # from the websocket-client package
except ImportError:
    sys.exit("websocket-client is not installed. Run:  pip install websocket-client")

# Check these against your robot (see docs/robot_guide.md).
ROBOT_IP       = "192.168.149.1"
ROSBRIDGE_PORT = 9090
SERVO_TOPIC    = "/ros_robot_controller/bus_servo/set_position"
SERVO_TYPE     = "ros_robot_controller_msgs/msg/ServosPosition"

SERVO_MIN, SERVO_MAX = 0, 1000          # bus servo positions; 500 is roughly the middle

# A sequence is DATA, not code: a list of steps. Each step moves some servos
# ({servo id: position}), gives them `duration` seconds to get there, then
# waits `pause` more seconds before the next step.
EXAMPLE_SEQUENCE = [
    {"positions": {1: 500}, "duration": 1.0, "pause": 0.3},
    {"positions": {1: 440}, "duration": 0.8, "pause": 0.3},
    {"positions": {1: 560}, "duration": 0.8, "pause": 0.3},
    {"positions": {1: 500}, "duration": 0.8, "pause": 0.0},
]


def connect():
    try:
        ws = websocket.create_connection(f"ws://{ROBOT_IP}:{ROSBRIDGE_PORT}", timeout=5)
    except Exception as exc:
        sys.exit(f"Could not connect to rosbridge at {ROBOT_IP}:{ROSBRIDGE_PORT}: {exc}")
    ws.send(json.dumps({"op": "advertise", "topic": SERVO_TOPIC, "type": SERVO_TYPE}))
    time.sleep(0.5)                     # give the robot a moment to set the topic up
    return ws


def move_servos(ws, positions, duration=1.0):
    """Send one pose. positions = {servo id: position 0..1000}. Servos that are
    not mentioned stay where they are. Returns immediately: the arm is still
    moving for `duration` seconds after this function comes back."""
    ws.send(json.dumps({"op": "publish", "topic": SERVO_TOPIC, "msg": {
        "duration": float(duration),
        "position": [{"id": int(sid), "position": max(SERVO_MIN, min(SERVO_MAX, int(pos)))}
                     for sid, pos in positions.items()],
    }}))


def play(ws, sequence):
    for number, step in enumerate(sequence, start=1):
        print(f"step {number}/{len(sequence)}: {step['positions']}")
        move_servos(ws, step["positions"], step["duration"])
        time.sleep(step["duration"] + step.get("pause", 0.0))


# TODO: your grab and drop routines. Some questions worth settling first:
#   - Where does the can have to be, relative to the robot, when the grab starts?
#     How does the driver (or the robot) know it is there?
#   - What happens to driving while the arm is moving?
#   - How do you stop the arm if something goes wrong halfway?
#   - This file blocks with time.sleep(). What would that do inside a GUI?


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--servo", type=int, help="move just this servo id ...")
    ap.add_argument("--pos", type=int, help="... to this position (0-1000)")
    ap.add_argument("--time", type=float, default=1.0, help="seconds for the move (default 1.0)")
    args = ap.parse_args()

    ws = connect()
    try:
        if args.servo is not None and args.pos is not None:
            move_servos(ws, {args.servo: args.pos}, args.time)
            time.sleep(args.time)
        else:
            play(ws, EXAMPLE_SEQUENCE)
    finally:
        ws.close()


if __name__ == "__main__":
    main()
