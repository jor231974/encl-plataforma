let API_USERS_CACHE = null;

const APP = {
  state: { users: [], sponsors: [], messages: [], courses: [], categories: [] },
  async init() {
    this.loadState();
    this.seedData();
    await this.loadAPIData();
    this.renderSponsors();
    this.renderMaterials();
    this.renderMessages();
    this.renderParticipants();
    this.checkSession();
    this.initNav();
  },
  async loadAPIData() {
    try {
      const home = await apiFetch('/public/home');
      if (home.sponsors) this.state.sponsors = home.sponsors.map(s => ({
        id: s.id, name: s.name, role: s.slogan || '', slogan: s.message || '',
        color: '#2962ff', bg: '#e8f0fe', logo: s.logo, photo: s.photo
      }));
      if (home.categories) this.state.categories = home.categories;
      if (home.featured_courses) this.state.courses = home.featured_courses;
      try { localStorage.setItem('dc_state', JSON.stringify({ users: this.state.users, sponsors: this.state.sponsors })); } catch(e) {}
    } catch(e) {
      console.log('API no disponible, usando datos locales');
    }
  },
  loadState() {
    try { const s = localStorage.getItem('dc_state'); if (s) Object.assign(this.state, JSON.parse(s)); } catch(e) {}
  },
  saveState() {
    try { localStorage.setItem('dc_state', JSON.stringify({ users: this.state.users, sponsors: this.state.sponsors })); } catch(e) {}
  },
  seedData() {
    if (!this.state.users.length) {
      this.state.users = [
        { id:1, user:'admin01', pass:'admin123', name:'Admin', last:'Principal', email:'admin@dc.com', role:'admin', district:'Nacional', status:'activo' },
        { id:2, user:'alumno01', pass:'demo123', name:'Maria', last:'Garcia Lopez', email:'maria@example.com', role:'student', district:'Distrito Educativo 02', level:'A2 - Intermedio', status:'activo' },
        { id:3, user:'alumno02', pass:'demo123', name:'Carlos', last:'Ramirez', email:'carlos@example.com', role:'student', district:'Distrito Educativo 01', level:'B1 - Avanzado', status:'activo' },
        { id:4, user:'alumno03', pass:'demo123', name:'Laura', last:'Hernandez', email:'laura@example.com', role:'student', district:'Distrito Educativo 03', level:'A1 - Basico', status:'activo' },
        { id:5, user:'alumno04', pass:'demo123', name:'Pedro', last:'Martinez', email:'pedro@example.com', role:'student', district:'Distrito Educativo 02', level:'A2 - Intermedio', status:'inactivo' },
        { id:6, user:'teacher01', pass:'demo123', name:'John', last:'Smith', email:'john@dc.com', role:'teacher', district:'Nacional', level:'Profesor', status:'activo' },
        { id:7, user:'teacher02', pass:'demo123', name:'Laura', last:'Martinez', email:'laura.m@dc.com', role:'teacher', district:'EdoMex', level:'Profesor', status:'activo' },
      ];
      this.saveState();
    }
    if (!this.state.sponsors.length) {
      this.state.sponsors = [
        { id:1, name:'Carlos Mendoza', role:'Director General - TechGlobal', slogan:'Comprometidos con la educacion.', color:'#2962ff', bg:'#e8f0fe' },
        { id:2, name:'Ana Torres', role:'CEO - EduFuture', slogan:'La capacitacion transforma vidas.', color:'#00c853', bg:'#e8f5e9' },
        { id:3, name:'Roberto Sanchez', role:'Presidente - ProEnglish', slogan:'Invertir en educacion es invertir en el futuro.', color:'#ff6d00', bg:'#fff3e0' },
        { id:4, name:'Patricia Lopez', role:'Directora de RH - SmartLearn', slogan:'Porque nunca es tarde para aprender.', color:'#7b1fa2', bg:'#f3e5f5' },
      ];
      this.saveState();
    }
  },
  getStudentById(id) {
    return this.state.users.find(u => u.id === id) || this.state.users[1];
  },
  renderSponsors() {
    const g = document.getElementById('sponsorsGrid');
    if (!g) return;
    g.innerHTML = this.state.sponsors.map(s =>
      `<div class="sponsor-card">
        <div class="sponsor-card__photo" style="background:${s.color}">${s.name.charAt(0)}${s.name.split(' ')[1]?.charAt(0)||''}</div>
        <div class="sponsor-card__name">${s.name}</div>
        <div class="sponsor-card__role">${s.role}</div>
        <div class="sponsor-card__slogan">"${s.slogan}"</div>
      </div>`
    ).join('');
  },
  renderMaterials() {
    const list = document.getElementById('materialsList');
    if (!list) return;
    const items = [
      { name:'Guia de Estudio - Module 3', type:'PDF', size:'2.4 MB', icon:'fa-file-pdf', color:'#d32f2f', bg:'#ffebee' },
      { name:'Vocabulario Semanal - Week 12', type:'PDF', size:'1.1 MB', icon:'fa-file-pdf', color:'#d32f2f', bg:'#ffebee' },
      { name:'Ejercicios de Gramatica', type:'PDF', size:'856 KB', icon:'fa-file-pdf', color:'#d32f2f', bg:'#ffebee' },
      { name:'Audio: Pronunciacion', type:'MP3', size:'5.2 MB', icon:'fa-file-audio', color:'#2e7d32', bg:'#e8f5e9' },
      { name:'Video: Conversacion Cotidiana', type:'MP4', size:'15.8 MB', icon:'fa-file-video', color:'#7b1fa2', bg:'#f3e5f5' },
    ];
    list.innerHTML = items.map(m =>
      `<div class="download-item" style="display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid var(--border)">
        <div style="width:40px;height:40px;border-radius:10px;background:${m.bg};color:${m.color};display:flex;align-items:center;justify-content:center;flex-shrink:0"><i class="fas ${m.icon}"></i></div>
        <div style="flex:1"><div style="font-weight:600;font-size:0.9rem">${m.name}</div><div style="font-size:0.8rem;color:var(--text-light)">${m.type} · ${m.size}</div></div>
        <button class="btn btn--sm btn--outline" onclick="alert('Descarga simulada: ${m.name}')"><i class="fas fa-download"></i></button>
      </div>`
    ).join('');
    const grid = document.getElementById('materialsGrid');
    if (!grid) return;
    grid.innerHTML = items.map(m =>
      `<div class="material-card">
        <div class="material-card__icon" style="background:${m.bg};color:${m.color}"><i class="fas ${m.icon}"></i></div>
        <div class="material-card__name">${m.name}</div>
        <div class="material-card__meta">${m.type} · ${m.size}</div>
        <button class="btn btn--sm btn--outline" onclick="alert('Descarga: ${m.name}')"><i class="fas fa-download"></i> Descargar</button>
      </div>`
    ).join('');
  },
  renderMessages() {
    const list = document.getElementById('messagesList');
    if (!list) return;
    const msgs = [
      { from:'Prof. John Smith', preview:'Great job on the last exercise! Keep practicing...', time:'10 min', avatar:'JS', color:'#2962ff', unread:true },
      { from:'Soporte DC', preview:'Tu certificado del curso A2 ya esta disponible...', time:'2 horas', avatar:'SD', color:'#00c853', unread:true },
      { from:'Coordinacion Academica', preview:'Recordatorio: Proximo examen el viernes...', time:'1 dia', avatar:'CA', color:'#ff6d00', unread:false },
      { from:'Maria (Companera)', preview:'Hi! Do you want to practice conversation this...', time:'2 dias', avatar:'M', color:'#7b1fa2', unread:false },
    ];
    list.innerHTML = msgs.map(m =>
      `<div class="message-item ${m.unread ? 'message-item--unread' : ''}">
        <div class="message-item__avatar" style="background:${m.color}">${m.avatar}</div>
        <div class="message-item__info"><div class="message-item__sender">${m.from}</div><div class="message-item__preview">${m.preview}</div></div>
        <div class="message-item__time">${m.time}</div>
      </div>`
    ).join('');
  },
  renderParticipants() {
    const list = document.getElementById('participantsList');
    if (!list) return;
    const users = [
      { name:'Maria Garcia', color:'#2962ff', role:'Alumno' },
      { name:'Carlos Ramirez', color:'#00c853', role:'Alumno' },
      { name:'Laura Hernandez', color:'#ff6d00', role:'Alumno' },
      { name:'Pedro Martinez', color:'#7b1fa2', role:'Alumno' },
      { name:'Sofia Torres', color:'#e91e63', role:'Alumno' },
      { name:'John Smith', color:'#ffd600', role:'Profesor' },
      { name:'Ana Castro', color:'#00bcd4', role:'Alumno' },
      { name:'Luis Vega', color:'#ff5722', role:'Alumno' },
    ];
    list.innerHTML = users.map(u =>
      `<div class="live-participant">
        <div class="live-participant__avatar" style="background:${u.color}">${u.name.charAt(0)}</div>
        <span>${u.name}</span>
        <span style="font-size:0.75rem;color:var(--text-light);margin-left:auto">${u.role === 'Profesor' ? '👑' : ''}</span>
      </div>`
    ).join('');
  },
  checkSession() {
    try {
      const s = localStorage.getItem('dc_session');
      if (s) {
        const sess = JSON.parse(s);
        const u = this.state.users.find(x => x.user === sess.user);
        if (u) { this.state.currentUser = u; this.updateNav(u); }
      }
    } catch(e) {}
  },
  updateNav(user) {
    const na = document.getElementById('navActions');
    const nu = document.getElementById('navUserMenu');
    const nn = document.getElementById('navUserName');
    const mn = document.getElementById('mNavActions');
    const mu = document.getElementById('mNavUser');
    const mn2 = document.getElementById('mNavUserName');
    if (user) {
      if (na) na.style.display = 'none';
      if (nu) { nu.style.display = 'flex'; nn.textContent = user.name + ' ' + user.last; }
      if (mn) mn.style.display = 'none';
      if (mu) { mu.style.display = 'block'; mn2.textContent = user.name + ' ' + user.last; }
    } else {
      if (na) na.style.display = '';
      if (nu) nu.style.display = 'none';
      if (mn) mn.style.display = '';
      if (mu) mu.style.display = 'none';
    }
  },
  initNav() {
    window.addEventListener('hashchange', () => {
      const p = window.location.hash.replace('#','') || 'home';
      const base = p.split('-')[0];
      if (['home','login','cursos'].includes(base) || base === 'curso') navigate(p);
    });
    if (window.location.hash) {
      const p = window.location.hash.replace('#','') || 'home';
      const base = p.split('-')[0];
      if (['home','login','cursos'].includes(base) || base === 'curso') setTimeout(() => navigate(p), 50);
    }
  },
  async renderCourseCatalog() {
    const grid = document.getElementById('coursesGrid');
    const filters = document.getElementById('categoryFilters');
    if (!grid) return;
    try {
      let courses = this.state.courses;
      if (!courses.length) {
        const res = await apiFetch('/courses');
        courses = res.courses || [];
        this.state.courses = courses;
      }
      if (filters) {
        const cats = this.state.categories || [];
        filters.innerHTML = `<button class="category-pill category-pill--active" data-cat="all" onclick="APP.filterCourses('all',this)">Todos</button>` +
          cats.map(c => `<button class="category-pill" data-cat="${c.id}" onclick="APP.filterCourses('${c.id}',this)">${c.name}</button>`).join('');
      }
      grid.innerHTML = courses.map(c => this.courseCardHTML(c)).join('');
    } catch(e) {
      grid.innerHTML = '<div class="empty-state"><i class="fas fa-book-open"></i><div class="empty-state__title">Cursos no disponibles</div><p>Intenta de nuevo mas tarde.</p></div>';
    }
  },
  filterCourses(catId, btn) {
    document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('category-pill--active'));
    if (btn) btn.classList.add('category-pill--active');
    const grid = document.getElementById('coursesGrid');
    if (!grid) return;
    const filtered = catId === 'all' ? this.state.courses : this.state.courses.filter(c => String(c.category_id) === String(catId));
    grid.innerHTML = filtered.length ? filtered.map(c => this.courseCardHTML(c)).join('') :
      '<div class="empty-state"><i class="fas fa-search"></i><div class="empty-state__title">Sin resultados</div><p>No hay cursos en esta categoria.</p></div>';
  },
  courseCardHTML(c) {
    const iconMap = { 1:'fa-language', 2:'fa-laptop-code', 3:'fa-briefcase', 4:'fa-building', 5:'fa-chart-line', 6:'fa-tools', 7:'fa-star' };
    const icon = iconMap[c.category_id] || 'fa-graduation-cap';
    return `<div class="course-card">
      <div class="course-card__image" style="background:linear-gradient(135deg,${c.category_id===1?'#132f4c,#2962ff':'#0a1628,#132f4c'})">
        <i class="fas ${icon} course-card__image-icon"></i>
        <span class="course-card__badge course-card__badge--${c.price>0?'premium':'gratis'}">${c.price>0 ? 'Premium' : 'Gratis'}</span>
      </div>
      <div class="course-card__body">
        <div class="course-card__title">${c.title}</div>
        <div class="course-card__summary">${c.summary || c.description?.substring(0,120) + '...' || ''}</div>
        <div class="course-card__meta">
          <span class="course-card__meta-item"><i class="fas fa-signal"></i> ${c.level || 'Todos'}</span>
          <span class="course-card__meta-item"><i class="far fa-clock"></i> ${c.duration || '—'}</span>
          <span class="course-card__meta-item"><i class="fas fa-file-video"></i> ${c.classes_count || 0} clases</span>
        </div>
        <div class="course-card__footer">
          <span class="course-card__level">${c.category_name || 'General'}</span>
          <button class="btn btn--primary btn--sm" onclick="navigate('curso-${c.id}')">Ver Curso</button>
        </div>
      </div>
    </div>`;
  },
  async renderCourseDetail(courseId) {
    document.getElementById('cursoLoading').style.display = 'block';
    document.getElementById('cursoContent').style.display = 'none';
    try {
      const course = await apiFetch(`/courses/${courseId}`);
      this.renderCursoHeader(course);
      this.renderCursoTabs(course);
      document.getElementById('cursoLoading').style.display = 'none';
      document.getElementById('cursoContent').style.display = 'block';
    } catch(e) {
      document.getElementById('cursoLoading').innerHTML = '<i class="fas fa-exclamation-triangle" style="font-size:2rem;color:var(--accent)"></i><p style="margin-top:16px">No se pudo cargar el curso.</p><button class="btn btn--primary mt-3" onclick="navigate(\'cursos\')">Volver a Cursos</button>';
    }
  },
  renderCursoHeader(c) {
    const header = document.getElementById('cursoHeader');
    const isEnrolled = (c.students_count || 0) > 0;
    header.innerHTML = `<div class="curso-header">
      <div class="curso-header__info">
        <div class="curso-header__category">${c.category_name || ''}</div>
        <h1 class="curso-header__title">${c.title}</h1>
        <p class="curso-header__summary">${c.description || c.summary || ''}</p>
        <div class="curso-header__details">
          <span class="curso-header__detail"><i class="fas fa-signal"></i> ${c.level || 'Todos los niveles'}</span>
          <span class="curso-header__detail"><i class="far fa-clock"></i> ${c.duration || '—'}</span>
          <span class="curso-header__detail"><i class="fas fa-file-video"></i> ${c.classes_count || 0} clases</span>
          <span class="curso-header__detail"><i class="fas fa-file-alt"></i> ${c.exams?.length || 0} examenes</span>
        </div>
        <div class="curso-header__instructor">
          <div class="curso-header__instructor-avatar">${(c.instructor_name || '?').charAt(0)}</div>
          <div class="curso-header__instructor-info">
            <div class="curso-header__instructor-name">${c.instructor_name || 'Instructor'}</div>
            <div class="curso-header__instructor-role">Instructor del curso</div>
          </div>
        </div>
      </div>
      <div class="curso-header__card">
        <div class="curso-header__price">${c.price > 0 ? '$' + c.price : 'Gratis'}</div>
        <div class="curso-header__price-label">${c.price > 0 ? 'Pago unico' : 'Acceso completo'}</div>
        <button class="btn btn--${c.price > 0 ? 'accent' : 'primary'} btn--lg btn--block" onclick="handleEnroll(${c.id})">
          <i class="fas ${isEnrolled ? 'fa-play-circle' : 'fa-user-plus'}"></i> ${isEnrolled ? 'Ir al Curso' : 'Inscribirme'}
        </button>
      </div>
    </div>`;
  },
  renderCursoTabs(course) {
    const nav = document.getElementById('cursoTabsNav');
    const content = document.getElementById('cursoTabsContent');
    const tabs = [
      { id:'clases', label:'Clases', icon:'fa-video' },
      { id:'examenes', label:'Examenes', icon:'fa-file-alt' },
      { id:'tareas', label:'Tareas', icon:'fa-tasks' },
    ];
    nav.innerHTML = tabs.map((t,i) =>
      `<button class="curso-tab-link ${i===0?'curso-tab-link--active':''}" onclick="switchCursoTab('${t.id}',this)"><i class="fas ${t.icon}"></i> ${t.label}</button>`
    ).join('');

    const classesHTML = (course.classes || []).map(cl =>
      `<div class="curso-class-item">
        <div class="curso-class-item__icon curso-class-item__icon--${cl.class_type === 'en_vivo' ? 'live' : 'recorded'}">
          <i class="fas ${cl.class_type === 'en_vivo' ? 'fa-video' : 'fa-play-circle'}"></i>
        </div>
        <div class="curso-class-item__body">
          <div class="curso-class-item__title">${cl.title}</div>
          <div class="curso-class-item__desc">${cl.description || ''}</div>
          <div class="curso-class-item__meta">
            <span><i class="far fa-clock"></i> ${cl.duration || '—'}</span>
            <span><i class="fas ${cl.class_type === 'en_vivo' ? 'fa-calendar-check' : 'fa-play-circle'}"></i> ${cl.class_type === 'en_vivo' ? (cl.date ? new Date(cl.date).toLocaleDateString('es-MX') : 'Proximamente') : 'Grabada'}</span>
          </div>
        </div>
        <div class="curso-class-item__action">
          ${cl.video_url ? `<a href="${cl.video_url}" target="_blank" class="btn btn--sm btn--primary"><i class="fas fa-play"></i></a>` : `<button class="btn btn--sm btn--outline" disabled><i class="fas fa-lock"></i></button>`}
        </div>
      </div>`
    ).join('') || '<div class="empty-state"><i class="fas fa-video-slash"></i><div class="empty-state__title">Sin clases</div></div>';

    const examsHTML = (course.exams || []).map(ex =>
      `<div class="curso-exam-item">
        <div class="curso-exam-item__header">
          <div class="curso-exam-item__title">${ex.title}</div>
          <span class="badge badge--${ex.attempts_count > 0 ? 'success' : 'warning'}">${ex.attempts_count > 0 ? ex.attempts_count + ' intento(s)' : 'No intentado'}</span>
        </div>
        <div class="curso-exam-item__desc">${ex.description || ''}</div>
        <div class="curso-exam-item__meta">
          <span><i class="fas fa-question-circle"></i> ${ex.questions_count || 0} preguntas</span>
          <span><i class="far fa-clock"></i> ${ex.duration_minutes || '—'} min</span>
          <span><i class="fas fa-check-circle"></i> Aprobacion: ${ex.passing_score || 60}%</span>
        </div>
      </div>`
    ).join('') || '<div class="empty-state"><i class="fas fa-file-alt"></i><div class="empty-state__title">Sin examenes</div></div>';

    const assignHTML = (course.assignments || []).map(a =>
      `<div class="curso-exam-item">
        <div class="curso-exam-item__header">
          <div class="curso-exam-item__title">${a.title}</div>
          <span class="badge badge--warning">${a.submissions_count || 0} entregas</span>
        </div>
        <div class="curso-exam-item__desc">${a.description || ''}</div>
        <div class="curso-exam-item__meta">
          <span><i class="fas fa-calendar-alt"></i> Vence: ${a.due_date ? new Date(a.due_date).toLocaleDateString('es-MX') : '—'}</span>
          <span><i class="fas fa-star"></i> Max: ${a.max_score || 100} pts</span>
        </div>
      </div>`
    ).join('') || '<div class="empty-state"><i class="fas fa-tasks"></i><div class="empty-state__title">Sin tareas</div></div>';

    content.innerHTML = `
      <div class="curso-tab-pane curso-tab-pane--active" id="cursoTabClases"><div class="curso-class-list">${classesHTML}</div></div>
      <div class="curso-tab-pane" id="cursoTabExamenes"><div class="curso-class-list">${examsHTML}</div></div>
      <div class="curso-tab-pane" id="cursoTabTareas"><div class="curso-class-list">${assignHTML}</div></div>
    `;
  }
};

