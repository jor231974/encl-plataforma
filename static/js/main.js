document.addEventListener('DOMContentLoaded', function() {
    // ==================== ANIMATIONS ON SCROLL ====================
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
    animateElements.forEach(el => observer.observe(el));

    // ==================== COUNTER ANIMATION ====================
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'));
        if (!target) return;
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                el.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                el.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    document.querySelectorAll('.stat-counter').forEach(el => counterObserver.observe(el));

    // ==================== SIDEBAR TOGGLE ====================
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.dashboard-sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 991 && sidebar.classList.contains('open')) {
                if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
    }

    // ==================== TERRITORIAL CASCADING ====================
    const estadoSelect = document.getElementById('estado_id');
    const municipioSelect = document.getElementById('municipio_id');
    const distritoSelect = document.getElementById('distrito_id');
    const grupoSelect = document.getElementById('grupo_id');

    if (estadoSelect) {
        estadoSelect.addEventListener('change', function() {
            const estadoId = this.value;
            if (municipioSelect) {
                municipioSelect.innerHTML = '<option value="">Seleccionar municipio</option>';
                municipioSelect.disabled = true;
            }
            if (distritoSelect) {
                distritoSelect.innerHTML = '<option value="">Seleccionar distrito</option>';
                distritoSelect.disabled = true;
            }
            if (grupoSelect) {
                grupoSelect.innerHTML = '<option value="">Seleccionar grupo</option>';
                grupoSelect.disabled = true;
            }
            if (estadoId) {
                fetch('/admin/api/municipios/' + estadoId)
                    .then(r => r.json())
                    .then(data => {
                        municipioSelect.disabled = false;
                        data.forEach(m => {
                            const opt = document.createElement('option');
                            opt.value = m.id;
                            opt.textContent = m.nombre;
                            municipioSelect.appendChild(opt);
                        });
                    });
            }
        });
    }

    if (municipioSelect) {
        municipioSelect.addEventListener('change', function() {
            const municipioId = this.value;
            if (distritoSelect) {
                distritoSelect.innerHTML = '<option value="">Seleccionar distrito</option>';
                distritoSelect.disabled = true;
            }
            if (grupoSelect) {
                grupoSelect.innerHTML = '<option value="">Seleccionar grupo</option>';
                grupoSelect.disabled = true;
            }
            if (municipioId) {
                fetch('/admin/api/distritos/' + municipioId)
                    .then(r => r.json())
                    .then(data => {
                        distritoSelect.disabled = false;
                        data.forEach(d => {
                            const opt = document.createElement('option');
                            opt.value = d.id;
                            opt.textContent = d.nombre;
                            distritoSelect.appendChild(opt);
                        });
                    });
            }
        });
    }

    if (distritoSelect) {
        distritoSelect.addEventListener('change', function() {
            const distritoId = this.value;
            if (grupoSelect) {
                grupoSelect.innerHTML = '<option value="">Seleccionar grupo</option>';
                grupoSelect.disabled = true;
            }
            if (distritoId) {
                fetch('/admin/api/grupos/' + distritoId)
                    .then(r => r.json())
                    .then(data => {
                        grupoSelect.disabled = false;
                        data.forEach(g => {
                            const opt = document.createElement('option');
                            opt.value = g.id;
                            opt.textContent = g.nombre;
                            grupoSelect.appendChild(opt);
                        });
                    });
            }
        });
    }

    // ==================== TOOLTIP INIT ====================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));

    // ==================== AUTO DISMISS ALERTS ====================
    document.querySelectorAll('.alert-auto-dismiss').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // ==================== LIVE CLASS ROOM ====================
    const videoContainer = document.querySelector('.video-container');
    if (videoContainer) {
        const joinBtn = videoContainer.querySelector('.btn-join-live');
        if (joinBtn) {
            joinBtn.addEventListener('click', function() {
                const url = this.getAttribute('data-url');
                if (url) {
                    window.open(url, '_blank');
                }
            });
        }
    }

    // ==================== CHART INITIALIZATION ====================
    if (typeof Chart !== 'undefined') {
        document.querySelectorAll('canvas[data-chart]').forEach(canvas => {
            const type = canvas.getAttribute('data-chart-type') || 'bar';
            const labels = JSON.parse(canvas.getAttribute('data-labels') || '[]');
            const values = JSON.parse(canvas.getAttribute('data-values') || '[]');
            const label = canvas.getAttribute('data-label') || 'Datos';
            const chartId = canvas.id;

            const config = {
                type: type,
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: values,
                        backgroundColor: [
                            'rgba(26,35,126,0.7)',
                            'rgba(0,200,83,0.7)',
                            'rgba(13,110,253,0.7)',
                            'rgba(255,193,7,0.7)',
                            'rgba(220,53,69,0.7)',
                            'rgba(111,66,193,0.7)',
                            'rgba(32,201,151,0.7)',
                            'rgba(253,126,20,0.7)'
                        ],
                        borderWidth: 0,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { display: false } },
                        x: { grid: { display: false } }
                    }
                }
            };

            if (type === 'doughnut' || type === 'pie') {
                config.options.plugins.legend = { display: true, position: 'bottom' };
            }
            if (type === 'line') {
                config.data.datasets[0].fill = true;
                config.data.datasets[0].backgroundColor = 'rgba(26,35,126,0.1)';
                config.data.datasets[0].borderColor = 'rgba(26,35,126,0.8)';
                config.data.datasets[0].borderWidth = 2;
                config.data.datasets[0].tension = 0.4;
            }

            new Chart(document.getElementById(chartId), config);
        });
    }

    // ==================== EXAM AUTO CALCULATION ====================
    const examForm = document.querySelector('.exam-form');
    if (examForm) {
        const questions = examForm.querySelectorAll('.exam-question');
        let examTimer = null;
        const timerDisplay = document.getElementById('exam-timer');
        if (timerDisplay) {
            let timeLeft = parseInt(timerDisplay.getAttribute('data-time')) * 60;
            examTimer = setInterval(() => {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                if (timeLeft <= 0) {
                    clearInterval(examTimer);
                    examForm.submit();
                }
                timeLeft--;
            }, 1000);
        }
    }

    // ==================== CONFIRM DIALOGS ====================
    document.querySelectorAll('[data-confirm]').forEach(el => {
        el.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm') || '¿Estás seguro?')) {
                e.preventDefault();
            }
        });
    });

    // ==================== SEARCH COURSES ====================
    const searchInput = document.getElementById('search-courses');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const q = this.value.toLowerCase();
            document.querySelectorAll('.course-card').forEach(card => {
                const title = card.querySelector('h5')?.textContent.toLowerCase() || '';
                const desc = card.querySelector('p')?.textContent.toLowerCase() || '';
                if (title.includes(q) || desc.includes(q)) {
                    card.closest('.col-md-6, .col-lg-4')?.style.removeProperty('display');
                } else {
                    card.closest('.col-md-6, .col-lg-4')?.style.setProperty('display', 'none');
                }
            });
        });
    }

    // ==================== SMOOTH SCROLL ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // ==================== MESSAGE MARK READ ====================
    document.querySelectorAll('.message-item').forEach(item => {
        item.addEventListener('click', function() {
            const msgId = this.getAttribute('data-message-id');
            if (msgId && !this.classList.contains('read')) {
                fetch('/alumno/leer-mensaje/' + msgId, { method: 'GET' });
                this.classList.add('read');
                this.querySelector('.badge')?.remove();
            }
        });
    });

    console.log('ENCL Platform initialized successfully');
});
