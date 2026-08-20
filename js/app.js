(function () {
  'use strict';
  const T = window.Tools, $ = id => document.getElementById(id);
  const NS = 'http://www.w3.org/2000/svg';
  function el(n, a, t) { const e = document.createElementNS(NS, n); for (const k in a) if (a[k] != null) e.setAttribute(k, a[k]); if (t != null) e.textContent = t; return e; }
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  const wave = t => 0.5 + 0.32 * Math.sin(t * Math.PI * 2) + 0.13 * Math.sin(t * Math.PI * 6 + 1);

  /* ---------- STEP1 ---------- */
  function drawWave() {
    const L = +$('levels').value, S = +$('samples').value;
    $('levelsV').textContent = L; $('samplesV').textContent = S;
    const W = 460, H = 300, M = { t: 14, r: 14, b: 28, l: 34 };
    const iw = W - M.l - M.r, ih = H - M.t - M.b;
    const X = t => M.l + t * iw, Y = v => M.t + ih - v * ih;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'アナログ波とデジタル化' });
    for (let k = 0; k < L; k++) {
      const y = Y(k / (L - 1));
      svg.appendChild(el('line', { x1: M.l, y1: y, x2: M.l + iw, y2: y, class: 'lvl' }));
    }
    const pts = [];
    for (let k = 0; k <= 200; k++) { const t = k / 200; pts.push(X(t) + ',' + Y(wave(t))); }
    svg.appendChild(el('polyline', { points: pts.join(' '), class: 'ana' }));
    const dpts = [];
    let err = 0;
    for (let i = 0; i < S; i++) {
      const t = i / (S - 1);
      const v = wave(t);
      const q = Math.round(v * (L - 1)) / (L - 1);
      err += Math.abs(v - q);
      dpts.push([X(t), Y(q)]);
      svg.appendChild(el('circle', { cx: X(t), cy: Y(q), r: 3, class: 'smp' }));
    }
    let d = '';
    dpts.forEach((p, i) => {
      if (i === 0) d += 'M' + p[0] + ' ' + p[1];
      else d += ' L' + dpts[i - 1][0] + ' ' + p[1] + ' L' + p[0] + ' ' + p[1];
    });
    svg.appendChild(el('path', { d, class: 'dig' }));
    svg.appendChild(el('text', { x: M.l, y: H - 8, class: 'lab' }, '時間 →'));
    const box = $('waveBox'); box.innerHTML = ''; box.appendChild(svg);

    const bits = Math.ceil(Math.log2(L));
    $('mBits').textContent = bits;
    $('mSize').textContent = (bits * S).toLocaleString();
    $('mErr').textContent = (err / S * 100).toFixed(1);
    const n = $('waveNote');
    const fine = L >= 16 && S >= 30;
    n.className = 'note ' + (fine ? 'ok' : 'warn');
    n.innerHTML = fine
      ? '細かく区切ったので、元の波にかなり近づきました。そのぶん<strong>データ量は ' + (bits * S) + ' ビット</strong>に増えています。'
      : '段階や回数が少ないと、<strong>元の波の形が失われます</strong>（ずれ ' + (err / S * 100).toFixed(1) +
        '％）。細かくすると再現度は上がりますが、データ量も増えます。';
  }

  /* ---------- STEP2 ノイズ ---------- */
  let seed = 1;
  function rnd(i) { const x = Math.sin(i * 127.1 + seed * 311.7) * 43758.5453; return x - Math.floor(x); }
  function drawNoise() {
    const nz = +$('noise').value / 100;
    $('noiseV').textContent = Math.round(nz * 100);
    const W = 660, H = 280, M = { t: 18, r: 14, b: 24, l: 70 };
    const iw = W - M.l - M.r;
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'ノイズの影響' });
    const rows = [
      { y: 60, t: 'アナログ', kind: 'a' },
      { y: 170, t: 'デジタル', kind: 'd' }
    ];
    rows.forEach(r => {
      svg.appendChild(el('text', { x: 8, y: r.y - 22, class: 'lab', 'font-size': 11, fill: '#15181c', 'font-weight': 700 }, r.t));
      const pts = [], org = [];
      for (let k = 0; k <= 120; k++) {
        const t = k / 120;
        const base = r.kind === 'a' ? wave(t) : (Math.floor(t * 8) % 2 === 0 ? 0.85 : 0.15);
        const v = Math.max(0, Math.min(1, base + (rnd(k + (r.kind === 'a' ? 0 : 500)) - .5) * nz * 1.6));
        pts.push((M.l + t * iw) + ',' + (r.y + 34 - v * 68));
        org.push((M.l + t * iw) + ',' + (r.y + 34 - base * 68));
      }
      svg.appendChild(el('polyline', { points: org.join(' '), stroke: '#d7d3cb', 'stroke-width': 1.6, fill: 'none' }));
      svg.appendChild(el('polyline', { points: pts.join(' '), class: r.kind === 'a' ? 'ana' : 'dig' }));
      if (r.kind === 'd') {
        svg.appendChild(el('line', { x1: M.l, y1: r.y, x2: M.l + iw, y2: r.y, class: 'thr' }));
        svg.appendChild(el('text', { x: M.l + iw - 4, y: r.y - 5, class: 'lab', fill: '#b3261e', 'text-anchor': 'end' }, 'しきい値'));
        // 復元した信号
        const rec = [];
        for (let k = 0; k <= 120; k++) {
          const t = k / 120;
          const base = (Math.floor(t * 8) % 2 === 0 ? 0.85 : 0.15);
          const v = Math.max(0, Math.min(1, base + (rnd(k + 500) - .5) * nz * 1.6));
          rec.push((M.l + t * iw) + ',' + (r.y + 100 - (v > 0.5 ? 0.85 : 0.15) * 68));
        }
        svg.appendChild(el('polyline', { points: rec.join(' '), stroke: '#1f7a3d', 'stroke-width': 2.4, fill: 'none' }));
        svg.appendChild(el('text', { x: 8, y: r.y + 78, class: 'lab', 'font-size': 10.5, fill: '#1f7a3d', 'font-weight': 700 }, '復元後'));
      }
    });
    const box = $('noiseBox'); box.innerHTML = ''; box.appendChild(svg);
    const n = $('noiseNote');
    const broken = nz > 0.5;
    n.className = 'note ' + (broken ? 'ng' : (nz > 0 ? 'ok' : 'info'));
    n.innerHTML = nz === 0
      ? 'ノイズを大きくして、両者のちがいを見てください。'
      : (broken
        ? 'ノイズが大きすぎると、<strong>デジタルでもしきい値の判定をまちがえます</strong>。ただしアナログよりはずっと強いことがわかります。'
        : 'アナログはノイズがそのまま信号のずれになります。デジタルは<strong>しきい値より上か下かだけを見る</strong>ので、' +
          '<strong>緑の線のようにきれいに復元できます</strong>。だから何度コピーしても劣化しません。');
  }

  /* ---------- STEP3 ビット数 ---------- */
  function drawBits() {
    const k = +$('kinds').value;
    $('kindsV').textContent = k;
    const n = Math.ceil(Math.log2(k));
    $('bitCalc').innerHTML = '2<sup>' + (n - 1) + '</sup> ＝ ' + Math.pow(2, n - 1) + ' < <strong>' + k +
      '</strong> ≦ 2<sup>' + n + '</sup> ＝ ' + Math.pow(2, n) + '<br>→ 必要なビット数は <strong style="font-size:1.5rem">' + n + ' ビット</strong>';
    let h = '<thead><tr><th>ビット数</th><th>表せる種類</th><th>足りるか</th></tr></thead><tbody>';
    for (let b = Math.max(1, n - 3); b <= n + 2; b++) {
      const c = Math.pow(2, b);
      h += '<tr' + (b === n ? ' style="background:var(--warn-bg);font-weight:700"' : '') + '><td class="mono">' + b +
        '</td><td class="mono">' + c.toLocaleString() + '</td><td style="color:' + (c >= k ? 'var(--ok)' : 'var(--ng)') + '">' +
        (c >= k ? '足りる' : '足りない') + '</td></tr>';
    }
    $('powTable').innerHTML = h + '</tbody>';
  }

  /* ---------- STEP4 クイズ ---------- */
  const QUIZ = [
    { t: '情報を連続する可変な物理量で表したものと、離散的な数値で表したもの、CDが記録するデータの組み合わせとして正しいものはどれか。',
      choices: ['アナログ・デジタル・デジタル', 'アナログ・デジタル・アナログ',
                'デジタル・アナログ・アナログ', 'デジタル・アナログ・デジタル'],
      a: 'アナログ・デジタル・デジタル',
      why: '連続＝アナログ、離散＝デジタル。CDは音をデジタルデータとして記録する光ディスクです。' },
    { t: 'デジタルデータの説明として<strong>適当でない</strong>ものはどれか。',
      choices: ['必ず元のアナログデータを完全に再現することができる',
                'コピーを繰り返しても劣化しない',
                'さまざまな表現メディアを統合的に扱うことができる',
                'ノイズが混入してもしきい値を設けることで復元できる'],
      a: '必ず元のアナログデータを完全に再現することができる',
      why: 'デジタル化は段階に区切る作業なので、<strong>その間の情報は失われます</strong>。細かくすれば近づきますが、完全な再現ではありません。' },
    { t: 'A〜Z、a〜z、0〜9をすべて区別するには最低何ビット必要か。',
      choices: ['6ビット', '5ビット', '7ビット', '8ビット'], a: '6ビット',
      why: '26＋26＋10＝62種類。2⁵＝32では足りず、2⁶＝64で足ります。よって<strong>6ビット</strong>です。' },
    { t: 'デジタル化の手順として正しい順番はどれか。',
      choices: ['標本化 → 量子化 → 符号化', '量子化 → 標本化 → 符号化',
                '符号化 → 標本化 → 量子化', '標本化 → 符号化 → 量子化'],
      a: '標本化 → 量子化 → 符号化',
      why: '一定間隔で読み取り（標本化）、段階に当てはめ（量子化）、0と1に直す（符号化）の順です。' },
    { t: 'デジタルがノイズに強い理由はどれか。',
      choices: ['0か1かの判定だけなので、しきい値で元にもどせるから',
                'ノイズが入らないから', 'データ量が小さいから', '電気を使わないから'],
      a: '0か1かの判定だけなので、しきい値で元にもどせるから',
      why: '多少の乱れがあっても、しきい値より上か下かがわかれば元の0と1を復元できます。' }
  ];
  let qList = [], qi = 0, qScore = 0;
  function startQuiz() { qList = shuffle(QUIZ); qi = 0; qScore = 0; renderQ(); }
  function renderQ() {
    if (qi >= qList.length) {
      $('qText').textContent = qScore + ' / ' + qList.length + ' 問正解';
      $('qChoices').innerHTML = ''; $('qFb').hidden = true; $('qNext').disabled = true;
      $('qProgress').textContent = qList.length + ' / ' + qList.length; return;
    }
    const it = qList[qi];
    $('qProgress').textContent = (qi + 1) + ' / ' + qList.length;
    $('qScore').textContent = qScore;
    $('qText').innerHTML = it.t;
    const box = $('qChoices'); box.className = 'choice4'; box.innerHTML = '';
    shuffle(it.choices).forEach(c => {
      const b = document.createElement('button');
      b.className = 'btn'; b.textContent = c; b.dataset.c = c;
      b.addEventListener('click', () => answerQ(c));
      box.appendChild(b);
    });
    $('qFb').hidden = true; $('qNext').disabled = true;
    $('qNext').textContent = (qi === qList.length - 1) ? '結果を見る' : '次の問題';
  }
  function answerQ(c) {
    const it = qList[qi], ok = c === it.a, box = $('qChoices');
    box.classList.add('locked');
    [...box.children].forEach(b => {
      if (b.dataset.c === it.a) b.classList.add('correct');
      else if (b.dataset.c === c) b.classList.add('wrong');
    });
    if (ok) qScore++;
    const fb = $('qFb');
    fb.className = 'note ' + (ok ? 'ok' : 'ng');
    fb.innerHTML = (ok ? '正解。' : '正解は「<strong>' + it.a + '</strong>」。') + it.why;
    fb.hidden = false;
    $('qScore').textContent = qScore; $('qNext').disabled = false;
  }

  /* 本文の問題 */
  function drawBook() {
    if (!document.getElementById('bookBox')) return;
    window.Quiz.choice('bookBox', 'bookNote', [{"k": "ア", "q": "【a】連続する可変な物理量で表したもの／【b】離散的な数値で表したもの／【c】CDが格納するデータ の組合せは。", "ch": ["a アナログ／b デジタル／c アナログ", "a アナログ／b デジタル／c デジタル", "a デジタル／b アナログ／c アナログ", "a デジタル／b アナログ／c デジタル"], "a": 1, "why": "連続がアナログ、離散がデジタル。CDは<strong>デジタル</strong>で記録します（カセットテープはアナログ）。"}, {"k": "イ", "q": "デジタルデータに関する説明として<strong>適当でない</strong>ものは。", "ch": ["コピーを繰り返しても劣化しない", "さまざまな表現メディアを統合的に扱うことができる", "必ず元のアナログデータを完全に再現することができる", "ノイズが混入しても、しきい値を設けることで復元できる"], "a": 2, "why": "標本化・量子化のときに<strong>必ず切り捨てが起こる</strong>ので、完全な再現はできません。「必ず」「完全に」は要注意の言い回しです。"}, {"k": "ウ", "q": "A〜Z、a〜z、0〜9をすべて区別するには、少なくとも何ビット必要か。", "ch": ["3", "4", "5", "6", "7", "8"], "a": 3, "why": "26＋26＋10＝62種類。2⁵＝32では足りず、2⁶＝64で足りるので<strong>6ビット</strong>です。"}], "本文の答えは【ア】①　【イ】②　【ウ】6 です。");
  }

  function init() {
    ['levels', 'samples'].forEach(i => $(i).addEventListener('input', drawWave));
    $('noise').addEventListener('input', drawNoise);
    $('reNoise').addEventListener('click', () => { seed = Math.random() * 100; drawNoise(); });
    $('kinds').addEventListener('input', drawBits);
    document.querySelectorAll('[data-kinds]').forEach(b => b.addEventListener('click', () => {
      $('kinds').value = b.dataset.kinds; drawBits();
    }));
    $('qNext').addEventListener('click', () => { qi++; renderQ(); });
    $('qReset').addEventListener('click', startQuiz);
    window.Terms.glossary($('glossBox'), ['アナログ', 'デジタル', '標本化', '量子化', '符号化', '2進法', '可逆圧縮', '非可逆圧縮']);
    drawWave(); drawNoise(); drawBits(); startQuiz();
    drawBook();
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
