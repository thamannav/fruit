/**
 * Fruit Angle Detector — Client-side Application Logic
 * Supports multi-image upload (1, 2, 5, 10+), drag & drop,
 * progressive queuing, independent computer-vision analysis,
 * dynamic compass gauges, result filtering,
 * AND 11 hilarious/useless features.
 */

// Global State
let queuedFiles = [];
let allResults = [];
let activeFilter = 'all';

// Fruit Emoji Mapping for rich aesthetics
const FRUIT_EMOJIS = {
  banana: '🍌',
  apple: '🍎',
  orange: '🍊',
  watermelon: '🍉',
  mango: '🥭',
  pineapple: '🍍',
  papaya: '🍈',
  lemon: '🍋',
  cucumber: '🥒',
  pear: '🍐',
  kiwi: '🥝',
  strawberry: '🍓',
  grape: '🍇',
  peach: '🍑',
  avocado: '🥑',
  cherry: '🍒',
  lime: '🍋',
  unknown: '❓'
};

// 8. Funny Rotating Loading Messages
const FUNNY_LOADING_MESSAGES = [
  "🔬 Measuring fruit geometry...",
  "🧠 Consulting the banana council...",
  "📐 Calculating absolutely necessary information...",
  "🍉 Asking the watermelon about its life choices...",
  "🤖 AI is judging your fruit...",
  "📊 Performing extremely important fruit mathematics...",
  "🧪 Science is happening..."
];

// 1. Fruit Personalities
const FRUIT_PERSONALITIES = {
  banana: [
    "Chill guy. Just hanging around.",
    "Thinks it's a boomerang.",
    "Potassium-powered philosopher.",
    "Bends under pressure, but never breaks."
  ],
  apple: [
    "Teacher's pet energy.",
    "Newton's favorite victim.",
    "Too shiny to be trusted.",
    "Believes an apple a day keeps anyone away."
  ],
  watermelon: [
    "Thinks it's a bowling ball.",
    "92% water, 8% pure ego.",
    "Heavyweight champion of the fruit bowl.",
    "Too big for its own good."
  ],
  orange: [
    "Round and confident.",
    "Citrus with an attitude.",
    "Immune to scurvy, immune to opinions.",
    "Peeling good, living better."
  ],
  pineapple: [
    "Too fancy for this app.",
    "Wears a crown, refuses to pay taxes.",
    "Tropical royalty with trust issues.",
    "Prickly outside, sweet inside."
  ],
  mango: [
    "Main character energy.",
    "Sticky sweet perfectionist.",
    "Too dramatic for a regular lunchbox.",
    "King of fruits and knows it."
  ],
  lemon: [
    "Bitter about everything.",
    "Life gave it itself, still unhappy.",
    "Professional eye-winker.",
    "High acidity, zero tolerance."
  ],
  cucumber: [
    "Technically a fruit, acts like a vegetable.",
    "Cool as a cucumber, bored as a rock.",
    "Having an identity crisis in the salad."
  ],
  pear: [
    "Hourglass figure and proud of it.",
    "Slightly bottom-heavy philosopher.",
    "Always paired up, never alone."
  ],
  kiwi: [
    "Fuzzy on the outside, vibrant inside.",
    "Hairy mystery orb.",
    "Refuses to shave for anyone."
  ],
  strawberry: [
    "Cute but emotionally fragile.",
    "Seeds on the outside like a showoff.",
    "Dessert aristocracy."
  ]
};

// 2. Fruit Horoscope Predictions
const FRUIT_HOROSCOPES = [
  "Today's prediction: You will probably become a smoothie.",
  "Today's prediction: Beware of blenders and overly enthusiastic toddlers.",
  "Today's prediction: A dramatic fruit salad awaits in your near future.",
  "Today's prediction: Stars indicate you will be admired for 10 seconds before being sliced.",
  "Today's prediction: High chance of being left in the fridge until Friday.",
  "Today's prediction: Avoid sharp knives and Instagram food bloggers today.",
  "Today's prediction: Your potassium levels will bring good fortune."
];

