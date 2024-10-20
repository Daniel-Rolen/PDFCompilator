// Galaxy background animation
const canvas = document.getElementById('galaxy-background');
const ctx = canvas.getContext('2d');

// Set canvas size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Galaxy properties
const galaxyParticles = [];
const particleCount = 1000;
const baseSize = 1;
const additionalSize = 2;
const baseSpeed = 0.02;
const additionalSpeed = 0.04;

class GalaxyParticle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * additionalSize + baseSize;
        this.originalSize = this.size;
        this.speed = Math.random() * additionalSpeed + baseSpeed;
        this.vx = Math.random() * 2 - 1;
        this.vy = Math.random() * 2 - 1;
        this.hue = Math.random() * 60 + 200; // Blue to purple hues
    }

    update(mouseX, mouseY) {
        this.x += this.vx * this.speed;
        this.y += this.vy * this.speed;

        // Wrap around screen
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;

        // Interactive effect
        const dx = mouseX - this.x;
        const dy = mouseY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxDistance = 100;
        
        if (distance < maxDistance) {
            const force = (maxDistance - distance) / maxDistance;
            this.vx += dx / distance * force * 0.02;
            this.vy += dy / distance * force * 0.02;
            this.size = this.originalSize + force * additionalSize;
        } else {
            this.size = this.originalSize;
        }
    }

    draw() {
        ctx.fillStyle = `hsla(${this.hue}, 100%, 50%, 0.8)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Create initial particles
for (let i = 0; i < particleCount; i++) {
    galaxyParticles.push(new GalaxyParticle());
}

let animationFrameId;
let lastTime = 0;
const targetFPS = 60;
const frameInterval = 1000 / targetFPS;

let mouseX = 0;
let mouseY = 0;

canvas.addEventListener('mousemove', (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
});

function animate(currentTime) {
    animationFrameId = requestAnimationFrame(animate);

    const deltaTime = currentTime - lastTime;
    if (deltaTime < frameInterval) return;

    lastTime = currentTime - (deltaTime % frameInterval);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    galaxyParticles.forEach(particle => {
        particle.update(mouseX, mouseY);
        particle.draw();
    });
}

animate(0);

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
                li.classList.add('space-element');
                selectedFilesList.appendChild(li);
            });
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                li.classList.add('space-element');
                availableFilesList.appendChild(li);
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

updatePdfLists();