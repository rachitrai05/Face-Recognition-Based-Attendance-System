const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// 🚀 **Start Webcam**
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error("❌ Error accessing webcam:", error);
    }
}

// 🚀 **Load Face API Models**
async function loadModels() {
    await faceapi.nets.tinyFaceDetector.loadFromUri("https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/");
}

// 🚀 **Detect Faces and Draw Red Bounding Box**
async function detectFaces() {
    const options = new faceapi.TinyFaceDetectorOptions();

    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, options);

        // **Clear Canvas**
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // **Draw Red Box for Each Detected Face**
        detections.forEach((detection) => {
            const { x, y, width, height } = detection.box;
            ctx.strokeStyle = "red";  // Red border
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, width, height);
        });
    }, 100);
}

// 🚀 **Start Everything**
(async function () {
    await loadModels();
    await startWebcam();
    detectFaces();
})();


async function captureImage() {
    let canvas = document.getElementById("canvas");
    let video = document.getElementById("video");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // 📌 Make canvas visible only while capturing
    //canvas.style.display = "block"; 
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    let imageData = canvas.toDataURL("image/png");
    // console.log("Captured Image Data:", imageData.substring(0, 50));

    setTimeout(() => {
      canvas.style.display = "none"; // 🛑 Hide after capture
    }, 500);  // Hides after 0.5 sec

    return imageData.split(',')[1];
}



async function registerFace() {
    let name = document.getElementById("nameInput").value;
    if (!name) return alert("Enter a name");

    let image = await captureImage();
    let response = await fetch("/register", {
        method: "POST",
        body: JSON.stringify({ name, image }),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    alert(result.message);
}

async function recognizeFace() {
    let image = await captureImage();
    let response = await fetch("/recognize", {
        method: "POST",
        body: JSON.stringify({ image }),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    if (result.success) {
        alert(result.message);
        document.getElementById("recognizedName").innerText = `✅ Recognized: ${result.name}`;
    

        // 🛑 Hide the canvas after recognition
        document.getElementById("canvas").style.display = "none";
    } else {
        alert(result.message);
    }
}



async function exportAttendance() {
    let image = await captureImage();
    let response = await fetch("/validate",{
        method: "POST",
        body: JSON.stringify({image}),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    if (result.success){
        if (result.name === "anuj gupta" | result.name === "rachit rai"){
            alert(result.message);
            window.location.href = "/export";
        } else {
            alert(result.message)
        }
    } else {
        alert(result.message)
    }

}

async function openAttendancePage() {
    let image = await captureImage();
    let response = await fetch("/validate",{
        method: "POST",
        body: JSON.stringify({image}),
        headers: { "Content-Type": "application/json" }
    });

    let result = await response.json();
    if (result.success){
        if (result.name === "anuj gupta" | result.name === "rachit rai"){
            alert(result.message);
            window.open("/attendance/view", "_blank");
        } else {
            alert(result.message)
        }
    } else {
        alert(result.message)
    }
    
}
