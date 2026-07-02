let examTimer = null;
let examAnswers = [];
let examQuestions = [];

function startExam() {
  document.getElementById('examStart').style.display = 'none';
  document.getElementById('examResult').style.display = 'none';
  document.getElementById('examRunning').style.display = 'block';

  examQuestions = [
    { q:'What is the meaning of "abundant"?', opts:['Scarce','Abundant','Difficult','Quick'], correct:1 },
    { q:'Complete: "If I ___ rich, I would travel."', opts:['am','was','were','be'], correct:2 },
    { q:'Synonym of "happy":', opts:['Sad','Angry','Joyful','Tired'], correct:2 },
    { q:'She ___ English for 5 years.', opts:['study','studies','has studied','studying'], correct:2 },
    { q:'The book ___ on the table.', opts:['is','are','am','be'], correct:0 },
    { q:'___ you like coffee?', opts:['Does','Do','Is','Are'], correct:1 },
    { q:'Opposite of "expensive":', opts:['Cheap','Costly','Valuable','Pricey'], correct:0 },
    { q:'He arrived ___ the airport at 8 AM.', opts:['on','in','at','to'], correct:2 },
    { q:'I ___ seen that movie before.', opts:['have','has','had','was'], correct:0 },
    { q:'Which is correct?', opts:['She go to school','She goes to school','She going school','She to go school'], correct:1 },
  ];

  examAnswers = new Array(examQuestions.length).fill(-1);
  document.getElementById('examTotalQ').textContent = examQuestions.length;

  const cont = document.getElementById('examQuestions');
  cont.innerHTML = examQuestions.map((q, i) =>
    `<div class="exercise-question" id="eq_${i}" style="${i > 0 ? 'display:none' : ''}">
      <div class="exercise-question__text">${i+1}. ${q.q}</div>
      <div class="exercise-options">${q.opts.map((o, j) =>
        `<label class="exercise-option" onclick="selectExamAnswer(${i},${j})" id="eqo_${i}_${j}">
          <span>${o}</span>
        </label>`
      ).join('')}</div>
    </div>`
  ).join('');

  document.getElementById('examCurrentQ').textContent = '1';
  document.getElementById('examProgressFill').style.width = '10%';
  document.getElementById('prevExamBtn').style.visibility = 'hidden';
  startTimer();
}

function selectExamAnswer(qIdx, optIdx) {
  examAnswers[qIdx] = optIdx;
  document.querySelectorAll(`#eq_${qIdx} .exercise-option`).forEach(el => {
    el.style.borderColor = ''; el.style.background = '';
  });
  const sel = document.getElementById(`eqo_${qIdx}_${optIdx}`);
  if (sel) { sel.style.borderColor = 'var(--secondary)'; sel.style.background = '#f0f7ff'; }
}

function nextExamQuestion() {
  const cur = parseInt(document.getElementById('examCurrentQ').textContent) - 1;
  if (cur < examQuestions.length - 1) {
    document.getElementById(`eq_${cur}`).style.display = 'none';
    document.getElementById(`eq_${cur+1}`).style.display = 'block';
    document.getElementById('examCurrentQ').textContent = cur + 2;
    document.getElementById('examProgressFill').style.width = ((cur+2)/examQuestions.length*100) + '%';
    document.getElementById('prevExamBtn').style.visibility = 'visible';
  } else {
    finishExam();
  }
}

function prevExamQuestion() {
  const cur = parseInt(document.getElementById('examCurrentQ').textContent) - 1;
  if (cur > 0) {
    document.getElementById(`eq_${cur}`).style.display = 'none';
    document.getElementById(`eq_${cur-1}`).style.display = 'block';
    document.getElementById('examCurrentQ').textContent = cur;
    document.getElementById('examProgressFill').style.width = (cur/examQuestions.length*100) + '%';
    if (cur === 1) document.getElementById('prevExamBtn').style.visibility = 'hidden';
  }
}

function startTimer() {
  let min = 15, sec = 0;
  const el = document.getElementById('examTimer');
  if (examTimer) clearInterval(examTimer);
  examTimer = setInterval(() => {
    if (sec === 0) {
      if (min === 0) { clearInterval(examTimer); finishExam(); return; }
      min--; sec = 59;
    } else { sec--; }
    el.textContent = `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
    el.classList.toggle('exam-timer--warning', min < 2);
  }, 1000);
}

function finishExam() {
  if (examTimer) { clearInterval(examTimer); examTimer = null; }
  let correct = 0;
  const unans = examAnswers.filter(a => a === -1).length;
  examQuestions.forEach((q, i) => { if (examAnswers[i] === q.correct) correct++; });

  document.getElementById('examRunning').style.display = 'none';
  const res = document.getElementById('examResult');
  res.style.display = 'block';
  const pct = Math.round(correct/examQuestions.length*100);
  const passed = pct >= 70;

  res.innerHTML = `
    <div class="exercise-result" style="text-align:center;padding:48px 32px;background:var(--bg-card);border-radius:var(--radius);box-shadow:var(--shadow)">
      <div style="font-size:3.5rem;font-weight:900;color:${passed?'var(--success)':'var(--danger)'}">${correct}/${examQuestions.length}</div>
      <p style="font-size:1.4rem;font-weight:700;margin:12px 0">${passed ? 'Aprobado!' : 'No aprobado'}</p>
      <p style="color:var(--text-light);margin-bottom:16px">Calificacion: ${pct}% ${unans > 0 ? `(${unans} sin responder)` : ''}</p>
      <div style="margin:0 auto 24px;max-width:300px;height:8px;background:var(--bg);border-radius:4px;overflow:hidden">
        <div style="height:100%;width:${pct}%;background:${passed?'var(--success)':'var(--danger)'};border-radius:4px;transition:width 0.5s"></div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:24px">
        ${examQuestions.map((q,i) =>
          `<span style="width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;
            background:${examAnswers[i]===-1?'#e0e0e0':examAnswers[i]===q.correct?'#e8f5e9':'#ffebee'};
            color:${examAnswers[i]===-1?'#999':examAnswers[i]===q.correct?'var(--success)':'var(--danger)'}">${i+1}</span>`
        ).join('')}
      </div>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <button class="btn btn--primary" onclick="startExam()"><i class="fas fa-redo"></i> Reintentar</button>
        ${passed ? `<button class="btn btn--accent" onclick="showCertFromExam(${pct})"><i class="fas fa-certificate"></i> Ver Certificado</button>` : ''}
        <button class="btn btn--ghost" onclick="switchStudentTab('studDashboard',document.querySelector('[data-student=studDashboard]'))">Volver</button>
      </div>
    </div>`;
}

function showCertFromExam(pct) {
  const user = APP.state.currentUser;
  if (user) {
    const cn = document.getElementById('certName');
    if (cn) cn.textContent = user.name + ' ' + user.last;
  }
  document.getElementById('certCode').textContent = 'DC-EX-2026-' + String(Math.floor(Math.random()*9000)+1000);
  document.getElementById('certFolio').textContent = document.getElementById('certCode').textContent;
  document.getElementById('certDate').textContent = new Date().toLocaleDateString('es-MX', {year:'numeric',month:'long',day:'numeric'});
  switchStudentTab('studCertificates', document.querySelector('[data-student=studCertificates]'));
}