function navigate(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('page--active'));
  const base = page.split('-')[0];
  const param = page.split('-')[1];
  const pageId = base === 'curso' ? 'curso' : base;
  const t = document.getElementById(`page-${pageId}`);
  if (t) t.classList.add('page--active');
  window.location.hash = '#' + page;
  document.querySelectorAll('[data-nav]').forEach(l => l.classList.toggle('navbar__link--active', l.dataset.nav === page));
  const mm = document.getElementById('mobileMenu');
  if (mm) mm.classList.remove('open');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (base === 'cursos') APP.renderCourseCatalog();
  if (base === 'curso' && param) APP.renderCourseDetail(parseInt(param));
}

function toggleMobileMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }

function switchCursoTab(tabId, btn) {
  document.querySelectorAll('.curso-tab-link').forEach(t => t.classList.remove('curso-tab-link--active'));
  if (btn) btn.classList.add('curso-tab-link--active');
  document.querySelectorAll('.curso-tab-pane').forEach(p => p.classList.remove('curso-tab-pane--active'));
  const target = document.getElementById('cursoTab' + tabId.charAt(0).toUpperCase() + tabId.slice(1));
  if (target) target.classList.add('curso-tab-pane--active');
}

function handleEnroll(courseId) {
  const session = localStorage.getItem('dc_session');
  if (session) {
    navigate('student');
    switchStudentTab('studClasses', document.querySelector('[data-student=studClasses]'));
  } else {
    navigate('login');
  }
}

function switchAuthTab(role, btn) {
  document.querySelectorAll('.auth-card__tab').forEach(t => t.classList.remove('auth-card__tab--active'));
  btn.classList.add('auth-card__tab--active');
  document.getElementById('authStudent').style.display = role === 'student' ? '' : 'none';
  document.getElementById('authAdmin').style.display = role === 'admin' ? '' : 'none';
}

function logout() {
  localStorage.removeItem('dc_session');
  APP.state.currentUser = null;
  APP.updateNav(null);
  navigate('home');
}

document.addEventListener('DOMContentLoaded', () => APP.init());
