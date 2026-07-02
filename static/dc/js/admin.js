function renderAdminPanel(user) {
  document.getElementById('adminSideName').textContent = user.name + ' ' + user.last;
  document.getElementById('adminWelcomeName').textContent = user.name + ' ' + user.last;
  document.getElementById('adminProfName').textContent = user.name + ' ' + user.last;
  document.getElementById('adminProfEmail').textContent = user.email;
  document.getElementById('adminLastAccess').textContent = new Date().toLocaleDateString('es-MX', {weekday:'long',hour:'2-digit',minute:'2-digit'});

  updateAdminStats();
  renderAdminUsers();
  renderAdminGroups();
  renderAdminSponsors();
  renderAdminPayments();
}

function switchAdminTab(tabId, btn) {
  document.querySelectorAll('.sidebar__nav a').forEach(a => a.classList.remove('sidebar__link--active'));
  if (btn) btn.classList.add('sidebar__link--active');
  document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('admin-tab--active'));
  const target = document.getElementById(tabId);
  if (target) target.classList.add('admin-tab--active');
}

function updateAdminStats() {
  const students = APP.state.users.filter(u => u.role === 'student').length;
  const teachers = APP.state.users.filter(u => u.role === 'teacher').length;
  document.getElementById('statStudents').textContent = students;
  document.getElementById('statTeachers').textContent = teachers;
  document.getElementById('statGroups').textContent = '8';
  document.getElementById('statSponsorsValue').textContent = APP.state.sponsors.length;
}

function renderAdminUsers() {
  const tb = document.getElementById('adminUsersBody');
  if (!tb) return;
  tb.innerHTML = APP.state.users.map(u =>
    `<tr>
      <td><strong>${u.name} ${u.last}</strong></td>
      <td>${u.email}</td>
      <td><span class="badge badge--${u.role==='admin'?'warning':u.role==='teacher'?'info':'primary'}">${u.role}</span></td>
      <td>${u.district||'N/A'}</td>
      <td><span class="badge badge--${u.status==='activo'?'success':'danger'}">${u.status}</span></td>
      <td>
        <button class="btn btn--sm btn--ghost" onclick="alert('Editar: ${u.name}')"><i class="fas fa-edit"></i></button>
        <button class="btn btn--sm btn--ghost" onclick="toggleUserStatus(${u.id})"><i class="fas fa-${u.status==='activo'?'ban':'check-circle'}"></i></button>
      </td>
    </tr>`
  ).join('');
}

function toggleUserStatus(id) {
  const u = APP.state.users.find(x => x.id === id);
  if (!u) return;
  u.status = u.status === 'activo' ? 'inactivo' : 'activo';
  APP.saveState();
  renderAdminUsers();
}

function addUser() {
  const name = prompt('Nombre del usuario:');
  if (!name) return;
  APP.state.users.push({ id: APP.state.users.length+1, user:'user'+Date.now(), pass:'demo123', name, last:'', email: name.toLowerCase().replace(/\s/g,'')+'@dc.com', role:'student', district:'Distrito Educativo 01', level:'A1 - Basico', status:'activo' });
  APP.saveState();
  renderAdminUsers();
  updateAdminStats();
}

function renderAdminGroups() {
  const tb = document.getElementById('adminGroupsBody');
  if (!tb) return;
  const groups = [
    { name:'Grupo A1-01', district:'Distrito 1', level:'A1 - Basico', teacher:'John Smith', students:8, status:'activo' },
    { name:'Grupo A2-01', district:'Distrito 2', level:'A2 - Intermedio', teacher:'John Smith', students:7, status:'activo' },
    { name:'Grupo B1-01', district:'Distrito 3', level:'B1 - Avanzado', teacher:'Laura Martinez', students:6, status:'activo' },
    { name:'Grupo A1-02', district:'Distrito 4', level:'A1 - Basico', teacher:'Laura Martinez', students:8, status:'activo' },
    { name:'Grupo TOEFL-01', district:'Distrito 1', level:'TOEFL', teacher:'John Smith', students:5, status:'activo' },
    { name:'Grupo B1-02', district:'Distrito 2', level:'B1 - Avanzado', teacher:'Laura Martinez', students:6, status:'inactivo' },
    { name:'Grupo A2-02', district:'Distrito 3', level:'A2 - Intermedio', teacher:'John Smith', students:7, status:'activo' },
    { name:'Grupo CONV-01', district:'Distrito 4', level:'Conversacion', teacher:'Laura Martinez', students:4, status:'activo' },
  ];
  tb.innerHTML = groups.map(g =>
    `<tr>
      <td><strong>${g.name}</strong></td>
      <td>${g.district}</td>
      <td>${g.level}</td>
      <td>${g.teacher}</td>
      <td>${g.students}</td>
      <td><span class="badge badge--${g.status==='activo'?'success':'danger'}">${g.status}</span></td>
    </tr>`
  ).join('');
}

