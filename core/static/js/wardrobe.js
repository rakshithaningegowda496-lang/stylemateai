/* ============================================================
   wardrobe.js — StyleMate AI
   API URLs matched to style/urls.py:
     POST   /api/wardrobe/                    → wardrobe_api
     DELETE /api/wardrobe/<id>/delete/        → wardrobe_delete_api
   ============================================================ */
 
"use strict";
 
/* ── SELECTORS ── */
const openModalBtn     = document.getElementById("openModalBtn");
const closeModalBtn    = document.getElementById("closeModalBtn");
const itemModal        = document.getElementById("itemModal");
const addItemForm      = document.getElementById("addItemForm");
const submitBtn        = document.getElementById("submitBtn");
 
const uploadZone       = document.getElementById("uploadZone");
const imageInput       = document.getElementById("itemImage");
const imagePreviewWrap = document.getElementById("imagePreviewWrap");
const imagePreview     = document.getElementById("imagePreview");
const removePreview    = document.getElementById("removePreview");
 
const deleteModal      = document.getElementById("deleteModal");
const cancelDelete     = document.getElementById("cancelDelete");
const confirmDelete    = document.getElementById("confirmDelete");
 
const filterBtns       = document.querySelectorAll(".filter-btn");
const categorySections = document.querySelectorAll(".category-section");
 
const toast            = document.getElementById("toast");
 
/* ── CSRF TOKEN ── */
function getCsrfToken() {
    const cookie = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="));
    return cookie ? cookie.split("=")[1] : "";
}
 
/* ── TOAST ── */
function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}
 
/* ── MODAL OPEN / CLOSE ── */
function openModal(modal) {
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
}
 
function closeModal(modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "";
}
 
openModalBtn.addEventListener("click", () => openModal(itemModal));
closeModalBtn.addEventListener("click", () => closeModal(itemModal));
itemModal.addEventListener("click", (e) => {
    if (e.target === itemModal) closeModal(itemModal);
});
 
/* ── IMAGE PREVIEW ── */
function loadPreview(file) {
    if (!file || !file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadZone.classList.add("hidden");
        imagePreviewWrap.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
}
 
imageInput.addEventListener("change", (e) => {
    if (e.target.files[0]) loadPreview(e.target.files[0]);
});
 
removePreview.addEventListener("click", () => {
    imageInput.value = "";
    imagePreview.src = "";
    imagePreviewWrap.classList.add("hidden");
    uploadZone.classList.remove("hidden");
});
 
/* ── DRAG & DROP ── */
uploadZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
});
 
["dragleave", "dragend"].forEach(evt =>
    uploadZone.addEventListener(evt, () => uploadZone.classList.remove("dragover"))
);
 
uploadZone.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) {
        const dt = new DataTransfer();
        dt.items.add(file);
        imageInput.files = dt.files;
        loadPreview(file);
    }
});
 
/* ── CATEGORY CONFIG ── */
const categoryIcons = {
    tops:        "fa-shirt",
    bottoms:     "fa-person",
    footwear:    "fa-shoe-prints",
    accessories: "fa-gem",
    outerwear:   "fa-vest",
    dresses:     "fa-dress",
};
 
const categoryLabels = {
    tops:        "Tops",
    bottoms:     "Bottoms",
    footwear:    "Footwear",
    accessories: "Accessories",
    outerwear:   "Outerwear",
    dresses:     "Dresses",
};
 
/* ── ESCAPE HTML ── */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
 
/* ── BUILD CARD HTML ── */
function buildCard(item) {
    return `
    <div class="card" data-id="${item.id}" data-category="${escapeHtml(item.category)}">
        <div class="card-image">
            <img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.name)}" loading="lazy" />
            <button class="delete-btn" data-id="${item.id}">
                <i class="fa-solid fa-trash"></i>
            </button>
            <div class="card-badge">${escapeHtml(item.category.toUpperCase())}</div>
        </div>
        <div class="card-content">
            <div class="top-row">
                <span>${escapeHtml(item.category.toUpperCase())}</span>
                <span>${escapeHtml(item.style_type.toUpperCase())}</span>
            </div>
            <h3>${escapeHtml(item.name)}</h3>
            <div class="color-row">
                <div class="color-dot" style="background:${escapeHtml(item.color_hex || '#888')}"></div>
                <p>${escapeHtml(item.color_name)}</p>
            </div>
        </div>
    </div>`;
}
 
/* ── UPDATE ITEM COUNT BADGE ── */
function updateCount(category) {
    const section = document.querySelector(`.category-section[data-category="${category}"]`);
    if (!section) return;
    const count = section.querySelectorAll(".card").length;
    const badge = section.querySelector(".item-count");
    if (badge) badge.textContent = `${count} item${count !== 1 ? "s" : ""}`;
 
    const activeFilter = document.querySelector(".filter-btn.active")?.dataset.category;
    if (count === 0 && activeFilter !== "all" && activeFilter !== category) {
        section.classList.add("hidden");
    }
}
 
/* ── ADD CARD TO CORRECT CATEGORY GRID ── */
function addCardToDOM(item) {
    const gridId = `grid-${item.category}`;
    let grid = document.getElementById(gridId);
 
    // Create section dynamically if it doesn't exist yet
    if (!grid) {
        const container = document.getElementById("wardrobeContainer");
        const section = document.createElement("section");
        section.className = "category-section";
        section.dataset.category = item.category;
        section.innerHTML = `
            <div class="category-header">
                <i class="fa-solid ${categoryIcons[item.category] || "fa-tag"}"></i>
                <h2>${categoryLabels[item.category] || item.category}</h2>
                <span class="item-count">0 items</span>
            </div>
            <div class="wardrobe-grid category-grid" id="grid-${item.category}"></div>`;
        container.appendChild(section);
        grid = document.getElementById(gridId);
    }
 
    // Remove empty state placeholder if present
    const empty = grid.querySelector(".empty-state");
    if (empty) empty.remove();
 
    // Inject card at the top
    grid.insertAdjacentHTML("afterbegin", buildCard(item));
 
    // Make sure section is visible
    const section = grid.closest(".category-section");
    section.classList.remove("hidden");
 
    // Update count badge
    updateCount(item.category);
 
    // Attach delete listener to newly added card
    const newCard = grid.querySelector(`[data-id="${item.id}"]`);
    if (newCard) {
        const deleteBtn = newCard.querySelector(".delete-btn");
        if (deleteBtn) attachDeleteListener(deleteBtn);
    }
}
 
