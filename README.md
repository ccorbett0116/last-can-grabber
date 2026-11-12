# The Last Can — Part 3: The Hunt (robotic task) — 10 marks

> *Eyes and a cockpit keep the rover moving. Only a can keeps it alive. Go and
> get one, and bring it home.*

This is the part where everything meets: the GUI drives, the model sees, and
the arm finally does something. You write the **grab** and **drop** routines
and your group performs the full run for your TA.

The assignment as a whole (mission, rules, setup, attendance, full rubric) is
in the [main repository](https://github.com/ccorbett0116/last-can). Do its
"Getting started" section first. Paths like `docs/robot_guide.md` on this page
are in that repository.

---

## The run

| Step | What happens | Who does it |
|---|---|---|
| 1 | The robot starts on the floor at the start point. The can is **out of the camera's view** | TA sets up |
| 2 | Drive until the can is found. The model must detect it **in frame, with the robot moving or stationary** | Driver, through your GUI |
| 3 | Press **Grab**. The robot runs its grabbing sequence and ends up holding the can | The robot |
| 4 | Drive back to the start point with the can | Driver, through your GUI |
| 5 | Press **Drop**. The robot runs its drop procedure | The robot |

**The drop counts if** the can ends up close to the start point and is
released **horizontally**: lying on its side, not standing up. The exact spot
doesn't matter.

Everything is done through your own GUI.

---

## How it's marked

One full run, marked live.

| Criterion | Marks | Full marks when |
|---|---|---|
| Finds the can | 2 | The driver reaches the can using the GUI, and the model detects it in frame, both while the robot is moving and once it has stopped |
| Grabs the can | 4 | A press of Grab starts the sequence, the sequence finishes by itself, and the robot ends up holding the can securely |
| Brings it home | 1 | The robot is driven back to the start point with the can still in the gripper |
| Drops the can | 2 | A press of Drop starts the procedure; the can is released close to the start point and **horizontally** |
| Reliability and control | 1 | The run works without restarts or rescues, the arm and wheels move in a controlled way, and nothing is knocked over or strained |
| **Total** | **10** | |

**Grabs the can (4 marks)** has part marks:

| Marks | What it looks like |
|---|---|
| 4 | The can is picked up cleanly and held securely |
| 3 | Picked up, but the grip is poor (the can slips or tilts badly), or it took a second attempt |
| 2 | The sequence runs and touches or moves the can but doesn't end up holding it |
| 1 | A grab sequence runs from the button but doesn't reach the can |
| 0 | No grab sequence |

**Drops the can (2 marks):** 1 mark for a controlled release close to the
start point, 1 mark for the can being released horizontally.

---

## Lining up with the detection box

After Grab is pressed, the robot lines *itself* up with the can using the
model's detection box, then grabs. The driver's job ends once the can is in
frame. From there the robot turns until the can is where it needs to be,
creeps forward until it's in reach, and then runs the arm sequence.

How you turn the box into movement is up to you. Questions to answer:

- **Where is "lined up"?** Which spot in the frame puts the can in front of
  the gripper? It may not be the centre of the image if the camera is mounted
  off to one side or tilted.
- **How do you know it's in reach?** The box gets bigger and lower in the
  frame as the robot gets closer. Which of those do you trust, and at what
  value do you stop?
- **How close is close enough?** Without some tolerance, the robot overshoots
  and hunts back and forth forever.
- **What if the box disappears?** The can can drop out of frame or the model
  can miss it for a few frames. Stop, wait, give up?

A simple approach that works nine times out of ten beats a clever one that
works twice. Reliability is in the rubric.

---

## The starter

[arm_pose_example.py](arm_pose_example.py) shows the two building blocks:
sending the arm one pose, and playing a list of poses with waits in between.
Run it from the `last-can` folder:

```bash
python last-can-grabber/arm_pose_example.py                       # wiggles the arm's base
python last-can-grabber/arm_pose_example.py --servo 1 --pos 500   # moves one servo
```

It only moves servo 1 (the base) by a small amount, so it's safe to run with
the arm in any position. **Clear the space around the arm first anyway.**

---

## Things to think about

**Learn the arm before you script it.** How many servos are there, and what
are their IDs? Which way does each one move as the number goes up? Where are
the limits beyond which it hits the chassis, the floor or itself? Move one
servo at a time, slowly (a long `duration`), until you know.
`docs/robot_guide.md` has the safety rules, and a section on finding and
learning the servos.

**Finding poses.** Servo commands are absolute positions, not "a bit more".
The servo sliders in your group's GUI are the natural tool for finding a pose
by hand and reading off the numbers, which is one reason to get them working
early. Until then, the `--servo` option above does the same job, slowly.

**Where is the camera?** Look at where it's mounted. If it moves when the arm
moves, then the arm's pose changes what the model sees, and a pose that is
good for driving may not be good for finding cans.

**Start from a known pose.** Because positions are absolute, a sequence that
begins by going to a known "home" pose behaves the same no matter where the
arm was left.

**Repeatability.** A scripted grab only works if the can is in the same place
relative to the robot every time. That's the alignment's job. How much error
can your grab tolerate, and are your thresholds tight enough to stay inside
it?

**Grip.** How far must the gripper close to hold a can without crushing it,
and without the servo straining? A servo that is pushing against something it
can't move gets hot and can be damaged. Don't leave it squeezing.

**Carrying.** The can has to survive the drive home. Where should the arm
hold it while the robot moves, turns and stops?

**Dropping horizontally.** The can is picked up one way and has to be let go
another. Which joint changes its orientation, and from how high can you
release it before it bounces or rolls away from the start point?

**Driving during a grab.** What should happen to the wheels while the arm is
working? What should happen if someone presses a drive key halfway through?

**Stopping.** Things will go wrong mid-sequence. How does the operator stop
the arm, and what state is it left in?

**Blocking.** The example waits with `time.sleep()`. Inside a tkinter GUI,
that freezes the window, the camera and the Stop button for the whole grab.
Your GUI builder and you need to solve this together.

**The picture is late.** The image reaches the lab PC a fraction of a second
after it was taken, sometimes more. An alignment that steers while it watches
is steering by the past. Small moves, then a pause to look again, are slower
but much easier to get right.

---

## Working with the other two parts

- The **GUI** calls your routines from its Grab and Drop buttons. Agree on
  that interface in the first session, then give your GUI builder a stand-in
  version on day one (one that just prints "grabbing…" and waits three
  seconds is enough) so neither of you is waiting for the other.
- The **model** tells you whether, and where, a can is in view. Your
  alignment runs on the box position, so ask your vision trainer early what a
  detection looks like in code, and how steady the box is from frame to frame.

See `docs/putting_it_together.md`.

---

## Using your robot time

This part needs the robot more than the other two, and the robot is shared.

| Doesn't need the robot | Needs the robot |
|---|---|
| The structure of the sequence code: steps, waits, a way to stop | Finding and tuning every pose |
| The interface with the GUI, tested with a stand-in that prints each pose | Every real grab and drop |
| The plan: which poses, in which order | How long each move really takes |
| Watching back a phone video of a failed attempt | Full runs |

Film your attempts. A grab takes ten seconds and fails in a tenth of one, and
watching it back costs no robot time. Arrive at each session with a short
list of what to try, in order.

---

## Practise the run

Do complete runs, start to finish, before the demo, with the person who will
drive on the day at the controls. Time them. The first full run always finds
a problem that none of the three parts had on its own.
