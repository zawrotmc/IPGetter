function refreshPage() {
    window.location.reload();
}

// Keep the server alive
function keepAlive() {
    fetch('/keep-alive', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).catch(console.error);
}

// Send keep-alive request every 30 seconds
setInterval(keepAlive, 30000);

// Add copy functionality if needed in the future
document.addEventListener('DOMContentLoaded', function() {
    const ipAddress = document.getElementById('ipAddress');
    if (ipAddress) {
        ipAddress.title = 'Kliknij aby skopiować';
        ipAddress.style.cursor = 'pointer';
        
        ipAddress.addEventListener('click', async function() {
            try {
                await navigator.clipboard.writeText(this.textContent);
                
                // Visual feedback
                const originalColor = this.style.color;
                this.style.color = 'var(--bs-success)';
                setTimeout(() => {
                    this.style.color = originalColor;
                }, 500);
            } catch (err) {
                console.error('Failed to copy IP:', err);
            }
        });
    }
});