/* ══════════════════════════════════════════
   ADD ITEM — POST /api/wardrobe/
   ══════════════════════════════════════════ */
addItemForm.addEventListener("submit", async (e) => {
    e.preventDefault();
 
    if (!imageInput.files[0]) {
        showToast("Please select an image.", "error");
        return;
    }
 
    submitBtn.classList.add("loading");
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving…';
    submitBtn.disabled = true;
 
    const formData = new FormData(addItemForm);
 
    try {
        const res = await fetch("/api/wardrobe/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken(),
            },
            body: formData,
        });
 
        const data = await res.json();
 
        if (res.ok && data.success) {
            addCardToDOM(data.item);
 
            closeModal(itemModal);
            addItemForm.reset();
            imageInput.value = "";
            imagePreview.src = "";
            imagePreviewWrap.classList.add("hidden");
            uploadZone.classList.remove("hidden");
 
            showToast(`"${data.item.name}" added to your wardrobe!`, "success");
        } else {
            showToast(data.error || "Failed to save item. Please try again.", "error");
        }
 
    } catch (err) {
        console.error("Add item error:", err);
        showToast("Network error. Please check your connection.", "error");
    } finally {
        submitBtn.classList.remove("loading");
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Item';
    }
});
 
/* ══════════════════════════════════════════
   DELETE ITEM — DELETE /api/wardrobe/<id>/delete/
   ══════════════════════════════════════════ */
let pendingDeleteId   = null;
let pendingDeleteCard = null;
 
function attachDeleteListener(btn) {
    if (!btn) return;
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        pendingDeleteId   = btn.dataset.id;
        pendingDeleteCard = btn.closest(".card");
        openModal(deleteModal);
    });
}
 
// Attach to all existing cards on page load
document.querySelectorAll(".delete-btn").forEach(attachDeleteListener);
 
// Cancel delete
cancelDelete.addEventListener("click", () => {
    pendingDeleteId   = null;
    pendingDeleteCard = null;
    closeModal(deleteModal);
});
 
deleteModal.addEventListener("click", (e) => {
    if (e.target === deleteModal) closeModal(deleteModal);
});
 
// Confirm delete
confirmDelete.addEventListener("click", async () => {
    if (!pendingDeleteId) return;
 
    const id       = pendingDeleteId;
    const card     = pendingDeleteCard;
    const category = card?.dataset.category;
 
    closeModal(deleteModal);
 
    // Optimistic UI — fade out immediately
    if (card) {
        card.style.transition = "all .25s ease";
        card.style.opacity    = "0";
        card.style.transform  = "scale(0.9)";
    }
 
    try {
        const res = await fetch(`/api/wardrobe/${id}/delete/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCsrfToken(),
                "Content-Type": "application/json",
            },
        });
 
        const data = await res.json();
 
        if (res.ok && data.success) {
            setTimeout(() => {
                if (card) card.remove();
                updateCount(category);
            }, 250);
            showToast("Item deleted from your wardrobe.", "success");
        } else {
            // Restore card if server rejected delete
            if (card) {
                card.style.opacity   = "1";
                card.style.transform = "scale(1)";
            }
            showToast(data.error || "Could not delete item.", "error");
        }
 
    } catch (err) {
        console.error("Delete error:", err);
        // Restore card on network error
        if (card) {
            card.style.opacity   = "1";
            card.style.transform = "scale(1)";
        }
        showToast("Network error. Could not delete.", "error");
    }
 
    pendingDeleteId   = null;
    pendingDeleteCard = null;
});
 
/* ── CATEGORY FILTER TABS ── */
filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        filterBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
 
        const selected = btn.dataset.category;
 
        categorySections.forEach((section) => {
            const cat   = section.dataset.category;
            const count = section.querySelectorAll(".card").length;
 
            if (selected === "all") {
                if (count > 0) section.classList.remove("hidden");
            } else if (cat === selected) {
                section.classList.remove("hidden");
            } else {
                section.classList.add("hidden");
            }
        });
    });
});
 
/* ── THEME TOGGLE ── */
const themeToggle = document.querySelector(".theme-icon");
const themeIconEl = document.querySelector(".theme-icon i");
let isDark = true;
 
if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        isDark = !isDark;
        const root = document.documentElement;
 
        if (isDark) {
            root.style.setProperty("--bg",       "#0d0d0d");
            root.style.setProperty("--surface",  "#161616");
            root.style.setProperty("--surface-2","#1f1f1f");
            root.style.setProperty("--text",     "#f0ece3");
            root.style.setProperty("--border",   "#2e2e2e");
            themeIconEl.className = "fa-regular fa-moon";
        } else {
            root.style.setProperty("--bg",       "#f7f4ef");
            root.style.setProperty("--surface",  "#ffffff");
            root.style.setProperty("--surface-2","#f0ece3");
            root.style.setProperty("--text",     "#1a1a1a");
            root.style.setProperty("--border",   "#e0dbd0");
            themeIconEl.className = "fa-regular fa-sun";
        }
    });
}