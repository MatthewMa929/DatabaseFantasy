document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();

    
    const role = document.getElementById('role').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!role || !username || !password) {
        alert('Please fill in all fields!');
        return;
    }

    if (role === 'admin') {
        window.location.href = 'admin_dashboard.html';
    } else if (role === 'user') {
        window.location.href = 'user_dashboard.html';   
    }
});

