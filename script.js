class DeepBrainstorm {
    constructor() {
        this.currentStep = 0;
        this.steps = [
            'step-1', 'step-2', 'step-3', 'step-4', 
            'step-5', 'step-6', 'step-7'
        ];
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        const sendButton = document.getElementById('send-button');
        const userInput = document.getElementById('user-input');
        const newQueryButton = document.getElementById('new-query-button');

        sendButton.addEventListener('click', () => this.handleSend());
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });
        newQueryButton.addEventListener('click', () => this.resetToHome());

        // Auto-resize textarea
        userInput.addEventListener('input', () => {
            userInput.style.height = 'auto';
            userInput.style.height = userInput.scrollHeight + 'px';
        });
    }

    async handleSend() {
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const query = userInput.value.trim();

        if (!query) {
            this.showError('Please enter your query first.');
            return;
        }

        // Disable send button
        sendButton.disabled = true;
        sendButton.innerHTML = '<span class="button-text">Processing...</span>';

        this.showProcessingPage();
        this.startProgressAnimation();

        try {
            const response = await this.processQuery(query);
            this.showResults(response);
        } catch (error) {
            console.error('Error processing query:', error);
            this.showError('Sorry, there was an error processing your query. Please try again.');
            this.resetToHome();
        } finally {
            // Re-enable send button
            sendButton.disabled = false;
            sendButton.innerHTML = '<span class="button-text">Send</span><svg class="send-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22,2 15,22 11,13 2,9"></polygon></svg>';
        }
    }

    showProcessingPage() {
        document.getElementById('home-page').style.display = 'none';
        document.getElementById('processing-page').style.display = 'block';
        document.getElementById('results-page').style.display = 'none';
    }

    showResults(response) {
        document.getElementById('home-page').style.display = 'none';
        document.getElementById('processing-page').style.display = 'none';
        document.getElementById('results-page').style.display = 'block';
        
        const resultsContent = document.getElementById('results-content');
        resultsContent.textContent = response;
    }

    resetToHome() {
        document.getElementById('home-page').style.display = 'block';
        document.getElementById('processing-page').style.display = 'none';
        document.getElementById('results-page').style.display = 'none';
        
        // Clear input
        document.getElementById('user-input').value = '';
        document.getElementById('user-input').style.height = 'auto';
        
        // Reset progress
        this.currentStep = 0;
        this.steps.forEach(stepId => {
            const step = document.getElementById(stepId);
            step.classList.remove('active', 'completed');
        });
    }

    startProgressAnimation() {
        this.currentStep = 0;
        
        const animateStep = () => {
            if (this.currentStep < this.steps.length) {
                // Mark current step as active
                const currentStepElement = document.getElementById(this.steps[this.currentStep]);
                currentStepElement.classList.add('active');
                
                // Mark previous steps as completed
                for (let i = 0; i < this.currentStep; i++) {
                    const prevStep = document.getElementById(this.steps[i]);
                    prevStep.classList.remove('active');
                    prevStep.classList.add('completed');
                }
                
                this.currentStep++;
                
                // Continue animation with random delay between 2-4 seconds
                const delay = Math.random() * 2000 + 2000;
                setTimeout(animateStep, delay);
            } else {
                // Mark last step as completed
                const lastStep = document.getElementById(this.steps[this.steps.length - 1]);
                lastStep.classList.remove('active');
                lastStep.classList.add('completed');
            }
        };
        
        animateStep();
    }

    async processQuery(query) {
        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                return data.result;
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Error calling API:', error);
            throw error;
        }
    }

    showError(message) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            font-family: inherit;
            font-size: 0.9rem;
            max-width: 300px;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Remove toast after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new DeepBrainstorm();
});