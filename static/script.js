// Animation for cyberpunk background
const canvas = document.getElementById('bubbly-background');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Particle properties
const particles = [];
const particleCount = 100;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 3 - 1.5;
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

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
    requestAnimationFrame(animate);
}

animate();

// Cybernetic eyeball animation
const eyeballs = document.querySelectorAll('.eyeball');

function animateEyeballs() {
    eyeballs.forEach(eyeball => {
        const pupil = eyeball.querySelector('.eyeball::after');
        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 10;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        
        eyeball.style.setProperty('--pupil-x', `${x}px`);
        eyeball.style.setProperty('--pupil-y', `${y}px`);
    });
    
    requestAnimationFrame(animateEyeballs);
}

animateEyeballs();

// Glitch effect for neon elements
class GlitchEffect {
    constructor(element) {
        this.element = element;
        this.originalText = element.textContent;
        this.glitchInterval = null;
        this.glitchDuration = 100;
        this.glitchCooldown = 5000;

        this.element.addEventListener('mouseenter', () => this.startGlitch());
        this.element.addEventListener('mouseleave', () => this.stopGlitch());
    }

    startGlitch() {
        if (this.glitchInterval) return;

        this.glitchInterval = setInterval(() => {
            this.element.textContent = this.generateGlitchedText();
            setTimeout(() => {
                this.element.textContent = this.originalText;
            }, this.glitchDuration);
        }, this.glitchCooldown);
    }

    stopGlitch() {
        clearInterval(this.glitchInterval);
        this.glitchInterval = null;
        this.element.textContent = this.originalText;
    }

    generateGlitchedText() {
        const glitchChars = '!@#$%^&*()_+-={}[]|;:,.<>?';
        return this.originalText
            .split('')
            .map(char => Math.random() > 0.7 ? glitchChars[Math.floor(Math.random() * glitchChars.length)] : char)
            .join('');
    }
}

// Apply GlitchEffect to neon elements
document.querySelectorAll('.neon-element').forEach(element => {
    new GlitchEffect(element);
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
                li.classList.add('neon-element');
                selectedFilesList.appendChild(li);
                new GlitchEffect(li);
            });
            // For now, we'll just duplicate the selected files in the available files list
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                li.classList.add('neon-element');
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

// Resize canvas when window is resized
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Screen flicker effect
function screenFlicker() {
    const app = document.getElementById('app');
    app.style.opacity = Math.random() * 0.1 + 0.9;
    setTimeout(() => {
        app.style.opacity = 1;
    }, 50);
}

setInterval(screenFlicker, 5000);