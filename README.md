# LaserPy_Quantum

**LaserPy_Quantum** provides an intuitive interface for simulating complex laser interactions, current drivers, and interferometer setups, with plans to offload performance-critical components to Rust for high-speed numerical computations. A *high-level, open-source Python library designed for the theoretical simulation of laser systems* in quantum communication and cryptographic protocols.

### 🚀 Features

- High-Level API for constructing laser-based quantum system simulations.
- Support for arbitrary waveform generation (AWG) and current drivers.
- Simulation of master–slave laser - configurations with injection locking.
- Built-in support for asymmetric Mach–Zehnder interferometers (AMZI) and photon detectors.
- Clock-driven simulation engine for precise time-step control.
- Extensible architecture for future modules and Rust acceleration.

### 📦 Installation

Currently, LaserPy_Quantum is under active development and not yet on PyPI.
- Clone the repository locally:

```bash
git clone https://github.com/Mathwizard1/LaserPy_Quantum.git
cd LaserPy_Quantum
pip install -e .
```

Ensure you’re using Python 3.9+.

### 📝 Example Usage

Below is an example of using LaserPy_Quantum component and connection system with simulator:

```python
from LaserPy_Quantum import Clock, PhysicalComponent
from LaserPy_Quantum import Connection, Simulator

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

### 🧠 Use Case: Laser simulations

LaserPy_Quantum’s current use case is simulating quantum key distribution (QKD) protocols using master–slave lasers with injection locking and interferometer-based detection.<br>
It allows researchers and engineers to prototype and test theoretical setups before implementing them in hardware.

### 🔧 Planned Features

- Rust-based backend for high-performance simulation.
- Expanded library of optical components (modulators, detectors, etc.).

#### TODO list
1) Rust based critical parts off-loading
2) Component behaviour refinement
3) Optical Regulator Components (VOA, Opt Circulator / Isolator)
4) More components
> - TODO multiport interferometer
> - TODO SPD photon count and clicked
> - TODO PhaseSensitive SPD

### 🤝 Contributing

We welcome contributions!<br>
Feel free to fork the repo, open issues, or submit pull requests.

### 📜 License

LaserPy_Quantum is distributed under a dual-license model to support both the open-source community and commercial applications.

-   **Open Source:** For academic, personal, and open-source projects, LaserPy_Quantum is licensed under the **GNU General Public License v3.0 (GPLv3)**.

-   **Commercial:** For use in proprietary or commercial software where the terms of *GPLv3 are not suitable*, a separate commercial license is available. Please contact the maintainer to discuss licensing options.

### 📬 Contact

Maintained by Anshurup Gupta.<br>
For questions or collaborations, open an issue or [email](mailto:anshurup.gupta@gmail.com).