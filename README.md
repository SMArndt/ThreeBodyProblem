# ThreeBodyProblem
# 🌌 3D Three-Body Problem Simulation

This project simulates and visualises the motion of three gravitationally interacting bodies in 3D using Newtonian mechanics. The animation helps explore complex, often chaotic trajectories that arise from simple initial conditions.

## 🎥 Example Output

![Three-Body Simulation Screenshot](ThreeBodyProblem_Frame.png)
![Three-Body Simulation](ThreeBodyProblem.mp4)

> The above video shows bodies orbiting in 3D, with colored trails and wall projections to help visualise their motion.

---

## 🧠 Features

- Newtonian gravity-based simulation of 3 bodies
- Time integration using the Euler method
- The simulation is visualised in an animated 3D plot with rotating view
- Colour-coded trajectories with wall projections

---

## ⚙️ Requirements

Install required Python packages:

```bash
pip install numpy matplotlib
```

---

## 🚀 Run the Simulation

```bash
python ThreeBody_Walls.py
```

If `ffmpeg` is available, it will export as an `.mp4`; otherwise it falls back to `.gif`.

---

## ✏️ Customization

To adjust the simulation:

- Change `masses`, `positions`, and `velocities` in the script
- Modify `colors` and background styling
- Tune simulation duration via `steps` and `dt`
- Adjust wall projection transparency or camera spin speed

---

## 📂 Files

- `ThreeBodyProblem.py`: Fully commented source code of the simulation
- `ThreeBody_3Dspin.mp4`: Example output animation
- `requirements.txt`: Python dependencies

---

## 📜 License
GNU General Public License 3.0

---

## 🙌 Acknowledgments
Originally developed by Stephan/ChatGPT. Mostly ChatGPT.
