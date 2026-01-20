// Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const connectionStatus = document.getElementById('connectionStatus');
const projectCount = document.getElementById('projectCount');
const similarProjects = document.getElementById('similarProjects');

// State
let sessionId = generateSessionId();

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    setupEventListeners();
    autoResizeTextarea(); // Initialize textarea size
});

// Event Listeners
function setupEventListeners() {
    sendBtn.addEventListener('click', handleSend);
    
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });
    
    // Auto-resize textarea as user types
    userInput.addEventListener('input', autoResizeTextarea);
}

// Generate Session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Auto-resize textarea
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 300) + 'px';
}

// Check API Health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            connectionStatus.textContent = '✅ Connected';
            connectionStatus.classList.add('online');
        } else {
            connectionStatus.textContent = '⚠️ Degraded';
            connectionStatus.classList.remove('online');
        }
        
        // Get stats
        const statsResponse = await fetch(`${API_BASE_URL}/stats`);
        const stats = await statsResponse.json();
        projectCount.textContent = stats.total_projects || '0';
        
    } catch (error) {
        connectionStatus.textContent = '❌ Offline';
        connectionStatus.classList.add('offline');
        console.error('Health check failed:', error);
    }
}

// Handle Send Message
async function handleSend() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input
    setLoading(true);
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input and reset height
    userInput.value = '';
    autoResizeTextarea();
    
    try {
        // Send to API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add assistant response
        addMessage(data.response, 'assistant', data.confidence);
        
        // Update similar projects
        updateSimilarProjects(data.similar_projects);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('❌ Sorry, something went wrong. Please check if the backend is running.', 'assistant');
    } finally {
        setLoading(false);
    }
}

// Add Message to Chat
function addMessage(text, sender, confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const textP = document.createElement('p');
    textP.textContent = text;
    messageDiv.appendChild(textP);
    
    // Add metadata
    const metaDiv = document.createElement('div');
    metaDiv.className = 'message-meta';
    const timestamp = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    metaDiv.textContent = timestamp;
    
    if (confidence !== null && sender === 'assistant') {
        metaDiv.textContent += ` • Confidence: ${(confidence * 100).toFixed(0)}%`;
    }
    
    messageDiv.appendChild(metaDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Update Similar Projects Sidebar
function updateSimilarProjects(projects) {
    if (!projects || projects.length === 0) {
        similarProjects.innerHTML = '<p class="empty-state">No similar projects found.</p>';
        return;
    }
    
    similarProjects.innerHTML = '';
    
    projects.forEach((project, index) => {
        const card = document.createElement('div');
        card.className = 'project-card';
        
        card.innerHTML = `
            <span class="similarity-badge">${(project.similarity_score * 100).toFixed(0)}% Match</span>
            <p><strong>Problem:</strong> ${truncate(project.problem_description, 80)}</p>
            <p><strong>Approach:</strong> ${truncate(project.ai_approach, 60)}</p>
            <p><strong>Tech:</strong> ${truncate(project.tech_stack, 70)}</p>
        `;
        
        similarProjects.appendChild(card);
    });
}

// Helper: Truncate Text
function truncate(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// Helper: Set Loading State
function setLoading(isLoading) {
    sendBtn.disabled = isLoading;
    userInput.disabled = isLoading;
    
    if (isLoading) {
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}