// 4. Uselessness Score Explanations
const USELESS_EXPLANATIONS = [
  "Congratulations. You measured something nobody asked about.",
  "Zero peer-reviewed papers will cite this angle, but here we are.",
  "A triumph of technology over practical purpose.",
  "The computational effort exceeded all known usefulness.",
  "Somewhere in the world, a mathematician is crying tears of confusion."
];

// 6. Should I Eat It Responses
const EAT_IT_RESPONSES = [
  "YES.",
  "Absolutely.",
  "Why are you asking an app?",
  "Put it back in the fruit bowl.",
  "Consult the fruit first.",
  "The angle is acceptable. Proceed.",
  "Scientifically inconclusive. Deliciousness unknown."
];

// 10. Fruit Compatibility Statuses
const COMPATIBILITY_STATUSES = [
  "Probably a smoothie.",
  "Better as a fruit salad.",
  "Opposites attract.",
  "Scientifically questionable. Emotionally complicated.",
  "They belong in the same fruit bowl."
];

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewTray = document.getElementById('previewTray');
const previewGrid = document.getElementById('previewGrid');
const queuedCount = document.getElementById('queuedCount');
const clearQueueBtn = document.getElementById('clearQueueBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearAllBtn = document.getElementById('clearAllBtn');
const processingIndicator = document.getElementById('processingIndicator');
const processingText = document.getElementById('processingText');
const resultsGrid = document.getElementById('resultsGrid');
const emptyState = document.getElementById('emptyState');
const summaryBar = document.getElementById('summaryBar');
const multiFruitSection = document.getElementById('multiFruitSection');
const loadDemoBtn = document.getElementById('loadDemoBtn');

// Leaderboard & Compatibility DOM Elements
const lbMostTilted = document.getElementById('lbMostTilted');
const lbMostConfused = document.getElementById('lbMostConfused');
const lbMostDramatic = document.getElementById('lbMostDramatic');
const compatFruits = document.getElementById('compatFruits');
const compatScore = document.getElementById('compatScore');
const compatFill = document.getElementById('compatFill');
const compatStatus = document.getElementById('compatStatus');

// Modals
const whyModal = document.getElementById('whyModal');
const closeWhyModal = document.getElementById('closeWhyModal');
const whyDoneBtn = document.getElementById('whyDoneBtn');
const whyAngleText = document.getElementById('whyAngleText');

const certModal = document.getElementById('certModal');
const closeCertModal = document.getElementById('closeCertModal');
const dismissCertBtn = document.getElementById('dismissCertBtn');
const printCertBtn = document.getElementById('printCertBtn');
const certFruitName = document.getElementById('certFruitName');
const certFruitAngle = document.getElementById('certFruitAngle');
const certFruitType = document.getElementById('certFruitType');
const certAngleVal = document.getElementById('certAngleVal');
const certConfidence = document.getElementById('certConfidence');

// Filter Buttons
const btnViewAll = document.getElementById('btnViewAll');
const btnViewDetected = document.getElementById('btnViewDetected');
const btnViewUnconfident = document.getElementById('btnViewUnconfident');

// Stats counters
const statTotal = document.getElementById('statTotal');
const statDetected = document.getElementById('statDetected');
const statUnconfident = document.getElementById('statUnconfident');
const statAvgAngle = document.getElementById('statAvgAngle');
const countAll = document.getElementById('countAll');
const countDetected = document.getElementById('countDetected');
const countUnconfident = document.getElementById('countUnconfident');

// ============================================================================
// File Upload & Drag-and-Drop Handlers
// ============================================================================

browseBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  fileInput.click();
});

dropZone.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files && e.target.files.length > 0) {
    addFilesToQueue(Array.from(e.target.files));
    fileInput.value = '';
  }
});

['dragenter', 'dragover'].forEach((eventName) => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('drag-over');
  });
});

