const startCamera = document.getElementById("startCamera");

const video = document.getElementById("video");

const captureBtn = document.getElementById("captureBtn");

const canvas = document.getElementById("canvas");

const imageInput = document.getElementById("imageInput");

const form = document.getElementById("profileForm");

const resultBox = document.getElementById("result");

let stream;


// START CAMERA
startCamera.onclick = async () => {

    try{

        stream = await navigator.mediaDevices.getUserMedia({
            video:true
        });

        video.style.display = "block";

        video.srcObject = stream;

    }catch(error){

        alert("Camera access denied");

        console.log(error);
    }
};


// CAPTURE IMAGE
captureBtn.onclick = () => {

    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;

    canvas.height = video.videoHeight;

    context.drawImage(video,0,0);

    canvas.toBlob((blob)=>{

        const file = new File(
            [blob],
            "capture.png",
            {type:"image/png"}
        );

        const container = new DataTransfer();

        container.items.add(file);

        imageInput.files = container.files;

        alert("Photo Captured!");

    });
};


// FORM SUBMIT
form.addEventListener("submit", async (e)=>{

    e.preventDefault();

    const formData = new FormData(form);

    try{

        const response = await fetch("/save-profile/",{

            method:"POST",

            body:formData
        });

        const data = await response.json();

        resultBox.style.display = "block";

        resultBox.innerHTML = `

            <h3>Analysis Result</h3>

            <p><strong>Skin Tone:</strong>
            ${data.skin_tone}</p>

            <p><strong>Body Type:</strong>
            ${data.body_type}</p>

        `;

    }catch(error){

        console.log(error);

        alert("Something went wrong");
    }

});