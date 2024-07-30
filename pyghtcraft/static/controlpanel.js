// script.js

let consoleOpen = false;

// Function to disable or enable buttons
function disableButtons(isdisabled) {
    document.getElementById('startBtn').disabled = isdisabled;
    document.getElementById('stopBtn').disabled = isdisabled;
    document.getElementById('infoBtn').disabled = isdisabled;
}

// Function to send an action to the server
function sendAction(action) {
    disableButtons(true); // Disable buttons

    // Get username and API key from Flask session
    const username = "{{ session['username'] }}";
    const api_key = "{{ session['api_key'] }}";
    
    document.getElementById('response').innerText = 'Waiting for server status...';
    fetch('/minecraft/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, api_key: api_key, action: action })
    })
    .then(response => response.json())
    .then(data => {
        // Display status if available
        if (data.status) {
            document.getElementById('response').innerText = data.status;
        } else {
            document.getElementById('response').innerText = 'Error: No permission.';
        }
    })
    .catch(error => {
        document.getElementById('response').innerText = 'Request failed: ' + error;
    })
    .finally(() => {
        disableButtons(false); // Enable buttons
    });
}

// Function to toggle the console window
function toggleConsole() {
    consoleOpen = !consoleOpen;
    const consoleContainer = document.getElementById('consoleContainer');
    const consoleWindow = document.getElementById('consoleWindow');
    const consoleToolbar = document.getElementById('consoletoolbar');
    const openConsoleBtn = document.getElementById('openConsoleBtn');
    const widthbox = document.getElementById('widthbox1');
    const sidebar = document.getElementById('serverSidebar');
    if (consoleOpen) {
        consoleContainer.style.display = 'block';
        consoleWindow.style.display = 'block';
        openConsoleBtn.innerText = 'Close Console';
        sidebar.style.width = '250px';
        if (window.innerWidth < 768) {
            consoleToolbar.style.display = 'flex';
            sidebar.style.display = 'none'; 
            widthbox.style.flexDirection = 'column';
        } else {
            consoleToolbar.style.display = 'none';
            sidebar.style.display = 'block';
            widthbox.style.flexDirection = 'row';
        }
        fetchConsoleOutput(); // Start fetching console output
    } else {
        consoleContainer.style.display = 'none';
        consoleWindow.style.display = 'none'; 
        openConsoleBtn.innerText = 'Open Console';
        sidebar.style.width = '320px';
        if (window.innerWidth < 768) {
            consoleToolbar.style.display = 'none';
            sidebar.style.display = 'block'; 
            widthbox.style.flexDirection = 'column';
        } else {
            consoleToolbar.style.display = 'none';
            sidebar.style.display = 'block';
            widthbox.style.flexDirection = 'row';
        }
    }
}

// Function to fetch console output
function fetchConsoleOutput() {
    if (!consoleOpen) return; // Stop fetching if console is closed

    const username = "{{ session['username'] }}";
    const api_key = "{{ session['api_key'] }}";

    fetch('/minecraft/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, api_key: api_key, action: 'getconsole' })
    })
    .then(response => {
        if (response.status === 204) {
            // No new data
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            const consoleContainer = document.getElementById('consoleContainer');
            const newConsoleOutput = data.console_output.join('\n');
            
            if (newConsoleOutput !== lastConsoleOutput) {
                lastConsoleOutput = newConsoleOutput;
                consoleContainer.innerText = newConsoleOutput;
                consoleContainer.scrollTop = consoleContainer.scrollHeight; // Scroll to bottom
            }
        }
    })
    .catch(error => {
        console.error('Failed to fetch console output:', error);
    })
    .finally(() => {
        // Fetch new console output every second
        setTimeout(fetchConsoleOutput, 1000);
    });
}

// Function to handle console input
function handleConsoleInput(event) {
    if (event.key === 'Enter') {
        sendConsoleCommand();
    }
}

// Function to send a console command
function sendConsoleCommand() {
    const consoleInput = document.getElementById('consoleInput');
    const command = consoleInput.value.trim();
    if (command === '') return;

    const username = "{{ session['username'] }}";
    const api_key = "{{ session['api_key'] }}";

    fetch('/controlpanel/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, api_key: api_key, action: 'command', command: command })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            consoleInput.value = '';
            fetchConsoleOutput(); // Fetch latest console output after sending command
        } else {
            console.error('Failed to send command:', data.error);
        }
    })
    .catch(error => {
        console.error('Failed to send command:', error);
    });
}

// Automatically fetch server status when loading the page
window.onload = function() {
    sendAction('status'); 
};
