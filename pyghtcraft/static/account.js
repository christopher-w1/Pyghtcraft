let editorMode = 0;

const enum_closed = 0;
const enum_password = 1;
const enum_email = 2;
const enum_name = 3;

const message_element = document.getElementById('js_hint_messages');

const api_url = "";

function openEditorPassword() {
    const sidebar = document.getElementById('accountsidebar');
    const accounteditor = document.getElementById('accounteditor');
    const passwordform = document.getElementById('changepasswordform');
    const emailform = document.getElementById('changemailform');
    const nameform = document.getElementById('changenameform');

    if (window.innerWidth < 768) {
        sidebar.style.display       = 'none';
    } else if (window.innerWidth < 1100) {
        sidebar.style.width       = '240px';
    }
    emailform.style.display     = 'none';
    nameform.style.display      = 'none';
    passwordform.style.display  = 'block';
    accounteditor.style.display = 'block';

    editorMode = enum_password;
}

function openEditorEmail() {
    const sidebar = document.getElementById('accountsidebar');
    const accounteditor = document.getElementById('accounteditor');
    const passwordform = document.getElementById('changepasswordform');
    const emailform = document.getElementById('changemailform');
    const nameform = document.getElementById('changenameform');

    if (window.innerWidth < 768) {
        sidebar.style.display       = 'none';
    } else if (window.innerWidth < 1100) {
        sidebar.style.width       = '240px';
    }
    passwordform.style.display  = 'none';
    nameform.style.display      = 'none';
    emailform.style.display     = 'block';
    accounteditor.style.display = 'block';

    editorMode = enum_email;
}

function openEditorName() {
    const sidebar = document.getElementById('accountsidebar');
    const accounteditor = document.getElementById('accounteditor');
    const passwordform = document.getElementById('changepasswordform');
    const emailform = document.getElementById('changemailform');
    const nameform = document.getElementById('changenameform');

    if (window.innerWidth < 768) {
        sidebar.style.display       = 'none';
    } else if (window.innerWidth < 1200) {
        sidebar.style.width       = '240px';
    }
    passwordform.style.display  = 'none';
    emailform.style.display     = 'none';
    nameform.style.display      = 'block';
    accounteditor.style.display = 'block';

    editorMode = enum_name;
}

function closeEditor() {
    const sidebar = document.getElementById('accountsidebar');
    const accounteditor = document.getElementById('accounteditor');
    const passwordform = document.getElementById('changepasswordform');
    const emailform = document.getElementById('changemailform');
    const nameform = document.getElementById('changenameform');

    passwordform.style.display  = 'none';
    emailform.style.display     = 'none';
    nameform.style.display      = 'none';
    accounteditor.style.display = 'none';
    sidebar.style.display       = 'block';
    sidebar.style.width         = '320px';

    editorMode = enum_closed;
}

async function changePassword(current_username, current_password, new_password) {
    const url = '/api/user';

    const data = {
        username: current_username,
        password: current_password,
        new_password: new_password,
        api_key: api_key,
        action: 'changepassword'
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            message_element.textContent = result.message || 'Password changed successfully!';
            message_element.className = 'success'; // Setzt die CSS-Klasse für Erfolg
        } else {
            message_element.textContent = result.error || 'Error changing password';
            message_element.className = 'error'; // Setzt die CSS-Klasse für Fehler
        }
    } catch (error) {
        message_element.textContent = 'Network error occurred.';
        message_element.className = 'error'; // Setzt die CSS-Klasse für Fehler
    }
    message_element.style = "display: box;"
}

function submitEditorData() {
    const new_password = document.getElementById('new_password').value.trim();
    const new_password2 = document.getElementById('new_password2').value.trim();

    const new_email = document.getElementById('new_email').value.trim();
    const new_email2 = document.getElementById('new_email2').value.trim();

    const new_name = document.getElementById('new_name').value.trim();
    const new_name2 = document.getElementById('new_name2').value.trim();

    const current_username = document.getElementById('current_username').value.trim();
    const current_password = document.getElementById('current_password').value.trim();

    message_element.innerText = "";

    switch (editorMode) {
        case enum_password:
            if (!(new_password === new_password2)) {
                message_element.innerText = "Password didn't match confirmation. Please type again.";
            } else if (new_password.length === 0) {
                message_element.innerText = "Please enter a new Password.";
            } else {
                changePassword(current_username, current_password, new_password);
            }

        default:
            console.log('Unkown editor mode: ' + editorMode);
            break;
    }
}