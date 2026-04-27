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

const SKIN_TONE_COLORS = {
  "fair":      { label: "Fair",      colors: ["Soft Pink", "Lavender", "Powder Blue", "Mint", "Champagne"] },
  "light":     { label: "Light",     colors: ["Peach", "Blush", "Sky Blue", "Sage", "Ivory"] },
  "medium":    { label: "Medium",    colors: ["Earth Tones", "Olive", "Gold", "Mustard", "Navy"] },
  "wheatish":  { label: "Wheatish",  colors: ["Warm Beige", "Caramel", "Burnt Sienna", "Olive", "Gold"] },
  "tan":       { label: "Tan",       colors: ["Terracotta", "Burnt Orange", "Coral", "Teal", "Warm Brown"] },
  "deep":      { label: "Deep",      colors: ["Jewel Tones", "Emerald", "Cobalt", "Plum", "Rich Red"] },
  "dark":      { label: "Dark",      colors: ["Bright White", "Electric Blue", "Fuchsia", "Orange", "Gold"] },
};

const PROFESSION_STYLE = {
  "Student":      "casual, youthful, comfortable, budget-friendly",
  "Professor":    "smart-casual, academic, polished, blazer-friendly",
  "IT Employee":  "business-casual, functional, modern, tech-smart",
  "Model":        "high-fashion, editorial, bold, avant-garde",
  "Doctor":       "clean, professional, minimal, practical",
  "Artist":       "creative, eclectic, expressive, artsy",
  "Entrepreneur": "sharp, power-dressing, confident, sleek",
  "Athlete":      "sporty, performance-wear, athleisure, dynamic",
};

const OCCASION_EMOJI = {
  casual: "👕", formal: "🤵", party: "🪩", office: "👔", date: "✨"
};

let profileData   = {};
let selectedProfession = null;
let colorMode     = "ai";

// ── Load profile on page load ─────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/api/profile/");
    if (res.ok) {
      profileData = await res.json();
      applyProfileColors();
    }
  } catch (e) {
    console.warn("Could not load profile:", e);
    applyProfileColors(); // fallback to medium
  }
  setupProfessionPills();
});

// ── Render color tag buttons from skin tone ───────────────────────────────────
function applyProfileColors() {
  const tone   = (profileData.skin_tone || "medium").toLowerCase().trim();
  const entry  = SKIN_TONE_COLORS[tone] || SKIN_TONE_COLORS["medium"];
  const colors = entry.colors;
  const label  = entry.label;

  // Update labels
  document.getElementById("skin-tone-label").textContent =
    `Suggested for your ${label} skin tone:`;
  document.getElementById("ai-card-sub").textContent =
    `Based on ${label} skin tone`;

  // Render selectable color buttons — all selected by default
  const container = document.getElementById("color-tags");
  container.innerHTML = colors.map(c => `
    <button class="color-tag selected" data-color="${c}" onclick="toggleColorTag(this)">
      <span class="color-swatch" style="background:${colorNameToHex(c)}"></span>
      ${c}
    </button>
  `).join("");
}

// ── Toggle individual color tag ───────────────────────────────────────────────
function toggleColorTag(el) {
  el.classList.toggle("selected");
  // ensure at least 1 always selected
  const allSelected = document.querySelectorAll(".color-tag.selected");
  if (allSelected.length === 0) el.classList.add("selected");
}

// ── Color name → approximate hex (for swatches) ───────────────────────────────
function colorNameToHex(name) {
  const map = {
    "Earth Tones":"#a0785a", "Olive":"#808000",      "Gold":"#ffd700",
    "Mustard":"#e1ad01",     "Navy":"#001f5b",        "Soft Pink":"#ffb6c1",
    "Lavender":"#e6e6fa",    "Powder Blue":"#b0e0e6", "Mint":"#98ff98",
    "Champagne":"#f7e7ce",   "Peach":"#ffcba4",       "Blush":"#de5d83",
    "Sky Blue":"#87ceeb",    "Sage":"#bcb88a",        "Ivory":"#fffff0",
    "Warm Beige":"#c9a882",  "Caramel":"#c68642",     "Burnt Sienna":"#e97451",
    "Terracotta":"#e2725b",  "Burnt Orange":"#cc5500","Coral":"#ff7f50",
    "Teal":"#008080",        "Warm Brown":"#964b00",  "Jewel Tones":"#4b0082",
    "Emerald":"#50c878",     "Cobalt":"#0047ab",      "Plum":"#dda0dd",
    "Rich Red":"#c41e3a",    "Bright White":"#f5f5f5","Electric Blue":"#7df9ff",
    "Fuchsia":"#ff00ff",     "Orange":"#ffa500",
  };
  return map[name] || "#8b6cef";
}

