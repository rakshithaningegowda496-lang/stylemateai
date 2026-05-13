document.addEventListener("DOMContentLoaded", function(){

    const uploadInput = document.getElementById("uploadInput");
    const cameraInput = document.getElementById("cameraInput");

    const previewWrapper = document.getElementById("previewWrapper");
    const previewImage = document.getElementById("previewImage");

    const skinTone = document.querySelector('input[name="skin_tone"]');
    const bodyType = document.querySelector('input[name="body_type"]');
    const skinType = document.querySelector('input[name="skin_type"]');
    const gender = document.querySelector('input[name="gender"]');

    function analyzeImage(file){
        if(!file) return;

        const reader = new FileReader();

        reader.onload = function(e){

            previewWrapper.classList.remove("hidden");
            previewImage.src = e.target.result;

            // Demo auto AI fill
            const tones = ["Fair", "Medium", "Brown", "Dark"];
            const bodies = ["Slim", "Athletic", "Average", "Curvy"];
            const skins = ["Normal", "Dry", "Oily", "Combination"];
            const genders = ["Female", "Male"];

            skinTone.value = tones[Math.floor(Math.random() * tones.length)];
            bodyType.value = bodies[Math.floor(Math.random() * bodies.length)];
            skinType.value = skins[Math.floor(Math.random() * skins.length)];
            gender.value = genders[Math.floor(Math.random() * genders.length)];
        };

        reader.readAsDataURL(file);
    }

    if(uploadInput){
        uploadInput.addEventListener("change", function(e){
            analyzeImage(e.target.files[0]);
        });
    }

    if(cameraInput){
        cameraInput.addEventListener("change", function(e){
            analyzeImage(e.target.files[0]);
        });
    }

});
