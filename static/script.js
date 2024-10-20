// Animation for bubbly background
const canvas = document.getElementById('bubbly-background');
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
        this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
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
        ctx.fillStyle = this.color;
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
    
    setTimeout(animateEyeballs, Math.random() * 1000 + 500);
}

animateEyeballs();

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
                selectedFilesList.appendChild(li);
            });
            // For now, we'll just duplicate the selected files in the available files list
            // In a real application, you'd fetch available files separately
            pdfs.forEach(pdf => {
                const li = document.createElement('li');
                li.textContent = pdf;
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
        alert(data.message);
    });
});

selectOutputFolderButton.addEventListener('click', () => {
    // This would typically open a folder selection dialog
    // For now, we'll just show an alert
    alert('Output folder selection is not implemented in this prototype.');
});

saveReportButton.addEventListener('click', () => {
    // This would typically save the current compilation settings
    // For now, we'll just show an alert
    alert('Report saving is not implemented in this prototype.');
});

loadReportButton.addEventListener('click', () => {
    // This would typically load saved compilation settings
    // For now, we'll just show an alert
    alert('Report loading is not implemented in this prototype.');
});

// Initial PDF list update
updatePdfLists();