['dragleave', 'drop'].forEach((eventName) => {
  dropZone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('drag-over');
  });
});

dropZone.addEventListener('drop', (e) => {
  const dt = e.dataTransfer;
  if (dt && dt.files && dt.files.length > 0) {
    const validFiles = Array.from(dt.files).filter(f => f.type.startsWith('image/'));
    if (validFiles.length > 0) {
      addFilesToQueue(validFiles);
    }
  }
});

function addFilesToQueue(files) {
  files.forEach((file) => {
    const exists = queuedFiles.some(f => f.name === file.name && f.size === file.size);
    if (!exists) {
      queuedFiles.push(file);
    }
  });
  renderQueuePreview();
}

function renderQueuePreview() {
  if (queuedFiles.length === 0) {
    previewTray.classList.add('hidden');
    analyzeBtn.disabled = true;
    return;
  }

  previewTray.classList.remove('hidden');
  queuedCount.textContent = queuedFiles.length;
  analyzeBtn.disabled = false;
  previewGrid.innerHTML = '';

  queuedFiles.forEach((file, index) => {
    const thumbDiv = document.createElement('div');
    thumbDiv.className = 'preview-thumb';

    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.alt = file.name;

    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-thumb';
    removeBtn.innerHTML = '&times;';
    removeBtn.title = 'Remove from queue';
    removeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      removeQueuedFile(index);
    });

    const caption = document.createElement('div');
    caption.className = 'thumb-name';
    caption.textContent = file.name;

    thumbDiv.appendChild(img);
    thumbDiv.appendChild(removeBtn);
    thumbDiv.appendChild(caption);
    previewGrid.appendChild(thumbDiv);
  });
}

function removeQueuedFile(index) {
  queuedFiles.splice(index, 1);
  renderQueuePreview();
}

clearQueueBtn.addEventListener('click', () => {
  queuedFiles = [];
  renderQueuePreview();
});

// Clear All Button
clearAllBtn.addEventListener('click', () => {
  queuedFiles = [];
  allResults = [];
  renderQueuePreview();
  renderResults();
  updateSummaryStats();
  updateMultiFruitFeatures();
});

// ============================================================================
// Image Analysis Request with 8. Rotating Loading Messages
// ============================================================================

analyzeBtn.addEventListener('click', async () => {
  if (queuedFiles.length === 0) return;

  analyzeBtn.disabled = true;
  browseBtn.disabled = true;
  dropZone.style.pointerEvents = 'none';
  processingIndicator.classList.remove('hidden');

  // Start rotating funny loading messages
  let loadMsgIdx = 0;
  processingText.textContent = FUNNY_LOADING_MESSAGES[0];
  const loadInterval = setInterval(() => {
    loadMsgIdx = (loadMsgIdx + 1) % FUNNY_LOADING_MESSAGES.length;
    processingText.textContent = FUNNY_LOADING_MESSAGES[loadMsgIdx];
  }, 900);

  const formData = new FormData();
  queuedFiles.forEach((file) => {
    formData.append('files', file, file.name);
  });

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    const data = await response.json();
    if (data.results && Array.isArray(data.results)) {
      data.results.forEach((res) => {
        allResults.unshift(res);
      });

      queuedFiles = [];
      renderQueuePreview();
      renderResults();
      updateSummaryStats();
      updateMultiFruitFeatures();
    }
  } catch (error) {
    console.error('Analysis error:', error);
    alert(`Error analyzing images: ${error.message}.`);
  } finally {
    clearInterval(loadInterval);
    processingIndicator.classList.add('hidden');
    dropZone.style.pointerEvents = 'auto';
    browseBtn.disabled = false;
    if (queuedFiles.length > 0) {
      analyzeBtn.disabled = false;
    }
  }
});

// ============================================================================
// Helper Functions for Fun Features
// ============================================================================

