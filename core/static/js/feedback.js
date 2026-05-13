const fileInput = document.getElementById("fileInput");
const selectBtn = document.getElementById("selectBtn");
const uploadArea = document.getElementById("uploadArea");
const resultBox = document.getElementById("resultBox");

selectBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", previewImage);

function previewImage() {

    const file = fileInput.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {

        uploadArea.innerHTML = `
            <img src="${e.target.result}" class="preview-image" />
        `;

        resultBox.innerHTML = `
            <img src="${e.target.result}" class="preview-result" />

            <div class="analysis">
                <h2>AI Styling Analysis</h2>

                <p>
                    ✔ Great color combination<br><br>
                    ✔ Smart casual styling works well<br><br>
                    ✔ Outfit balance looks clean and modern<br><br>
                    ✔ Consider adding accessories for premium appearance
                </p>
            </div>
        `;
    };

    reader.readAsDataURL(file);
}