function renderStudentPanel(user) {
  document.getElementById('studSideName').textContent = user.name + ' ' + user.last;
  document.getElementById('studWelcomeName').textContent = user.name + ' ' + user.last;
  document.getElementById('studAvatar').textContent = user.name.charAt(0);
  document.getElementById('studSideLevel').textContent = user.level || 'Nivel A2 - Intermedio';

  const certName = document.getElementById('certName');
  if (certName) certName.textContent = user.name + ' ' + user.last;
  const profName = document.getElementById('profName');
  if (profName) profName.textContent = user.name + ' ' + user.last;
  const profEmail = document.getElementById('profEmail');
  if (profEmail) profEmail.textContent = user.email;
  const profAvatar = document.getElementById('profAvatar');
  if (profAvatar) profAvatar.textContent = user.name.charAt(0);
}

function switchStudentTab(tabId, btn) {
  document.querySelectorAll('.sidebar__nav a').forEach(a => a.classList.remove('sidebar__link--active'));
  if (btn) btn.classList.add('sidebar__link--active');

  document.querySelectorAll('.student-tab').forEach(t => t.classList.remove('student-tab--active'));
  const target = document.getElementById(tabId);
  if (target) target.classList.add('student-tab--active');

  if (tabId === 'studExercises') renderExercise();
  if (tabId === 'studExams') { document.getElementById('examStart').style.display = 'block'; document.getElementById('examRunning').style.display = 'none'; document.getElementById('examResult').style.display = 'none'; }
  if (tabId === 'studCertificates') {
    document.getElementById('certCode').textContent = 'DC-B1-2026-' + String(Math.floor(Math.random()*9000)+1000);
    document.getElementById('certFolio').textContent = document.getElementById('certCode').textContent;
    document.getElementById('certDate').textContent = new Date().toLocaleDateString('es-MX', {year:'numeric',month:'long',day:'numeric'});
  }
}

function sendChat() {
  const input = document.getElementById('chatInput');
  if (!input.value.trim()) return;
  const msg = document.createElement('div');
  msg.className = 'live-chat__msg';
  msg.innerHTML = '<strong>Tu:</strong> ' + input.value;
  document.getElementById('chatMessages').appendChild(msg);
  input.value = '';
  document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
}

function renderExercise() {
  const cont = document.getElementById('exerciseQuestions');
  if (!cont) return;
  document.getElementById('exerciseResult').style.display = 'none';
  document.getElementById('exerciseWrap').style.display = 'block';
  document.getElementById('submitExerciseBtn').disabled = false;

  const qs = [
    { q:'Translate: "Good morning"', opts:['A) Buenas tardes','B) Buenos dias','C) Buenas noches','D) Gracias'], correct:1 },
    { q:'Translate: "How are you?"', opts:['A) Como estas?','B) Donde estas?','C) Quien eres?','D) Que hora es?'], correct:0 },
    { q:'What is the meaning of "beautiful"?', opts:['A) Feo','B) Hermoso','C) Grande','D) Rapido'], correct:1 },
    { q:'Complete: "She ___ a teacher."', opts:['A) am','B) are','C) is','D) be'], correct:2 },
    { q:'Choose the correct: "I ___ to school every day."', opts:['A) go','B) goes','C) going','D) went'], correct:0 },
  ];

  cont.innerHTML = qs.map((q, i) =>
    `<div class="exercise-question" data-eq="${i}">
      <div class="exercise-question__text">${i+1}. ${q.q}</div>
      <div class="exercise-options">${q.opts.map((o, j) =>
        `<label class="exercise-option" data-eq="${i}" data-eo="${j}">
          <input type="radio" name="ex_q${i}" value="${j}" onchange="clearExOpts(${i})">
          <span>${o}</span>
        </label>`
      ).join('')}</div>
    </div>`
  ).join('');
}

function clearExOpts(idx) {
  document.querySelectorAll(`.exercise-option[data-eq="${idx}"]`).forEach(o => {
    o.classList.remove('exercise-option--correct','exercise-option--incorrect','exercise-option--disabled');
    o.querySelector('input').disabled = false;
  });
}

function submitExercise() {
  const qs = [
    { correct:1 }, { correct:0 }, { correct:1 }, { correct:2 }, { correct:0 }
  ];
  let correct = 0;
  qs.forEach((q, i) => {
    const sel = document.querySelector(`input[name="ex_q${i}"]:checked`);
    const ans = sel ? parseInt(sel.value) : -1;
    document.querySelectorAll(`.exercise-option[data-eq="${i}"]`).forEach((o, j) => {
      o.querySelector('input').disabled = true;
      o.classList.add('exercise-option--disabled');
      if (j === q.correct) o.classList.add('exercise-option--correct');
      else if (j === ans && ans !== q.correct) o.classList.add('exercise-option--incorrect');
    });
    if (ans === q.correct) correct++;
  });
  document.getElementById('submitExerciseBtn').disabled = true;
  const pct = Math.round(correct/qs.length*100);
  const res = document.getElementById('exerciseResult');
  res.style.display = 'block';
  res.innerHTML =
    `<div class="exercise-result" style="text-align:center;padding:40px;background:var(--bg-card);border-radius:var(--radius);box-shadow:var(--shadow)">
      <div style="font-size:3rem;font-weight:900;color:${pct>=80?'var(--success)':'var(--accent)'}">${correct}/${qs.length}</div>
      <p style="font-size:1.2rem;font-weight:700;margin:8px 0">${pct>=80?'Excelente!':pct>=60?'Bien, sigue practicando':'Sigue estudiando'}</p>
      <p style="color:var(--text-light)">Calificacion: ${pct}%</p>
      <button class="btn btn--primary mt-3" onclick="renderExercise()"><i class="fas fa-redo"></i> Intentar de nuevo</button>
    </div>`;
}