// 1. Fruit Personality Generator
function getFruitPersonality(fruitName) {
  const key = (fruitName || '').toLowerCase().trim();
  const list = FRUIT_PERSONALITIES[key] || [
    "Quiet observer of the fruit bowl.",
    "Mysterious fruit with untold ambition.",
    "Living life one degree at a time."
  ];
  return list[Math.floor(Math.random() * list.length)];
}

// 2. Fruit Horoscope Generator
function getFruitHoroscope() {
  return FRUIT_HOROSCOPES[Math.floor(Math.random() * FRUIT_HOROSCOPES.length)];
}

// 3. Angle-Based Mood Generator (Uses REAL detected angle)
function getAngleMood(angle) {
  const absA = Math.abs(angle);
  if (absA <= 12) {
    return { mood: "I'm lying down. Don't disturb me. 😴", badge: "Horizontal Zen (0°)" };
  } else if (angle > 12 && angle <= 55) {
    return { mood: "I'm feeling diagonal today. 📐", badge: "Diagonal Vibes (+45°)" };
  } else if (angle < -12 && angle >= -55) {
    return { mood: "Questioning my life choices. 🙃", badge: "Existential Tilt (-45°)" };
  } else {
    return { mood: "Standing tall 💪", badge: "Vertical Power (90°)" };
  }
}

// 4. Uselessness Score & Explanation
function getUselessnessData() {
  return {
    score: "97%",
    scientific: "0.3%",
    entertainment: "100%",
    explanation: USELESS_EXPLANATIONS[Math.floor(Math.random() * USELESS_EXPLANATIONS.length)]
  };
}

// 5. Roast My Fruit Generator (Uses REAL fruit name and REAL angle)
function generateFruitRoast(fruitName, angle) {
  const formattedAngle = `${angle > 0 ? '+' : ''}${angle.toFixed(1)}°`;
  const roasts = [
    `Your ${fruitName} is at ${formattedAngle}. Even it doesn't know where it's going.`,
    `This ${fruitName} is tilted at ${formattedAngle} and has completely lost direction.`,
    `Standing at ${formattedAngle} like it has an interview tomorrow.`,
    `At ${formattedAngle}, this ${fruitName} is leaning harder than the Tower of Pisa.`,
    `At ${formattedAngle}, this ${fruitName} is about 2 degrees away from an existential crisis.`,
    `A bold ${formattedAngle} orientation for a ${fruitName} that clearly lacks spine.`
  ];
  return roasts[Math.floor(Math.random() * roasts.length)];
}

// 6. Should I Eat It Verdict
function getShouldIEatItAnswer() {
  return EAT_IT_RESPONSES[Math.floor(Math.random() * EAT_IT_RESPONSES.length)];
}

// ============================================================================
// Results Rendering & Card Generation
// ============================================================================

function renderResults() {
  resultsGrid.innerHTML = '';

  const filtered = allResults.filter((item) => {
    if (activeFilter === 'detected') return item.detected;
    if (activeFilter === 'unconfident') return !item.detected;
    return true;
  });

  if (allResults.length === 0) {
    emptyState.classList.remove('hidden');
    resultsGrid.appendChild(emptyState);
    summaryBar.classList.add('hidden');
    multiFruitSection.classList.add('hidden');
    return;
  }

  emptyState.classList.add('hidden');
  summaryBar.classList.remove('hidden');

  if (filtered.length === 0) {
    const noMatch = document.createElement('div');
    noMatch.className = 'empty-state card glass';
    noMatch.innerHTML = `
      <div class="empty-icon">🔍</div>
      <h3>No matching results</h3>
      <p>No images match the current filter "${activeFilter}".</p>
    `;
    resultsGrid.appendChild(noMatch);
    return;
  }

  filtered.forEach((item, index) => {
    const card = createResultCard(item, index);
    resultsGrid.appendChild(card);
  });
}

