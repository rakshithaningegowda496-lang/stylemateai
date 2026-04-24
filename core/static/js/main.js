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