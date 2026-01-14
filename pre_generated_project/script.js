// script.js
// Core Calculator module
// Exposes a Calculator class globally (window.Calculator)

class Calculator {
  constructor() {
    // Initialize values as strings
    this.currentValue = '';
    this.previousValue = '';
    this.operator = null; // '+', '-', '*', '/' or null
    this._updateDisplay('0');
  }

  // Private helper to update the display element (#display)
  _updateDisplay(value) {
    const display = document.querySelector('#display');
    if (!display) return;
    // If the element is an input/textarea, set its value; otherwise set textContent
    if ('value' in display) {
      display.value = value;
    } else {
      display.textContent = value;
    }
  }

  // Append a digit (or decimal point) to the current value
  appendDigit(digit) {
    if (typeof digit !== 'string' && typeof digit !== 'number') return;
    const d = String(digit);
    // Prevent multiple leading zeros (except when decimal point follows)
    if (this.currentValue === '0' && d !== '.') {
      this.currentValue = d;
    } else {
      // Prevent multiple decimal points
      if (d === '.' && this.currentValue.includes('.')) {
        return; // ignore extra decimal
      }
      this.currentValue += d;
    }
    this._updateDisplay(this.currentValue || '0');
  }

  // Set the operator for the next calculation
  setOperator(op) {
    if (!['+', '-', '*', '/'].includes(op)) return;
    // If there is already a pending operation, calculate first
    if (this.operator && this.previousValue && this.currentValue) {
      this.calculate();
    }
    this.operator = op;
    // Move current value to previous and reset current for new entry
    if (this.currentValue !== '') {
      this.previousValue = this.currentValue;
    }
    this.currentValue = '';
    // Optionally show operator or keep current display; we'll keep current display unchanged
  }

  // Perform the calculation based on stored operator and values
  calculate() {
    if (!this.operator || this.previousValue === '' || this.currentValue === '') {
      return;
    }
    const a = parseFloat(this.previousValue);
    const b = parseFloat(this.currentValue);
    let result;
    switch (this.operator) {
      case '+':
        result = a + b;
        break;
      case '-':
        result = a - b;
        break;
      case '*':
        result = a * b;
        break;
      case '/':
        result = b === 0 ? 'Error' : a / b;
        break;
      default:
        return;
    }
    this.currentValue = typeof result === 'number' ? String(result) : result;
    this._updateDisplay(this.currentValue);
    // Reset operator and previous value after calculation
    this.operator = null;
    this.previousValue = '';
  }

  // Clear the current entry (CE)
  clearEntry() {
    this.currentValue = '';
    this._updateDisplay('0');
  }

  // Reset the entire calculator (C)
  reset() {
    this.currentValue = '';
    this.previousValue = '';
    this.operator = null;
    this._updateDisplay('0');
  }
}

// Expose globally for other scripts / tests
if (typeof window !== 'undefined') {
  window.Calculator = Calculator;
}

// ------------------------------------------------------------
// Todo List Core Logic
// ------------------------------------------------------------

// DOM elements for the todo list
const taskForm = document.getElementById('task-form');
const newTaskInput = document.getElementById('new-task');
const taskList = document.getElementById('task-list');

// In‑memory task collection
let tasks = [];

/** Load tasks from localStorage. If none exist, initialize with an empty array. */
function loadTasksFromStorage() {
  const stored = localStorage.getItem('todoTasks');
  try {
    tasks = stored ? JSON.parse(stored) : [];
    // Ensure we have an array of objects with required fields
    if (!Array.isArray(tasks)) tasks = [];
  } catch (e) {
    console.error('Failed to parse stored tasks:', e);
    tasks = [];
  }
}

/** Persist the current tasks array to localStorage. */
function saveTasksToStorage() {
  try {
    localStorage.setItem('todoTasks', JSON.stringify(tasks));
  } catch (e) {
    console.error('Failed to save tasks:', e);
  }
}

/** Render the task list UI based on the current `tasks` array. */
function renderTasks() {
  if (!taskList) return;
  taskList.innerHTML = '';

  tasks.forEach((task) => {
    const li = document.createElement('li');
    li.className = 'task-item';
    li.dataset.id = task.id;

    const span = document.createElement('span');
    span.textContent = task.text;
    if (task.completed) {
      span.classList.add('completed');
    }
    li.appendChild(span);

    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toggle-btn';
    toggleBtn.textContent = task.completed ? 'Undo' : 'Done';
    li.appendChild(toggleBtn);

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.textContent = 'Delete';
    li.appendChild(deleteBtn);

    taskList.appendChild(li);
  });
}