function createResultCard(item, index) {
  const card = document.createElement('div');
  card.className = 'result-card card glass';

  const fruitKey = (item.fruit_name || '').toLowerCase();
  const emoji = FRUIT_EMOJIS[fruitKey] || (item.detected ? '🍎' : '❓');
  const isDetected = item.detected;
  const angle = item.angle_deg || 0.0;
  const signStr = angle > 0 ? '+' : '';
  const needleRotation = -angle;

  const imgSrc = item.annotated_image || item.original_image || '';
  const originalSrc = item.original_image || '';
  const annotatedSrc = item.annotated_image || '';

  // Fun metadata
  const personality = getFruitPersonality(item.fruit_name);
  const horoscope = getFruitHoroscope();
  const moodData = getAngleMood(angle);
  const uselessData = getUselessnessData();

  card.innerHTML = `
    <div class="card-media">
      <img id="img_${index}" src="${imgSrc}" alt="${item.filename}" loading="lazy">
      
      ${originalSrc && annotatedSrc ? `
        <button type="button" class="media-toggle-btn" id="toggle_${index}" data-mode="annotated">
          👁️ View Original
        </button>
      ` : ''}

      <div class="media-status-badge ${isDetected ? 'status-detected' : 'status-unconfident'}">
        ${isDetected ? '✓ Fruit Detected' : '⚠ Unconfident'}
      </div>
    </div>

    <div class="card-body">
      <div class="card-title-row">
        <div class="fruit-name-group">
          <span class="fruit-emoji">${emoji}</span>
          <span class="fruit-name">${escapeHtml(item.fruit_name)}</span>
        </div>
        <span class="filename-caption" title="${escapeHtml(item.filename)}">${escapeHtml(item.filename)}</span>
      </div>

      <!-- Orientation & Angle Gauge Dashboard -->
      <div class="angle-dashboard">
        <div class="gauge-visual">
          <div class="compass-dial" title="Fruit Major Orientation Axis (0° = Horizontal Right)">
            <div class="compass-baseline"></div>
            <div class="compass-needle" style="transform: rotate(${needleRotation}deg);"></div>
            <div class="compass-center"></div>
          </div>
          <div class="angle-metric">
            <span class="angle-number">${signStr}${angle.toFixed(1)}°</span>
            <span class="angle-caption">Orientation Angle</span>
          </div>
        </div>
        <div class="angle-axis-info">
          <!-- 3. Angle-Based Mood -->
          <div class="mood-badge" title="Mood computed from actual angle">
            <span>${moodData.mood}</span>
          </div>
        </div>
      </div>

      ${isDetected ? `
        <!-- 1. Fruit Personality -->
        <div class="personality-row">
          <span class="personality-label">Personality:</span>
          <span class="personality-text">“${personality}”</span>
        </div>

        <!-- 2. Fruit Horoscope -->
        <div class="horoscope-box">
          <span class="horoscope-tag">🔮 Horoscope:</span>
          <span>${horoscope}</span>
        </div>

        <!-- 4. Uselessness Score -->
        <div class="useless-box">
          <div class="useless-header">
            <span class="useless-title">💀 Uselessness Score</span>
            <span class="useless-score-val">${uselessData.score}</span>
          </div>
          <div class="useless-breakdown">
            <span>Scientific importance: <strong>${uselessData.scientific}</strong></span>
            <span>Entertainment value: <strong>${uselessData.entertainment}</strong></span>
          </div>
          <p class="useless-quote">“${uselessData.explanation}”</p>
        </div>

        <!-- Fun Interactive Buttons: Roast, Eat It, Why, Certificate -->
        <div class="fun-actions-grid">
          <button type="button" class="btn-fun btn-roast" id="roastBtn_${index}">
            <span>🔥 Roast My Fruit</span>
          </button>
          <button type="button" class="btn-fun btn-eat" id="eatBtn_${index}">
            <span>🍴 Should I Eat It?</span>
          </button>
          <button type="button" class="btn-fun btn-why" id="whyBtn_${index}">
            <span>❓ WHY?</span>
          </button>
          <button type="button" class="btn-fun btn-cert" id="certBtn_${index}">
            <span>🏆 Certificate</span>
          </button>
        </div>

        <!-- Dynamic popover target for Roast & Eat-it verdicts -->
        <div id="popoverArea_${index}" class="hidden"></div>
      ` : ''}

      <!-- Confidence Bar -->
      <div class="confidence-container">
        <div class="confidence-labels">
          <span>Detection Confidence</span>
          <span><strong>${item.confidence || 0}%</strong></span>
        </div>
        <div class="progress-track">
          <div class="progress-fill ${item.confidence < 40 ? 'low-conf' : ''}" style="width: ${Math.min(100, item.confidence || 0)}%;"></div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card-footer">
        ${annotatedSrc ? `
          <a class="download-link" href="${annotatedSrc}" download="detected_${item.filename || 'fruit.jpg'}">
            <span>💾 Download Image</span>
          </a>
        ` : '<span></span>'}
        <span class="status-message" style="font-size: 11px; color: var(--text-muted);">
          ${isDetected ? 'Major Axis via PCA' : 'Fruit not confidently detected'}
        </span>
      </div>
    </div>
  `;

  // Attach toggle listener for viewing original vs annotated
  if (originalSrc && annotatedSrc) {
    const toggleBtn = card.querySelector(`#toggle_${index}`);
    const cardImg = card.querySelector(`#img_${index}`);

    toggleBtn.addEventListener('click', () => {
      const currentMode = toggleBtn.getAttribute('data-mode');
      if (currentMode === 'annotated') {
        cardImg.src = originalSrc;
        toggleBtn.setAttribute('data-mode', 'original');
        toggleBtn.textContent = '📐 View Orientation';
      } else {
        cardImg.src = annotatedSrc;
        toggleBtn.setAttribute('data-mode', 'annotated');
        toggleBtn.textContent = '👁️ View Original';
      }
    });
  }

  // Attach Fun Action Listeners if fruit was detected
  if (isDetected) {
    const popoverArea = card.querySelector(`#popoverArea_${index}`);

    // 5. Roast My Fruit
    const roastBtn = card.querySelector(`#roastBtn_${index}`);
    roastBtn.addEventListener('click', () => {
      const roast = generateFruitRoast(item.fruit_name, angle);
      popoverArea.className = 'bubble-popover';
      popoverArea.innerHTML = `<strong>🔥 Fruit Roast:</strong> ${escapeHtml(roast)}`;
    });

    // 6. Should I Eat It?
    const eatBtn = card.querySelector(`#eatBtn_${index}`);
    eatBtn.addEventListener('click', () => {
      const verdict = getShouldIEatItAnswer();
      popoverArea.className = 'bubble-popover';
      popoverArea.innerHTML = `<strong>🍴 Kitchen Oracle:</strong> “${escapeHtml(verdict)}”`;
    });

    // 7. WHY? Dramatic Popup
    const whyBtn = card.querySelector(`#whyBtn_${index}`);
    whyBtn.addEventListener('click', () => {
      openWhyModal(angle);
    });

    // 9. Generate Fruit Certificate
    const certBtn = card.querySelector(`#certBtn_${index}`);
    certBtn.addEventListener('click', () => {
      openCertificateModal(item);
    });
  }

  return card;
}

