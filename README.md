# LaserPy

A high-level Python library designed for the theoretical simulation of laser systems in quantum communication and cryptographic protocols.
LaserPy provides an intuitive interface for simulating complex laser interactions, current drivers, and interferometer setups, with plans to offload performance-critical components to Rust for high-speed numerical computations.

### 🚀 Features

- High-Level API for constructing laser-based quantum system simulations.
- Support for arbitrary waveform generation (AWG) and current drivers.
- Simulation of master–slave laser - configurations with injection locking.
- Built-in support for asymmetric Mach–Zehnder interferometers (AMZI) and photon detectors.
- Clock-driven simulation engine for precise time-step control.
- Extensible architecture for future modules and Rust acceleration.

### 📦 Installation

Currently, LaserPy is under active development and not yet on PyPI.
- Clone the repository locally:

```
git clone https://github.com/Mathwizard1/LaserPy.git
cd LaserPy
pip install -e .
```

Ensure you’re using Python 3.9+.

### 📝 Example Usage

Below is an example of using LaserPy component and connection system with simulator:

```
from LaserPy import Clock, PhysicalComponent
from LaserPy import Connection, Simulator

simulator_clock = Clock(dt=0.001)
simulator_clock.set(2)

simulator = Simulator(simulator_clock)

physical_device1 = PhysicalComponent(save_simulation= True)
physical_device2 = PhysicalComponent(save_simulation= True)

simulator.set((
    Connection(simulator_clock, physical_device1),
    Connection(physical_device1, physical_device2)
))

simulator.simulate()
time_data = simulator.get_data()

physical_device1.display_data(time_data)
physical_device2.display_data(time_data)
```

### 🧠 Use Case: Quantum Protocol Simulation

LaserPy’s current use case is simulating quantum key distribution (QKD) protocols using master–slave lasers with injection locking and interferometer-based detection.
It allows researchers and engineers to prototype and test theoretical setups before implementing them in hardware.

### 🔧 Planned Features

- Rust-based backend for high-performance simulation.
- Expanded library of optical components (modulators, detectors, etc.).

### 🤝 Contributing

We welcome contributions!
Feel free to fork the repo, open issues, or submit pull requests.

### 📜 License

This project is currently copyrighted. ©2025

### 📬 Contact

Maintained by Anshurup Gupta.\
For questions or collaborations, open an issue or [email](mailto:anshurup.gupta@gmail.com).