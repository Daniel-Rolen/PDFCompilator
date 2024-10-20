// Animation for bubbly background
const canvas = document.getElementById('bubbly-background');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Bubble properties
const bubbles = [];
const bubbleCount = 50;
const bubblePool = [];

class Bubble {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height + Math.random() * 100;
        this.size = Math.random() * 20 + 10;
        this.speed = Math.random() * 2 + 1;
        this.color = `hsla(${Math.random() * 360}, 100%, 50%, 0.5)`;
        this.opacity = Math.random() * 0.5 + 0.1;
        this.scale = 1;
        this.growthRate = Math.random() * 0.02 - 0.01;
        this.wobbleOffset = Math.random() * Math.PI * 2;
        this.wobbleSpeed = Math.random() * 0.05 + 0.02;
    }

    update() {
        this.y -= this.speed;
        this.x += Math.sin(this.wobbleOffset) * 0.5;
        this.wobbleOffset += this.wobbleSpeed;
        this.scale += this.growthRate;

        if (this.scale > 1.2 || this.scale < 0.8) {
            this.growthRate *= -1;
        }

        this.opacity += this.growthRate * 0.2;
        this.opacity = Math.max(0.1, Math.min(0.6, this.opacity));

        if (this.y < -this.size) {
            this.reset();
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * this.scale, 0, Math.PI * 2);
        ctx.fillStyle = this.color.replace('0.5', this.opacity);
        ctx.fill();
    }
}

function createBubble() {
    if (bubblePool.length > 0) {
        return bubblePool.pop();
    }
    return new Bubble();
}

// Create initial bubbles
for (let i = 0; i < bubbleCount; i++) {
    bubbles.push(createBubble());
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    bubbles.forEach(bubble => {
        bubble.update();
        bubble.draw();
    });
    requestAnimationFrame(animate);
}

animate();

// Eyeball animation
const eyeballs = document.querySelectorAll('.eyeball');
const eyeballBubbles = [];

class EyeballBubble extends Bubble {
    constructor(eyeball) {
        super();
        this.eyeball = eyeball;
        this.angle = Math.random() * Math.PI * 2;
        this.distance = Math.random() * 30 + 20;
        this.size = Math.random() * 5 + 2;
    }

    update() {
        super.update();
        this.angle += 0.05;
        const rect = this.eyeball.getBoundingClientRect();
        this.x = rect.left + rect.width / 2 + Math.cos(this.angle) * this.distance;
        this.y = rect.top + rect.height / 2 + Math.sin(this.angle) * this.distance;
    }
}

eyeballs.forEach(eyeball => {
    for (let i = 0; i < 5; i++) {
        eyeballBubbles.push(new EyeballBubble(eyeball));
    }
});

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
    
    eyeballBubbles.forEach(bubble => {
        bubble.update();
        bubble.draw();
    });

    requestAnimationFrame(animateEyeballs);
}

animateEyeballs();

// New BalloonElement class for buttons, sections, and window frames
class BalloonElement {
    constructor(element) {
        this.element = element;
        this.originalScale = 1;
        this.inflated = false;
        this.wobbleOffset = Math.random() * Math.PI * 2;
        this.wobbleSpeed = Math.random() * 0.02 + 0.01;

        this.element.addEventListener('mouseenter', () => this.inflate());
        this.element.addEventListener('mouseleave', () => this.deflate());
        this.element.addEventListener('click', () => this.wobble());

        this.animate();
    }

    inflate() {
        this.inflated = true;
        this.element.style.transform = `scale(1.05)`;
    }

    deflate() {
        this.inflated = false;
        this.element.style.transform = `scale(1)`;
    }

    wobble() {
        this.element.style.animation = 'wobble 0.8s ease-in-out';
        this.element.addEventListener('animationend', () => {
            this.element.style.animation = '';
        }, { once: true });
    }

    animate() {
        if (!this.inflated) {
            this.wobbleOffset += this.wobbleSpeed;
            const wobbleAmount = Math.sin(this.wobbleOffset) * 2;
            this.element.style.transform = `translateY(${wobbleAmount}px)`;
        }
        requestAnimationFrame(() => this.animate());
    }
}

// Apply BalloonElement behavior to relevant elements
document.querySelectorAll('.balloon-element').forEach(element => {
    new BalloonElement(element);
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
                li.classList.add('balloon-element');
                selectedFilesList.appendChild(li);
                new BalloonElement(li);
            });
            // For now, we'll just duplicate the selected files in the available files list
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
                li.classList.add('balloon-element');
                availableFilesList.appendChild(li);
                new BalloonElement(li);
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
        alert(data.message);
    });
});

selectOutputFolderButton.addEventListener('click', () => {
    alert('Output folder selection is not implemented in this prototype.');
});

saveReportButton.addEventListener('click', () => {
    alert('Report saving is not implemented in this prototype.');
});

loadReportButton.addEventListener('click', () => {
    alert('Report loading is not implemented in this prototype.');
});

// Initial PDF list update
updatePdfLists();

// Resize canvas when window is resized
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
