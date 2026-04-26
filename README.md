# Gesture Surfers - Hand-Controlled Endless Runner

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Subway Surfers-style endless runner game controlled entirely by hand gestures using MediaPipe and OpenCV. This project combines computer vision with game development to create an immersive, touchless gaming experience.

## 🚀 Features

- **Real-time Gesture Control**:
  - ✊ **Fist (0 Fingers)**: Slide under high obstacles.
  - ☝️ **1 Finger**: Move to Lane 1 (Left).
  - ✌️ **2 Fingers**: Move to Lane 2 (Center).
  - 🤟 **3 Fingers**: Move to Lane 3 (Right).
  - 🖐️ **4+ Fingers**: Jump over low obstacles.
- **Adaptive Difficulty**: Game speed increases dynamically as your score grows.
- **Neon Aesthetics**: Futuristic dark theme with glowing obstacles and fluid animations.
- **Multithreaded Architecture**: Vision processing runs on a separate thread to ensure a lag-free gaming experience.
- **Docker Support**: Ready for containerized deployment and testing.

## 🛠 Tech Stack

- **Core**: [Python](https://www.python.org/)
- **Game Engine**: [Pygame](https://www.pygame.org/)
- **Computer Vision**: [OpenCV](https://opencv.org/), [MediaPipe](https://mediapipe.dev/)
- **Numerical Processing**: [NumPy](https://numpy.org/)
- **Containerization**: [Docker](https://www.docker.com/)

## 📦 Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KanishkaGole/Gesture-Surfers-Hand-Controlled-Endless-Runner.git
   cd Gesture-Surfers-Hand-Controlled-Endless-Runner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

### Docker Setup

1. **Build the image**:
   ```bash
   docker build -t gesture-surfers .
   ```

2. **Run the container** (Requires X11 forwarding for GUI):
   ```bash
   docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix gesture-surfers
   ```

## 🎮 Usage

- **Webcam**: Ensure your webcam is enabled and your hand is clearly visible.
- **Gestures**: Use the gestures described in the [Features](#-features) section to control the player.
- **Keyboard Shortcuts**:
  - `R`: Restart the game after Game Over.
  - `Esc`: Exit the game.

## 📂 Folder Structure

```text
Gesture-Surfers-Hand-Controlled-Endless-Runner/
├── assets/          # Game sprites, sounds, and fonts
├── game/            # Core game logic (engine, player, obstacles)
├── utils/           # Constants and helper functions
├── vision/          # Hand tracking and gesture recognition logic
├── main.py          # Entry point of the application
├── requirements.txt # Python dependencies
├── Dockerfile       # Container configuration
└── README.md        # Project documentation
```

## 👥 Contributors

This project was developed as a collaborative team effort:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/KanishkaGole">
        <img src="https://github.com/KanishkaGole.png" width="100px;" alt="Kanishka Gole"/>
        <br />
        <sub><b>Kanishka Gole</b></sub>
      </a>
      <br />
      <a href="https://github.com/KanishkaGole/AI-Gym-Trainer/commits?author=KanishkaGole" title="Code">💻</a>
    </td>
    <td align="center">
      <a href="https://github.com/Aarya-dixit">
        <img src="https://github.com/Aarya-dixit.png" width="100px;" alt="Arya Dixit"/>
        <br />
        <sub><b>Arya Dixit</b></sub>
      </a>
      <br />
      <a href="https://github.com/KanishkaGole/AI-Gym-Trainer/commits?author=Aarya-dixit" title="Code">💻</a>
    </td>
  </tr>
</table>

- **Kanishka Gole** - [GitHub Profile](https://github.com/KanishkaGole)
- **Aarya Dixit** - [GitHub Profile](https://github.com/Aarya-dixit)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
