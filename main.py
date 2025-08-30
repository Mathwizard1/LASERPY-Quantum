from LaserPy.Components import Clock

clock = Clock(dt=0.1, name="my_clock")
clock.set(t_final=1.0)

while(clock.running):
    print(f"Current time: {clock.t}")
    clock.update()