/** Add a new task to the list, persist it, and re‑render. */
function addTask(text) {
  const task = {
    id: Date.now().toString(),
    text,
    completed: false,
  };
  tasks.push(task);
  saveTasksToStorage();
  renderTasks();
}

/** Delete a task by its id, persist changes, and re‑render. */
function deleteTask(id) {
  // Ensure id is a string for comparison
  tasks = tasks.filter((task) => task.id !== String(id));
  saveTasksToStorage();
  renderTasks();
}

/** Toggle the completed state of a task by its id, persist, and re‑render. */
function toggleTaskCompletion(id) {
  const taskId = String(id);
  const task = tasks.find((t) => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
    saveTasksToStorage();
    renderTasks();
  }
}

/** Initialize the application: set up event listeners and load initial state. */
function init() {
  // Instantiate the calculator
  const calc = new Calculator();

  // ------------------------------------------------------------
  // Calculator button handling
  // ------------------------------------------------------------
  function handleButtonClick(event) {
    const btn = event.currentTarget;
    const key = btn.getAttribute('data-key');
    if (!key) return;

    // Digits and decimal point
    if (/^[0-9]$/.test(key) || key === '.') {
      calc.appendDigit(key);
      return;
    }

    // Operators
    if (['+', '-', '*', '/'].includes(key)) {
      calc.setOperator(key);
      return;
    }

    // Equals
    if (key === '=') {
      calc.calculate();
      return;
    }

    // Clear entry
    if (key === 'CE') {
      calc.clearEntry();
      return;
    }

    // Reset / Clear all
    if (key === 'C') {
      calc.reset();
      return;
    }
  }

  const buttons = document.querySelectorAll('.btn');
  buttons.forEach((button) => {
    button.addEventListener('click', handleButtonClick);
  });

  // ------------------------------------------------------------
  // Keyboard support for calculator
  // ------------------------------------------------------------
  window.addEventListener('keydown', (e) => {
    const { key } = e;

    // Digits (0-9) and decimal point
    if (/^[0-9]$/.test(key) || key === '.') {
      e.preventDefault();
      calc.appendDigit(key);
      return;
    }

    // Operators
    if (['+', '-', '*', '/'].includes(key)) {
      e.preventDefault();
      calc.setOperator(key);
      return;
    }

    // Equals / Enter
    if (key === '=' || key === 'Enter') {
      e.preventDefault();
      calc.calculate();
      return;
    }

    // Clear entry (Backspace)
    if (key === 'Backspace') {
      e.preventDefault();
      calc.clearEntry();
      return;
    }

    // Reset / Clear all (Escape)
    if (key === 'Escape') {
      e.preventDefault();
      calc.reset();
      return;
    }
  });

  // ------------------------------------------------------------
  // Todo List event handling
  // ------------------------------------------------------------
  if (taskForm && newTaskInput) {
    taskForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = newTaskInput.value.trim();
      if (text) {
        addTask(text);
        newTaskInput.value = '';
      }
    });
  }

  if (taskList) {
    taskList.addEventListener('click', (e) => {
      const li = e.target.closest('li.task-item');
      if (!li) return;
      const id = li.dataset.id;
      if (e.target.classList.contains('delete-btn')) {
        deleteTask(id);
      } else if (e.target.classList.contains('toggle-btn')) {
        toggleTaskCompletion(id);
      }
    });
  }

  // Load persisted tasks and render UI
  loadTasksFromStorage();
  renderTasks();
}

// Export functions for testing / external use (if module system available)
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = {
    addTask,
    deleteTask,
    toggleTaskCompletion,
    loadTasksFromStorage,
    saveTasksToStorage,
  };
} else if (typeof window !== 'undefined') {
  window.addTask = addTask;
  window.deleteTask = deleteTask;
  window.toggleTaskCompletion = toggleTaskCompletion;
  window.loadTasksFromStorage = loadTasksFromStorage;
  window.saveTasksToStorage = saveTasksToStorage;
}

// Bootstrap the application
init();
