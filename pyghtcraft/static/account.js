let editorMode = 0;

const enum_closed = 0;
const enum_password = 1;
const enum_email = 2;
const enum_name = 3;

const message_element = document.getElementById('js_hint_messages');
const message_element_sidebar = document.getElementById('sidebarmessage');

const api_url = "/minecraft/api/user";

function displayError(errormsg) {
    message_element.className = 'error';
    message_element.innerText = errormsg;
    message_element.style.display = 'block';
}
function displaySuccess(successmsg) {
    message_element.className = '';
    message_element.innerText = '';
    message_element.style.display = 'none';
    message_element_sidebar.innerText = successmsg;
    message_element_sidebar.style.display = 'block';
}

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

    const data = {
        username: current_username,
        password: current_password,
        new_password: new_password,
        api_key: api_key,
        action: 'changepassword'
    };

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            displaySuccess(result.message || 'Password changed successfully!');
            closeEditor();
        } else {
            displayError(result.message || result.error || 'Error changing password');
        }
    } catch (error) {
        displayError('Network error occurred.');
    }
    message_element.style = "display: box;"
}


async function changeEmail(current_username, current_password, new_email) {

    const data = {
        username: current_username,
        password: current_password,
        new_email: new_email,
        api_key: api_key,
        action: 'changeemail'
    };

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            displaySuccess(result.message || 'E-Mail changed successfully!');
            closeEditor();
        } else {
            displayError(result.message || result.error || 'Error changing e-mail address');
        }
    } catch (error) {
        displayError('Network error occurred.');
    }
    message_element.style = "display: box;"
}


async function changeUsername(current_username, current_password, new_username) {

    const data = {
        username: current_username,
        password: current_password,
        new_username: new_username,
        api_key: api_key,
        action: 'changeusername'
    };

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            displaySuccess(result.message || 'Username changed successfully!');
            closeEditor();
        } else {
            displayError(result.message || result.error || 'Error changing username');
        }
    } catch (error) {
        displayError('Network error occurred.');
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
    
    // Check name and password
    if (!(username === current_username)) {
        displayError("Wrong username!");
    } else {

        switch (editorMode) {
            case enum_password:
                if (!(new_password === new_password2)) {
                    displayError("New password did not match confirmation. Please type again.");
                } else {
                    changePassword(current_username, current_password, new_password);
                }
                break;
                
            case enum_email:
                if (!(new_email === new_email2)) {
                    displayError("New e-mail did not match confirmation. Please type again.");
                } else {
                    changeEmail(current_username, current_password, new_email);
                }
                break;

            case enum_name:
                if (!(new_name === new_name2)) {
                    displayError("New username did not match confirmation. Please type again.");
                } else {
                    changeUsername(current_username, current_password, new_email);
                }
                break;

            default:
                console.log('Unkown editor mode: ' + editorMode);
                break;
            }
        }
    }