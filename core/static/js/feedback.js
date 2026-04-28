const dragDrop = document.getElementById('dragDrop');
const photoInput = document.getElementById('photoInput');
const previewContainer = document.getElementById('previewContainer');
const preview = document.getElementById('preview');
const feedbackResult = document.getElementById('feedbackResult');
const historyContainer = document.getElementById('historyContainer');

let feedbackData = JSON.parse(localStorage.getItem('feedbackData')) || [];
let currentImage = null;

dragDrop.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragDrop.classList.add('dragover');
});

dragDrop.addEventListener('dragleave', () => {
    dragDrop.classList.remove('dragover');
});

dragDrop.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDrop.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

photoInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFile(e.target.files[0]);
});

function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        currentImage = e.target.result;
        preview.src = currentImage;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function analyzeOutfit() {
    const mockFeedback = {
        mistakes: [
            "❌ Color clash between top and shoes",
            "❌ Over-accessorized for casual occasion",
            "❌ Too tight for body type"
        ],
        improvements: [
            "✅ Swap shoes for neutral tone",
            "✅ Remove 2-3 accessories",
            "✅ Try a size up for comfort"
        ],
        improvedLook: "Clean, elegant, and perfectly balanced look suitable for any occasion!"
    };

    feedbackResult.innerHTML = `
        <div class="feedback-card">
            <h3>Mistakes Found:</h3>
            <ul>${mockFeedback.mistakes.map(m => `<li>${m}</li>`).join('')}</ul>
        </div>
        <div class="feedback-card">
            <h3>Improvements:</h3>
            <ul>${mockFeedback.improvements.map(i => `<li>${i}</li>`).join('')}</ul>
        </div>
        <div class="feedback-card">
            <h3>Improved Look:</h3>
            <p>${mockFeedback.improvedLook}</p>
            <button onclick="saveFeedback()" style="width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; margin-top: 10px;">Save Feedback</button>
        </div>
    `;
}

function saveFeedback() {
    const item = {
        id: Date.now(),
        image: currentImage,
        date: new Date().toLocaleDateString(),
        feedback: feedbackResult.innerHTML
    };
    feedbackData.push(item);
    localStorage.setItem('feedbackData', JSON.stringify(feedbackData));
    alert('✅ Feedback saved!');
    feedbackResult.innerHTML = '';
    previewContainer.style.display = 'none';
    renderHistory();
}

function deleteFeedback(id) {
    feedbackData = feedbackData.filter(item => item.id !== id);
    localStorage.setItem('feedbackData', JSON.stringify(feedbackData));
    renderHistory();
}

function renderHistory() {
    historyContainer.innerHTML = feedbackData.length === 0
        ? '<div class="empty-state">No feedback history yet!</div>'
        : feedbackData.map(item => `
            <div class="history-item">
                <img src="${item.image}" class="history-img" alt="Feedback">
                <div class="history-info">
                    <p><strong>Date:</strong> ${item.date}</p>
                    <button class="delete-feedback" onclick="deleteFeedback(${item.id})">Delete</button>
                </div>
            </div>
        `).join('');
}

function switchTab(tab) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    event.target.classList.add('active');
    if (tab === 'history') renderHistory();
}

renderHistory();