function renderAdminSponsors() {
  const tb = document.getElementById('adminSponsorsBody');
  if (!tb) return;
  tb.innerHTML = APP.state.sponsors.map(s =>
    `<tr>
      <td><strong>${s.name}</strong></td>
      <td>${s.role}</td>
      <td><em>"${s.slogan}"</em></td>
      <td>
        <button class="btn btn--sm btn--ghost" onclick="editSponsor(${s.id})"><i class="fas fa-edit"></i></button>
        <button class="btn btn--sm btn--ghost" onclick="deleteSponsor(${s.id})"><i class="fas fa-trash" style="color:var(--danger)"></i></button>
      </td>
    </tr>`
  ).join('');
}

function addSponsor() {
  const name = prompt('Nombre del patrocinador:');
  if (!name) return;
  APP.state.sponsors.push({ id: APP.state.sponsors.length+1, name, role: prompt('Cargo:')||'Patrocinador', slogan: prompt('Lema:')||'Educacion de calidad', color:'#2962ff', bg:'#e8f0fe' });
  APP.saveState();
  renderAdminSponsors();
  APP.renderSponsors();
  updateAdminStats();
}

function editSponsor(id) {
  const s = APP.state.sponsors.find(x => x.id === id);
  if (!s) return;
  const n = prompt('Nombre:', s.name);
  if (n) s.name = n;
  const sl = prompt('Lema:', s.slogan);
  if (sl) s.slogan = sl;
  APP.saveState();
  renderAdminSponsors();
  APP.renderSponsors();
}

function deleteSponsor(id) {
  if (!confirm('Eliminar patrocinador?')) return;
  APP.state.sponsors = APP.state.sponsors.filter(s => s.id !== id);
  APP.saveState();
  renderAdminSponsors();
  APP.renderSponsors();
  updateAdminStats();
}

function renderAdminPayments() {
  const tb = document.getElementById('adminPaymentsBody');
  if (!tb) return;
  const payments = [
    { student:'Maria Garcia', concept:'Curso A2 - Mensualidad', amount:'$2,450', date:'15 jun 2026', method:'Tarjeta', status:'completado' },
    { student:'Carlos Ramirez', concept:'Curso B1 - Inscripcion', amount:'$4,900', date:'12 jun 2026', method:'Transferencia', status:'completado' },
    { student:'Laura Hernandez', concept:'Curso A1 - Mensualidad', amount:'$2,450', date:'10 jun 2026', method:'Efectivo', status:'completado' },
    { student:'Pedro Martinez', concept:'Curso A2 - Mensualidad', amount:'$2,450', date:'8 jun 2026', method:'Tarjeta', status:'pendiente' },
    { student:'Sofia Torres', concept:'Curso TOEFL - Completo', amount:'$12,000', date:'5 jun 2026', method:'Transferencia', status:'completado' },
  ];
  tb.innerHTML = payments.map(p =>
    `<tr>
      <td><strong>${p.student}</strong></td>
      <td>${p.concept}</td>
      <td><strong>${p.amount}</strong></td>
      <td>${p.date}</td>
      <td>${p.method}</td>
      <td><span class="badge badge--${p.status==='completado'?'success':'warning'}">${p.status}</span></td>
    </tr>`
  ).join('');
}
