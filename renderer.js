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
        const pupil = eyeball.querySelector('.pupil');
        const pupilRadius = rect.width / 4;
        
        pupil.style.transform = `translate(${Math.cos(angle) * pupilRadius}px, ${Math.sin(angle) * pupilRadius}px)`;
    });
});

// TODO: Implement functionality for Add PDF, Remove PDF, and Compile PDF buttons
