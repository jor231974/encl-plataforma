async function handleLogin(e, role) {
  e.preventDefault();
  let userField, passField, alertEl;
  if (role === 'student') {
    userField = document.getElementById('loginUser').value.trim();
    passField = document.getElementById('loginPass').value.trim();
    alertEl = document.getElementById('loginAlert');
  } else {
    userField = document.getElementById('loginUserAdmin').value.trim();
    passField = document.getElementById('loginPassAdmin').value.trim();
    alertEl = document.getElementById('loginAlertAdmin');
  }

  alertEl.className = 'alert';
  if (!userField || !passField) {
    alertEl.textContent = 'Completa todos los campos.';
    alertEl.className = 'alert alert--visible alert--error';
    return;
  }

  try {
    const data = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username: userField, password: passField })
    });
    const user = data.user;
    try { localStorage.setItem('dc_session', JSON.stringify({ user: user.username, role: user.role, id: user.id })); } catch(e) {}
    APP.state.currentUser = user;
    APP.updateNav(user);

    if (user.role === 'admin') {
      renderAdminPanel(user);
      navigate('admin');
    } else {
      renderStudentPanel(user);
      navigate('student');
    }
  } catch (err) {
    const user = APP.state.users.find(u => u.user === userField && u.pass === passField);
    if (!user) {
      alertEl.textContent = 'Usuario o contrasena incorrectos.';
      alertEl.className = 'alert alert--visible alert--error';
      return;
    }
    try { localStorage.setItem('dc_session', JSON.stringify({ user: user.user, role: user.role })); } catch(e) {}
    APP.state.currentUser = user;
    APP.updateNav(user);
    if (user.role === 'admin') { renderAdminPanel(user); navigate('admin'); }
    else { renderStudentPanel(user); navigate('student'); }
  }
}
