# SimpleTodoApp

## Overview
A lightweight, client‑side Todo application built with vanilla **HTML**, **CSS**, and **JavaScript**. The app lets users add, toggle, and delete tasks, persisting the list in the browser’s **Local Storage** so the data survives page reloads.

---

## Tech Stack
- **HTML5** – Structure of the UI.
- **CSS3** – Styling and responsive layout.
- **JavaScript (ES6)** – Application logic, DOM manipulation, and Local Storage handling.

---

## Features
- Add new todo items.
- Mark items as completed / uncompleted.
- Delete individual items.
- Clear all completed tasks.
- Persist the todo list in **Local Storage** (no backend required).
- Responsive design works on desktop and mobile browsers.

---

## Setup & Usage
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/simple-todo-app.git
   cd simple-todo-app
   ```
2. **Open `index.html` in a browser** – no build step or server is required.
   ```bash
   # macOS / Linux
   open index.html
   # Windows
   start index.html
   ```
   The application will load and you can start managing your todos immediately.

---

## Project Structure
```
/simple-todo-app
│
├─ index.html      # Markup for the Todo UI (input, list, controls)
├─ style.css       # Styling – layout, colors, responsive tweaks
└─ script.js       # Core JavaScript – DOM handling, state management, Local Storage
```
- **`index.html`** – Contains the main container, an input field for new tasks, an unordered list where todo items are rendered, and a footer with the “Clear completed” button.
- **`style.css`** – Provides a clean, minimal look using Flexbox/Grid, defines styles for completed items (strikethrough), and includes media queries for mobile friendliness.
- **`script.js`** – Implements the Todo app logic:
  - Maintains an array of todo objects `{ id, text, completed }`.
  - Renders the list into the DOM.
  - Handles adding, toggling, and deleting items.
  - Saves and loads the todo array from **Local Storage**.

---

## Local Storage Mechanism
The app stores the entire todo list under the key **`simpleTodoApp.todos`** in `window.localStorage`.

### Data Shape
```json
[
  {
    "id": "1687264839123",   // unique string (timestamp based)
    "text": "Buy groceries",
    "completed": false
  },
  {
    "id": "1687264850045",
    "text": "Walk the dog",
    "completed": true
  }
]
```
- On every change (add, toggle, delete, clear completed) the array is stringified with `JSON.stringify` and saved.
- On page load, `script.js` reads the value, parses it with `JSON.parse`, and populates the UI.

---

## Contribution Guide
We welcome contributions! Follow these steps:
1. **Fork** the repository.
2. **Clone** your fork locally.
   ```bash
   git clone https://github.com/your-username/simple-todo-app.git
   cd simple-todo-app
   ```
3. Create a new **branch** for your feature or bug‑fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes, ensuring existing functionality remains intact.
5. **Commit** with a clear message.
   ```bash
   git commit -m "feat: add dark‑mode toggle"
   ```
6. **Push** to your fork and open a **Pull Request** against the `main` branch of the original repository.
7. Wait for review, address any feedback, and once approved the PR will be merged.

---

## License
[Insert License Here] – e.g., MIT License.