// 7. Open WHY Modal with dramatic sequential reveal
function openWhyModal(angle) {
  const formatted = `${angle > 0 ? '+' : ''}${angle.toFixed(1)}°`;
  whyAngleText.textContent = formatted;
  whyModal.classList.remove('hidden');
}

closeWhyModal.addEventListener('click', () => whyModal.classList.add('hidden'));
whyDoneBtn.addEventListener('click', () => whyModal.classList.add('hidden'));
whyModal.addEventListener('click', (e) => {
  if (e.target === whyModal) whyModal.classList.add('hidden');
});

// 9. Open Certificate Modal
function openCertificateModal(item) {
  const angleStr = `${item.angle_deg > 0 ? '+' : ''}${item.angle_deg.toFixed(1)}°`;
  certFruitName.textContent = item.fruit_name;
  certFruitAngle.textContent = angleStr;
  certFruitType.textContent = item.fruit_name;
  certAngleVal.textContent = angleStr;
  certConfidence.textContent = `${item.confidence}%`;

  certModal.classList.remove('hidden');
}

closeCertModal.addEventListener('click', () => certModal.classList.add('hidden'));
dismissCertBtn.addEventListener('click', () => certModal.classList.add('hidden'));
certModal.addEventListener('click', (e) => {
  if (e.target === certModal) certModal.classList.add('hidden');
});
printCertBtn.addEventListener('click', () => {
  window.print();
});

