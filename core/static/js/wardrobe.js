const addItemForm = document.getElementById('addItemForm');
const wardrobeGrid = document.getElementById('wardrobeGrid');
const gapAnalysis = document.getElementById('gapAnalysis');

let wardrobe = JSON.parse(localStorage.getItem('wardrobe')) || [];

addItemForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const item = {
        id: Date.now(),
        name: document.getElementById('itemName').value,
        color: document.getElementById('itemColor').value,
        type: document.getElementById('itemType').value,
        style: document.getElementById('itemStyle').value
    };
    wardrobe.push(item);
    localStorage.setItem('wardrobe', JSON.stringify(wardrobe));
    addItemForm.reset();
    render();
});

function deleteItem(id) {
    wardrobe = wardrobe.filter(item => item.id !== id);
    localStorage.setItem('wardrobe', JSON.stringify(wardrobe));
    render();
}

function updateInsights() {
    const types = { top: 0, bottom: 0, shoes: 0, accessory: 0 };
    wardrobe.forEach(item => types[item.type]++);
    
    document.getElementById('totalItems').textContent = wardrobe.length;
    document.getElementById('topCount').textContent = types.top;
    document.getElementById('bottomCount').textContent = types.bottom;
    document.getElementById('shoeCount').textContent = types.shoes;
    
    let gaps = [];
    if (types.bottom < 2) gaps.push('⚠️ You need more bottoms');
    if (types.shoes < 2) gaps.push('⚠️ Add more shoes');
    if (types.accessory < 1) gaps.push('⚠️ Add accessories to complete looks');
    
    gapAnalysis.innerHTML = gaps.length ? gaps.join('<br>') : '✅ Great wardrobe balance!';
}

function render() {
    wardrobeGrid.innerHTML = wardrobe.length === 0 
        ? '<div class="empty-state">No items yet. Add your first item!</div>'
        : wardrobe.map(item => `
            <div class="wardrobe-item">
                <div class="color-preview" style="background-color: ${item.color}"></div>
                <div class="item-details">
                    <h3>${item.name}</h3>
                    <div class="item-info">
                        <span class="item-badge">${item.type}</span>
                        <span class="item-badge">${item.style}</span>
                    </div>
                    <button class="delete-btn" onclick="deleteItem(${item.id})">Delete</button>
                </div>
            </div>
        `).join('');
    updateInsights();
}

render();