// ── Color mode switch ─────────────────────────────────────────────────────────
function selectColorMode(mode) {
  colorMode = mode;
  document.getElementById("ai-recommended").classList.toggle("active", mode === "ai");
  document.getElementById("custom-color").classList.toggle("active", mode === "custom");
  document.getElementById("ai-color-section").style.display    = mode === "ai"     ? "" : "none";
  document.getElementById("custom-color-section").style.display = mode === "custom" ? "" : "none";
}

// ── Profession pills ──────────────────────────────────────────────────────────
function setupProfessionPills() {
  document.querySelectorAll("#profession-group .pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll("#profession-group .pill")
              .forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      selectedProfession = pill.dataset.val;
      document.getElementById("profession-hint").textContent =
        `Style: ${PROFESSION_STYLE[selectedProfession] || "versatile"}`;
    });
  });
}

// ── Get selected colors ───────────────────────────────────────────────────────
function getSelectedColors() {
  if (colorMode === "custom") {
    return document.getElementById("custom-color-input").value.trim() || "neutral tones";
  }
  return [...document.querySelectorAll(".color-tag.selected")]
    .map(el => el.dataset.color).join(", ");
}

// ── Generate outfits ──────────────────────────────────────────────────────────
async function generateOutfits() {
  if (!selectedProfession) {
    alert("Please select your profession first.");
    return;
  }

  const occasion  = document.getElementById("occasion").value;
  const mood      = document.getElementById("mood").value;
  const colors    = getSelectedColors();
  const profStyle = PROFESSION_STYLE[selectedProfession] || "versatile";
  const skinTone  = profileData.skin_tone || "medium";

  document.getElementById("preview-placeholder").style.display = "none";
  document.getElementById("spinner").style.display             = "block";
  document.getElementById("outfit-grid").style.display         = "none";

  const prompt = `
You are a professional fashion stylist AI.
Generate exactly 3 outfit suggestions for:
- Occasion: ${occasion}
- Profession: ${selectedProfession} (style: ${profStyle})
- Mood: ${mood}
- Skin tone: ${skinTone}
- Preferred colors: ${colors}

Respond ONLY with a JSON array, no markdown, no extra text:
[
  {
    "name": "Outfit name",
    "description": "Short 1-line description",
    "pieces": ["Top", "Bottom", "Footwear", "Accessory"],
    "colors": ["color1", "color2"]
  }
]`;

  try {
    const res  = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{ role: "user", content: prompt }]
      })
    });
    const data    = await res.json();
    const raw     = data.content.map(b => b.text || "").join("");
    const clean   = raw.replace(/```json|```/g, "").trim();
    const outfits = JSON.parse(clean);
    renderOutfits(outfits, occasion);
  } catch (err) {
    console.error(err);
    document.getElementById("outfit-grid").innerHTML =
      `<p style="color:red;padding:1rem;">Failed to generate outfits. Please try again.</p>`;
    document.getElementById("outfit-grid").style.display = "block";
  } finally {
    document.getElementById("spinner").style.display = "none";
  }
}

// ── Render outfit cards ───────────────────────────────────────────────────────
function renderOutfits(outfits, occasion) {
  const emoji = OCCASION_EMOJI[occasion] || "👗";
  const grid  = document.getElementById("outfit-grid");
  grid.innerHTML = outfits.map(o => `
    <div class="outfit-card">
      <div class="outfit-img">${emoji}</div>
      <div class="outfit-info">
        <div class="outfit-name">${o.name}</div>
        <div class="outfit-desc">${o.description}</div>
        <ul class="outfit-pieces">
          ${o.pieces.map(p => `<li>${p}</li>`).join("")}
        </ul>
        <div class="outfit-color-dots">
          ${o.colors.map(c =>
            `<span class="color-dot" style="background:${colorNameToHex(c)}" title="${c}"></span>`
          ).join("")}
        </div>
      </div>
    </div>
  `).join("");
  grid.style.display = "grid";
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