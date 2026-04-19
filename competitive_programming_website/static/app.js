(function() {
  let problems = [];
  let currentProblem = null;
  let currentQid = 0;
  let saveTimer = null;

  document.addEventListener('DOMContentLoaded', () => {
    loadProblems();
  });

  async function loadProblems() {
    try {
      const r = await fetch('/api/problems');
      problems = await r.json();
      renderProblems(problems);
      updateCounts();
    } catch(e) {
      document.getElementById('problems-grid').innerHTML =
        '<p style="color:#f85149;text-align:center;width:100%;padding:40px;">Failed to load problems. Please refresh.</p>';
    }
  }

  function updateCounts() {
    const c = {Easy:0,Medium:0,Hard:0};
    problems.forEach(p => c[p.difficulty]++);
    document.getElementById('cnt-easy').textContent = '(' + c.Easy + ')';
    document.getElementById('cnt-med').textContent = '(' + c.Medium + ')';
    document.getElementById('cnt-hard').textContent = '(' + c.Hard + ')';
  }

  function renderProblems(list) {
    const grid = document.getElementById('problems-grid');
    grid.innerHTML = list.map(p => {
      const d = p.difficulty.toLowerCase();
      return '<div class="problem-card ' + d + '" onclick="openProblem(' + p.id + ')">' +
        '<div class="card-num">Problem ' + String(p.id).padStart(2,'0') + ' of 50</div>' +
        '<div class="card-title">' + escapeHtml(p.name) + '</div>' +
        '<div class="card-meta">' +
        '<span class="diff-badge ' + d + '">' + p.difficulty + '</span>' +
        '<span class="topic-badge">' + escapeHtml(p.topic) + '</span>' +
        '</div></div>';
    }).join('');
  }

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      if (f === 'all') renderProblems(problems);
      else renderProblems(problems.filter(p => p.difficulty === f));
    });
  });

  async function openProblem(qid) {
    currentQid = qid;
    
    // Fetch full problem detail
    try {
      const r = await fetch('/api/problem?id=' + qid);
      currentProblem = await r.json();
    } catch(e) {
      alert('Failed to load problem.');
      return;
    }
    if (!currentProblem) { alert('Problem not found.'); return; }

    document.getElementById('q-badge').textContent = 'Problem ' + String(qid).padStart(2,'0') + '/50';
    document.getElementById('modal-title').textContent = currentProblem.name;
    const diffEl = document.getElementById('modal-diff');
    diffEl.textContent = currentProblem.difficulty;
    diffEl.className = 'diff-badge ' + currentProblem.difficulty.toLowerCase();

    // Show function name hint
    const descEl = document.getElementById('desc-content');
    let descHtml = currentProblem.description || '<p>No description available.</p>';
    
    // Add function hint if available
    if (currentProblem.func_name && currentProblem.param_names) {
      const params = currentProblem.param_names.join(', ');
      descHtml += '<br><br><div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;margin-top:8px;">' +
        '<div style="color:#58a6ff;font-weight:600;font-size:.85rem;margin-bottom:4px;">📝 Function Signature</div>' +
        '<code style="font-size:.9rem;color:#e6edf3;">def ' + currentProblem.func_name + '(' + params + '):</code>' +
        '<p style="color:#8b949e;font-size:.8rem;margin-top:6px;">Write your solution with this function name in the editor.</p></div>';
    }
    descEl.innerHTML = descHtml;

    const editor = document.getElementById('code-editor');
    {
      const fn = currentProblem.func_name || 'solve';
      const params = currentProblem.param_names ? currentProblem.param_names.join(', ') : 'input';
      editor.value = '# Write your solution here\n# Function to implement: ' + fn + '\n\n' +
        'def ' + fn + '(' + params + '):\n    pass\n';
    }
    
    document.getElementById('results-panel').style.display = 'none';
    document.getElementById('btn-next').style.display = 'none';
    document.getElementById('btn-submit').style.display = '';
    document.getElementById('btn-submit').disabled = false;
    document.getElementById('btn-submit').innerHTML = '▶ Submit';
    document.getElementById('editor-status').textContent = 'saved';

    document.getElementById('modal-overlay').classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  window.openProblem = openProblem;

  window.closeModal = function() {
    document.getElementById('modal-overlay').classList.remove('show');
    document.body.style.overflow = '';
    if (currentQid) localStorage.removeItem('cp_q' + currentQid);
  };
  document.getElementById('close-btn').addEventListener('click', closeModal);
  document.getElementById('modal-overlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal-overlay')) closeModal();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  const editor = document.getElementById('code-editor');
  editor.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const s = editor.selectionStart, end = editor.selectionEnd;
      editor.value = editor.value.substring(0, s) + '    ' + editor.value.substring(end);
      editor.selectionStart = editor.selectionEnd = s + 4;
      autoSave();
    }
  });

  editor.addEventListener('input', () => {
    document.getElementById('editor-status').textContent = 'typing...';
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      if (currentQid) {
        localStorage.setItem('cp_q' + currentQid, editor.value);
        document.getElementById('editor-status').textContent = 'saved ✓';
        setTimeout(() => { document.getElementById('editor-status').textContent = 'saved'; }, 2000);
      }
    }, 600);
  });

  window.submitCode = async function() {
    const code = editor.value;
    const btn = document.getElementById('btn-submit');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Running...';

    try {
      const r = await fetch('/api/run', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({qid: currentQid, code: code})
      });
      const result = await r.json();
      showResults(result);
    } catch (e) {
      alert('Error running tests: ' + e.message);
    }
  };

  function showResults(result) {
    const panel = document.getElementById('results-panel');
    const header = document.getElementById('results-header');
    const list = document.getElementById('test-list');
    panel.style.display = '';

    // Re-enable submit button after 3 seconds
    const btn = document.getElementById('btn-submit');
    btn.disabled = true;
    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = '▶ Submit';
    }, 2000);

    let html = '';
    if (result.all_passed) {
      html = '<div class="msg success">🎉 All ' + result.total + ' test cases passed! Congratulations!</div>';
      launchConfetti();
      document.getElementById('btn-next').style.display = '';
    } else {
      html = '<div class="msg fail">' + result.passed + ' of ' + result.total + ' tests passed</div>';
      html += '<div class="stats"><span class="stat pass">' + result.passed + ' passed</span><span class="stat fail">' + result.failed + ' failed</span></div>';
    }
    header.innerHTML = html;

    list.innerHTML = '';
    if (result.test_results && result.test_results.length) {
      result.test_results.forEach(t => {
        const cls = t.status === 'pass' ? 'pass' : 'fail';
        const icon = t.status === 'pass' ? '✓' : '✗';
        const desc = t.name ? t.name : 'Test';
        const msg = t.message ? escapeHtml(t.message).substring(0, 100) : '';
        list.innerHTML += '<li class="test-item ' + cls + '">' +
          '<span class="ticon">' + icon + '</span>' +
          '<div class="tinfo"><div class="tname">' + escapeHtml(desc) + '</div>' +
          '<div class="tdesc">' + (msg ? escapeHtml(msg) : '') + '</div></div></li>';
      });
    }

    panel.scrollIntoView({behavior:'smooth', block:'nearest'});
  }

  window.goNext = function() {
    if (!currentQid || currentQid >= 50) return;
    localStorage.removeItem('cp_q' + currentQid);
    closeModal();
    setTimeout(() => openProblem(currentQid + 1), 200);
  };

  window.clearCode = function() {
    const fn = currentProblem ? (currentProblem.func_name || 'solve') : 'solve';
    const params = currentProblem && currentProblem.param_names ? currentProblem.param_names.join(', ') : 'input';
    editor.value = '# Write your solution here\n# Function to implement: ' + fn + '\n\ndef ' + fn + '(' + params + '):\n    pass\n';
    document.getElementById('results-panel').style.display = 'none';
    document.getElementById('btn-next').style.display = 'none';
    document.getElementById('btn-submit').style.display = '';
    document.getElementById('btn-submit').disabled = false;
    document.getElementById('btn-submit').innerHTML = '▶ Submit';
    if (currentQid) localStorage.removeItem('cp_q' + currentQid);
  };

  function launchConfetti() {
    const container = document.getElementById('confetti');
    container.innerHTML = '';
    const colors = ['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#f778ba','#79c0ff'];
    for (let i = 0; i < 80; i++) {
      const piece = document.createElement('div');
      piece.className = 'confetti';
      piece.style.left = Math.random() * 100 + '%';
      piece.style.animationDelay = Math.random() * 2 + 's';
      piece.style.animationDuration = (2 + Math.random() * 2) + 's';
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
      piece.style.width = (6 + Math.random() * 8) + 'px';
      piece.style.height = (6 + Math.random() * 8) + 'px';
      container.appendChild(piece);
    }
    setTimeout(() => { container.innerHTML = ''; }, 4000);
  }

  function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

})();