// 10 & 11. Fruit Compatibility & Useless Leaderboard for Multi-Fruit Batches
function updateMultiFruitFeatures() {
  const detectedList = allResults.filter(r => r.detected);

  if (detectedList.length < 2) {
    multiFruitSection.classList.add('hidden');
    return;
  }

  multiFruitSection.classList.remove('hidden');

  // 11. Useless Leaderboard
  // Most tilted fruit: largest |angle|
  const mostTilted = [...detectedList].sort((a, b) => Math.abs(b.angle_deg) - Math.abs(a.angle_deg))[0];
  const mostTiltedSign = mostTilted.angle_deg > 0 ? '+' : '';
  lbMostTilted.textContent = `${mostTilted.fruit_name} (${mostTiltedSign}${mostTilted.angle_deg.toFixed(1)}°)`;

  // Most confused fruit: fruit closest to diagonal 37.4° or -42.1°
  const mostConfused = [...detectedList].sort((a, b) => {
    const diffA = Math.min(Math.abs(Math.abs(a.angle_deg) - 37.4), Math.abs(Math.abs(a.angle_deg) - 42.1));
    const diffB = Math.min(Math.abs(Math.abs(b.angle_deg) - 37.4), Math.abs(Math.abs(b.angle_deg) - 42.1));
    return diffA - diffB;
  })[0];
  const confusedSign = mostConfused.angle_deg > 0 ? '+' : '';
  lbMostConfused.textContent = `${mostConfused.fruit_name} (${confusedSign}${mostConfused.angle_deg.toFixed(1)}°)`;

  // Most dramatic fruit: random fruit from detected
  const dramaticFruit = detectedList[Math.floor(Math.random() * detectedList.length)];
  lbMostDramatic.textContent = `${dramaticFruit.fruit_name} (100% Drama)`;

  // 10. Fruit Compatibility Match
  const fruitA = detectedList[0];
  const fruitB = detectedList[1];
  compatFruits.textContent = `${FRUIT_EMOJIS[fruitA.fruit_name.toLowerCase()] || '🍎'} ${fruitA.fruit_name} + ${FRUIT_EMOJIS[fruitB.fruit_name.toLowerCase()] || '🍌'} ${fruitB.fruit_name}`;

  // Compatibility score based on fruit angles and names
  const score = Math.min(99, Math.max(62, Math.floor(75 + (fruitA.angle_deg - fruitB.angle_deg) * 0.3) % 100));
  compatScore.textContent = `${score}%`;
  compatFill.style.width = `${score}%`;

  const status = COMPATIBILITY_STATUSES[Math.floor(Math.random() * COMPATIBILITY_STATUSES.length)];
  compatStatus.textContent = `“${status}”`;
}

// Update summary metrics
function updateSummaryStats() {
  const total = allResults.length;
  const detected = allResults.filter(r => r.detected).length;
  const unconfident = total - detected;

  statTotal.textContent = total;
  statDetected.textContent = detected;
  statUnconfident.textContent = unconfident;

  countAll.textContent = total;
  countDetected.textContent = detected;
  countUnconfident.textContent = unconfident;

  if (detected > 0) {
    const sumAngles = allResults
      .filter(r => r.detected)
      .reduce((acc, curr) => acc + Math.abs(curr.angle_deg || 0), 0);
    const avg = sumAngles / detected;
    statAvgAngle.textContent = `${avg.toFixed(1)}°`;
  } else {
    statAvgAngle.textContent = '0.0°';
  }
}

