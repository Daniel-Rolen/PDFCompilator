// Animation for cyberpunk background
const canvas = document.getElementById('bubbly-background');
const ctx = canvas.getContext('2d');

// Set canvas size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Particle properties
const particles = [];
const particleCount = 20; // Reduced from 30 to 20 for better performance

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 0.5 - 0.25; // Reduced speed range
        this.speedY = Math.random() * 0.5 - 0.25; // Reduced speed range
        this.color = `hsl(${Math.random() * 60 + 180}, 100%, 50%)`;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > canvas.width || this.x < 0) {
            this.speedX = -this.speedX;
        }
        if (this.y > canvas.height || this.y < 0) {
            this.speedY = -this.speedY;
        }
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Create initial particles
for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

let animationFrameId;
let lastTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
    animationFrameId = requestAnimationFrame(animate);

    const deltaTime = currentTime - lastTime;
    if (deltaTime < frameInterval) return;

    lastTime = currentTime - (deltaTime % frameInterval);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
}

animate(0);

// Cybernetic eyeball animation
const eyeballs = document.querySelectorAll('.eyeball');
let lastEyeballUpdate = 0;
const eyeballUpdateInterval = 200; // Update every 200ms for better performance

function animateEyeballs(timestamp) {
    if (timestamp - lastEyeballUpdate > eyeballUpdateInterval) {
        eyeballs.forEach(eyeball => {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 5; // Reduced distance for subtler movement
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;
            
            eyeball.style.setProperty('--pupil-x', `${x}px`);
            eyeball.style.setProperty('--pupil-y', `${y}px`);
        });
        lastEyeballUpdate = timestamp;
    }
    
    requestAnimationFrame(animateEyeballs);
}

animateEyeballs(0);

// Bubble animation
function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.style.left = `${Math.random() * 100}%`;
    bubble.style.width = `${Math.random() * 30 + 10}px`; // Reduced size for better performance
    bubble.style.height = bubble.style.width;
    bubble.style.animationDuration = `${Math.random() * 3 + 5}s`; // Reduced animation duration
    document.body.appendChild(bubble);

    bubble.addEventListener('animationend', () => {
        bubble.remove();
    });
}

// Create bubbles at a controlled rate
setInterval(createBubble, 2000); // Reduced frequency for better performance

// Glitch effect for neon elements (optimized)
class GlitchEffect {
    constructor(element) {
        this.element = element;
        this.originalText = element.textContent;
        this.isGlitching = false;
    }

    startGlitch() {
        if (this.isGlitching) return;
        this.isGlitching = true;
        this.glitchInterval = setInterval(() => this.applyGlitch(), 200); // Reduced frequency
    }

    stopGlitch() {
        clearInterval(this.glitchInterval);
        this.isGlitching = false;
        this.element.textContent = this.originalText;
    }

    applyGlitch() {
        const glitchChars = '!@#$%^&*()_+-={}[]|;:,.<>?';
        this.element.textContent = this.originalText
            .split('')
            .map(char => Math.random() > 0.95 ? glitchChars[Math.floor(Math.random() * glitchChars.length)] : char)
            .join('');
    }
}

// Apply GlitchEffect to neon elements
document.querySelectorAll('.neon-element').forEach(element => {
    const glitch = new GlitchEffect(element);
    element.addEventListener('mouseenter', () => glitch.startGlitch());
    element.addEventListener('mouseleave', () => glitch.stopGlitch());
});

// PDF management functionality
const addPdfButton = document.getElementById('addPdf');
const removePdfButton = document.getElementById('removePdf');
const compilePdfButton = document.getElementById('compilePdf');
const selectOutputFolderButton = document.getElementById('selectOutputFolder');
const saveReportButton = document.getElementById('saveReport');
const loadReportButton = document.getElementById('loadReport');
const pdfNameInput = document.getElementById('pdfName');
const selectedFilesList = document.getElementById('selectedFilesList');
const availableFilesList = document.getElementById('availableFilesList');
const useCoverPagesCheckbox = document.getElementById('useCoverPages');
const coverPagesInput = document.getElementById('coverPages');

function updatePdfLists() {
    fetch('/get_pdfs')
        .then(response => response.json())
        .then(pdfs => {
            selectedFilesList.innerHTML = '';
            availableFilesList.innerHTML = '';
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                li.classList.add('neon-element', 'bubble-element');
                selectedFilesList.appendChild(li);
                new GlitchEffect(li);
            });
            // For now, we'll just duplicate the selected files in the available files list
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                li.classList.add('neon-element', 'bubble-element');
                availableFilesList.appendChild(li);
                new GlitchEffect(li);
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
            updatePdfLists();
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
            updatePdfLists();
            pdfNameInput.value = '';
        });
    }
});

compilePdfButton.addEventListener('click', () => {
    fetch('/compile_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            useCoverPages: useCoverPagesCheckbox.checked,
            coverPages: coverPagesInput.value,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`PDFs compiled successfully! Output file: ${data.message}`);
        } else {
            alert(`Error: ${data.message}`);
        }
    });
});

selectOutputFolderButton.addEventListener('click', () => {
    alert('Output folder selection is not implemented in this prototype. Files are saved in the "output" folder.');
});

saveReportButton.addEventListener('click', () => {
    const report = {
        pdfs: Array.from(selectedFilesList.children).map(li => li.textContent),
        useCoverPages: useCoverPagesCheckbox.checked,
        coverPages: coverPagesInput.value,
    };
    const blob = new Blob([JSON.stringify(report)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'binder_report.json';
    a.click();
});

loadReportButton.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const report = JSON.parse(e.target.result);
            report.pdfs.forEach(pdf => {
                fetch('/add_pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: pdf }),
                })
                .then(() => updatePdfLists());
            });
            useCoverPagesCheckbox.checked = report.useCoverPages;
            coverPagesInput.value = report.coverPages;
        };
        reader.readAsText(file);
    };
    input.click();
});

// Initial PDF list update
updatePdfLists();

// Screen flicker effect (optimized)
function screenFlicker() {
    const app = document.getElementById('app');
    app.style.opacity = Math.random() * 0.03 + 0.97; // Reduced flicker intensity
    setTimeout(() => {
        app.style.opacity = 1;
    }, 50);
}

setInterval(screenFlicker, 10000); // Reduced frequency for better performance
