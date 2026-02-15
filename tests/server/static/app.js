const textarea = document.getElementById('scriptInput');

// Simple default script for testing
const defaultScript = `document.body.style.backgroundColor = "#fef3c7";`;

// Load saved script from localStorage or fallback to default
textarea.value = localStorage.getItem('savedScript') || defaultScript;

// Reuse a single script element to avoid DOM clutter
let scriptElement = null;

function runScript() {
  const code = textarea.value;
  localStorage.setItem('savedScript', code);

  // Remove existing script if it exists
  if (scriptElement) {
    scriptElement.remove();
  }

  // Create and append new script
  scriptElement = document.createElement('script');
  scriptElement.textContent = `
    try {
      ${code}
    } catch (e) {
      console.error("Script execution error:", e);
    }
  `;
  document.body.appendChild(scriptElement);

  // Send log to server
  fetch('/log', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: `Script updated: ${code.substring(0, 50)}...` }),
  }).catch(err => console.error("Failed to send log:", err));
}

function clearScript() {
  localStorage.removeItem('savedScript');
  textarea.value = defaultScript;
  console.log("Saved script cleared. Reset to simple default.");
  runScript(); // run the simple script immediately
}

// Debounce helper to avoid executing on every keystroke
function debounce(func, timeout = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args);
    }, timeout);
  };
}

const debouncedRun = debounce(() => runScript());

// Auto-live execution with debounce
textarea.addEventListener('input', debouncedRun);

// Run once on page load
runScript();