// Filter Handlers
[btnViewAll, btnViewDetected, btnViewUnconfident].forEach((btn) => {
  btn.addEventListener('click', (e) => {
    [btnViewAll, btnViewDetected, btnViewUnconfident].forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    if (btn === btnViewDetected) activeFilter = 'detected';
    else if (btn === btnViewUnconfident) activeFilter = 'unconfident';
    else activeFilter = 'all';

    renderResults();
  });
});

// Demo Images Generator / Quick Loader
loadDemoBtn.addEventListener('click', async () => {
  loadDemoBtn.disabled = true;
  loadDemoBtn.innerHTML = '<span>⏳ Creating Demo Fruits...</span>';

  try {
    const demoFiles = await Promise.all([
      createSyntheticFruitFile('demo_banana_35deg.jpg', 'banana', 35),
      createSyntheticFruitFile('demo_apple_tilt.jpg', 'apple', -25),
      createSyntheticFruitFile('demo_orange_15deg.jpg', 'orange', 15),
      createSyntheticFruitFile('demo_cucumber_60deg.jpg', 'cucumber', 60)
    ]);

    addFilesToQueue(demoFiles);
  } catch (err) {
    console.error('Demo loading failed:', err);
  } finally {
    loadDemoBtn.disabled = false;
    loadDemoBtn.innerHTML = '<span>✨ Load Demo Images</span>';
  }
});

function createSyntheticFruitFile(filename, fruitType, angleDeg) {
  return new Promise((resolve) => {
    const canvas = document.createElement('canvas');
    canvas.width = 480;
    canvas.height = 480;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#f1f5f9';
    ctx.fillRect(0, 0, 480, 480);

    const grad = ctx.createRadialGradient(240, 240, 80, 240, 240, 260);
    grad.addColorStop(0, '#ffffff');
    grad.addColorStop(1, '#e2e8f0');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 480, 480);

    ctx.save();
    ctx.translate(240, 240);
    ctx.rotate((-angleDeg * Math.PI) / 180);

    if (fruitType === 'banana') {
      ctx.beginPath();
      ctx.moveTo(-130, -20);
      ctx.bezierCurveTo(-60, 90, 60, 90, 130, -10);
      ctx.bezierCurveTo(70, 50, -50, 50, -130, -20);
      ctx.fillStyle = '#facc15';
      ctx.fill();
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#ca8a04';
      ctx.stroke();

      ctx.fillStyle = '#713f12';
      ctx.fillRect(130, -14, 10, 8);
      ctx.fillRect(-138, -22, 10, 6);
    } else if (fruitType === 'apple') {
      ctx.beginPath();
      ctx.arc(-25, 0, 75, 0, Math.PI * 2);
      ctx.arc(25, 0, 75, 0, Math.PI * 2);
      ctx.fillStyle = '#ef4444';
      ctx.fill();
      ctx.fillStyle = '#78350f';
      ctx.fillRect(-4, -90, 8, 25);
    } else if (fruitType === 'orange') {
      ctx.beginPath();
      ctx.arc(0, 0, 80, 0, Math.PI * 2);
      ctx.fillStyle = '#f97316';
      ctx.fill();
      ctx.fillStyle = '#c2410c';
      ctx.beginPath();
      ctx.arc(0, -78, 5, 0, Math.PI * 2);
      ctx.fill();
    } else if (fruitType === 'cucumber') {
      ctx.beginPath();
      ctx.ellipse(0, 0, 140, 32, 0, 0, Math.PI * 2);
      ctx.fillStyle = '#15803d';
      ctx.fill();
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#166534';
      ctx.stroke();
    }

    ctx.restore();

    canvas.toBlob((blob) => {
      const file = new File([blob], filename, { type: 'image/jpeg' });
      resolve(file);
    }, 'image/jpeg', 0.95);
  });
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
