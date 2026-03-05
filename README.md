# OpenMouf

Open source robot control and visualization library for the Mouf robot.

## Project Structure

```
openmouf/
├── mouf/                    # Main Python library
│   ├── __init__.py         # Core mouf module
│   ├── driver/             # Device drivers (servos, PCA9685, etc.)
│   │   ├── __init__.py
│   │   ├── PCA9685.py      # 16-channel PWM controller driver
│   │   ├── Servo.py        # Servo motor driver
│   │   ├── ServoMT.py      # Multi-threaded servo driver
│   │   ├── ServoMTO.py     # Optimized multi-threaded servo driver
│   │   └── calibrate.py    # Calibration utilities
│   └── engine/             # Control engine and visualization
│       ├── __init__.py
│       ├── emotion.py      # Emotion state management
│       ├── viz.py          # Visualization utilities
│       ├── _viz.py         # Internal visualization helpers
│       └── emotion_viz.py  # Emotion visualization
│
├── moufctl/                 # Control utility CLI
│   └── __init__.py
│
├── skeleton/               # Robot physical design (OpenSCAD + STL)
│   ├── *.scad             # OpenSCAD 3D models
│   └── stl/               # 3D printable STL files
│
├── pyproject.toml         # Python project configuration
├── requirements.txt       # Core Python dependencies
├── requirements-viz.txt   # Visualization dependencies
└── install.txt            # System dependencies (apt)
```

### Key Components

- **mouf**: Core robot control library with driver abstractions
- **moufctl**: Control utility that re-exports mouf modules
- **skeleton**: OpenSCAD and STL files for the Mouf robot skeleton

## Installation

### System Dependencies

```bash
sudo apt-get install python3-smbus
sudo apt-get install p7zip-full
```

### Python Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Core Package

```bash
pip install -e .
```

### Install with Visualization Support

```bash
pip install -e ".[viz]"
```

## Usage

### Basic Import

```python
import mouf
from mouf import driver, engine
```

### Using moufctl

```python
import moufctl
from moufctl import driver, engine

# Access driver modules
from mouf.driver import Servo, PCA9685

# Access engine modules
from mouf.engine import emotion, viz
```

### Example: Servo Control

```python
from mouf.driver import Servo, PCA9685

# Initialize PWM controller
pwm = PCA9685(address=0x40)
pwm.set_pwm_freq(50)

# Create and control servo
servo = Servo(pwm, channel=0)
servo.set_angle(90)
```

## Development

### Running Tests

```bash
pytest tests/
```

### Building

The project uses setuptools for packaging. Edit `pyproject.toml` to modify package configuration.

## License

MIT
