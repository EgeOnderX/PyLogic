# PyLogic V1.1.0

PyLogic is a comprehensive, cross-platform interactive digital logic gate simulator built with Python and Pygame. It provides hardware enthusiasts, students etc. with an intuitive playground to construct, test, and analyze logical circuits in real time. 

---

## Project Rebranding Notice

The project has transitioned its official name from **LogicPy** to **PyLogic**.

---

## New Features

* **Enhanced Sidebar Inventory:** Optimised the component selection panel for a smoother user interface layout.
* **Integrated Menu Bar:** Added a comprehensive top menu bar structure providing quick access to essential application features.
* **Dynamic Theme Swapping:** Introduced live toggle capabilities between fully customized Light and Dark modes.
* **Persistent Configuration Engine:** Implemented automated `config.cfg` serialization to preserve localized user environments across launches.
* **Quad-Language Localization:** Added full operational translations for English, Turkish, German, and French.
* **Immersive Fullscreen Mode:** Deployed a hardware-accelerated scaling display module to support seamless fullscreen toggling without viewport distortion.

## Bug Fixes & Stability Adjustments

* **Wiring System Overhaul:** Resolved logic routing failures, erratic drawing behaviors, and trace errors within multi-segment connection wires.
* **Cascaded Component Pipeline:** Corrected visual rendering artifacts and collision issues triggered when placing multiple AND gates in close proximity.
* **Universal Node Shifting:** Fixed a coordinate drift issue where internal connection points and logical slots failed to translate alongside dragged Switches and LEDs.
* **Null Pointer Prevention:** Eliminated fatal exceptions caused by dangling, incomplete, or `None`-returning wire endpoints.
* **Gate Evaluation Core Updates:** Fixed calculation inaccuracies and general runtime bugs inside the primary logic gate simulation loop.
---

## Key Features

### 1. High-Fidelity Logic Simulation Engine
* **Component Diversity:** Features a robust array of standard logical components including basic gates (AND, OR, NOT), universal gates (NAND, NOR), and advanced gates (XOR, XNOR), alongside interactive input elements (Switches) and visual output modules (LEDs).
* **Real-Time Signal Propagation:** Implements a dynamic logic calculation loop that sequentially evaluates input states, executes gate logic, and updates wire values seamlessly at 60 frames per second.
* **Advanced Wiring System:** Supports intricate wiring mechanics, allowing users to trace real-time signal previews and inject multi-segment bend points onto the canvas for clean engineering schematic layouts.

### 2. Modern UI/UX and Theme Adaptation
* **Dual Palette Infrastructure:** Equipped with native Light Mode and Dark Mode configurations. The interfaces switch color spaces dynamically, adjusting backgrounds, text surfaces, bounding boxes, and accents to reduce eye strain.
* **Engineering Grid Overlay:** Renders a non-intrusive geometric grid background aligned with the viewport to assist users with precise component placement and linear alignment.
* **Layered Rendering Pipeline:** Orchestrates assets into four isolated rendering layers to guarantee that high-priority user interface panels (such as toolbars and dropdowns) always hover legibly above the underlying simulation canvas.

### 3. Native Internationalization
* Provides full multi-language localization directly within the source architecture. The entire environment can instantly adapt its layout prose to:
  * English (EN)
  * Turkish (TR)
  * German (DE)
  * French (FR)

### 4. Configuration Persistence
* **State Management:** Automatically saves user environmental variables (selected language, screen mode, active theme) into a local `config.cfg` file upon termination, parsing it on initialization to preserve user preferences.
* **Circuit Serialization:** Supports complete structural JSON serialization. Complex schematic structures—including logic states, canvas coordinates, discrete slot indices, component types, and colored wire vectors—can be dumped to or pulled from local files (`circuit.json`) instantly.

### 5. Resolution Independence & Robust Interaction
* **Aspect Scalability:** Utilizes hardware-accelerated scaling flags (`pygame.SCALED`), preventing layout deformation, pixel stretching, or coordinate drift when shifting between resizable windowed formats and full-screen displays.
* **Universal Delta Shifting:** Integrates an error-correcting delta coordinate modifier. When dragging components across the canvas, internal bounding boxes (`pygame.Rect`) and logical contact slots are recalculated programmatically relative to physical mouse deltas, preventing component misalignment bugs.

---

## User Interface

### Mouse Inputs
* **Left Click (Canvas Sidebar):** Selects a logical gate or component from the tool inventory to prepare for canvas placement.
* **Left Click (Active Canvas):** Places the selected element, toggles interactive Switches between high (1) and low (0) impedance states, or initiates/completes wire links from defined slot nodes.
* **Left Click + Drag:** Engages the universal delta shifter to move placed components safely across the environment without breaking coordinate bounds.
* **Right Click:** Deletes targeted components from the simulator canvas. It automatically traces connected paths and clears dead-ended wire vectors from memory.

### Keyboard Shortcuts
* **S Key:** Silently executes the JSON serialization routines to back up the current layout to `circuit.json`.
* **L Key:** Deserializes and reloads the active layout from `circuit.json` onto the workspace grid.

## Video

https://github.com/user-attachments/assets/2f15a8b0-10d2-43d3-b5b1-cf860569f21a

---

⭐ **Support the Project**
If you like this project and find it useful, please consider giving it a star! It means a lot and helps the project grow!

