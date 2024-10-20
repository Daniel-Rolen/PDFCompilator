// Animation for bubbly background
const canvas = document.createElement('canvas');
canvas.id = 'bubbly-background';
document.getElementById('app').prepend(canvas);
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Bubble properties
const bubbles = [];
const bubbleCount = 50;

class Bubble {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 100;
        this.size = Math.random() * 20 + 10;
        this.speed = Math.random() * 2 + 1;
    }

    rise() {
        this.y -= this.speed;
        if (this.y < -this.size) {
            this.y = canvas.height + this.size;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fill();
    }
}

// Create initial bubbles
for (let i = 0; i < bubbleCount; i++) {
    bubbles.push(new Bubble());
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    bubbles.forEach(bubble => {
        bubble.rise();
        bubble.draw();
    });
    requestAnimationFrame(animate);
}

animate();

// Eyeball animation
const eyeballs = document.querySelectorAll('.eyeball');

document.addEventListener('mousemove', (e) => {
    eyeballs.forEach(eyeball => {
        const rect = eyeball.getBoundingClientRect();
        const eyeX = rect.left + rect.width / 2;
        const eyeY = rect.top + rect.height / 2;
        const angle = Math.atan2(e.clientY - eyeY, e.clientX - eyeX);
        const pupilRadius = rect.width / 4;
        
        eyeball.style.setProperty('--pupil-x', `${Math.cos(angle) * pupilRadius}px`);
        eyeball.style.setProperty('--pupil-y', `${Math.sin(angle) * pupilRadius}px`);
    });
});

// PDF management functionality
const addPdfButton = document.getElementById('addPdf');
const removePdfButton = document.getElementById('removePdf');
const compilePdfButton = document.getElementById('compilePdf');
const pdfNameInput = document.getElementById('pdfName');
const pdfList = document.getElementById('pdfList');

function updatePdfList() {
    fetch('/get_pdfs')
        .then(response => response.json())
        .then(pdfs => {
            pdfList.innerHTML = '';
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                pdfList.appendChild(li);
            });
        });
}

addPdfButton.addEventListener('click', () => {
    const pdfName = pdfNameInput.value.trim();
    if (pdfName) {
        fetch('/add_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: pdfName }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updatePdfList();
            pdfNameInput.value = '';
        });
    }
});

removePdfButton.addEventListener('click', () => {
    const pdfName = pdfNameInput.value.trim();
    if (pdfName) {
        fetch('/remove_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: pdfName }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updatePdfList();
            pdfNameInput.value = '';
        });
    }
});

compilePdfButton.addEventListener('click', () => {
    fetch('/compile_pdf', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
});

// Initial PDF list update
updatePdfList();
