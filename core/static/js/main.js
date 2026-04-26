const API = "http://127.0.0.1:8000/api/profile/";

// Load profile
async function loadProfile() {
  const res = await fetch(API);
  const data = await res.json();

  document.getElementById("username").innerText = data.name;
  document.getElementById("location").innerText = "📍 " + data.location;

  document.getElementById("skin_tone").value = data.skin_tone;
  document.getElementById("skin_type").value = data.skin_type;
  document.getElementById("body_type").value = data.body_type;
  document.getElementById("gender").value = data.gender;
  document.getElementById("user_location").value = data.location;
}

// Save profile
async function saveProfile() {
  const data = {
    skin_tone: document.getElementById("skin_tone").value,
    skin_type: document.getElementById("skin_type").value,
    body_type: document.getElementById("body_type").value,
    gender: document.getElementById("gender").value,
    location: document.getElementById("user_location").value
  };

  await fetch(API, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  document.getElementById("statusMsg").innerText = "✔ Profile updated!";
}

loadProfile();
// ── ACTIVE NAV LINK (auto-detects current page) ──
(function () {
  const currentFile = window.location.pathname.split('/').pop() || 'home.html';
  document.querySelectorAll('.nav-links a[data-page]').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentFile) {
      link.classList.add('active');
    }
  });
})();
 
// ── PILL TOGGLE ──
document.querySelectorAll('.pill-group').forEach(group => {
  group.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', () => {
      group.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    });
  });
});
 
// ── COLOR PREFERENCE TOGGLE ──
const aiCard = document.getElementById('ai-recommended');
const customCard = document.getElementById('custom-color');
 
if (aiCard && customCard) {
  [aiCard, customCard].forEach(card => {
    card.addEventListener('click', () => {
      aiCard.classList.remove('active');
      customCard.classList.remove('active');
      card.classList.add('active');
    });
  });
}
 
// ── GENERATE OUTFITS ──
const genBtn      = document.getElementById('gen-btn');
const spinner     = document.getElementById('spinner');
const outfitGrid  = document.getElementById('outfit-grid');
const previewPanel = document.getElementById('preview-panel');
 
if (genBtn) {
  genBtn.addEventListener('click', () => {
    previewPanel.querySelector('h2').style.display           = 'none';
    previewPanel.querySelector('p').style.display            = 'none';
    previewPanel.querySelector('.preview-icon').style.display = 'none';
    outfitGrid.style.display = 'none';
    spinner.style.display    = 'block';
 
    setTimeout(() => {
      spinner.style.display   = 'none';
      outfitGrid.style.display = 'grid';
    }, 1800);
  });
}