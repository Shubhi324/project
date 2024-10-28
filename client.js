const peerConnection = new RTCPeerConnection();
const video = document.getElementById('video');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));
    });

async function sendImage() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData.split(',')[1] })
    });

    const result = await response.json();
    console.log(result);  // Display the prediction result
}

// Set interval to send image every few seconds
setInterval(sendImage, 5000);  // Adjust time as needed
