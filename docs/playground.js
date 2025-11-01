// Playground Interactive Scripts

// Command templates
const templates = {
    convert: {
        cli: '# Convert video\nrsj-ffmpeg -i input.mp4 -o output.mp4',
        python: 'from rsj_ffmpeg import RSJToolkit\n\ntoolkit = RSJToolkit()\ntoolkit.convert("input.mp4", "output.mp4")',
        api: 'curl -X POST http://localhost:8080/api/v1/convert \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "input.mp4", "output_file": "output.mp4"}\''
    },
    upscale: {
        cli: '# AI upscale video\nrsj-ffmpeg -i input.mp4 --ai-upscale 4x -o output_4k.mp4',
        python: 'from rsj_ffmpeg import RSJToolkit\nfrom rsj_ffmpeg.ai_engine import AIEngine\n\ntoolkit = RSJToolkit()\nai_engine = AIEngine(toolkit.config)\nai_engine.upscale_video("input.mp4", "output_4k.mp4", scale=4)',
        api: 'curl -X POST http://localhost:8080/api/v1/enhance \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "input.mp4", "output_file": "output_4k.mp4", "upscale": "4x"}\''
    },
    watermark: {
        cli: '# Add watermark\nrsj-ffmpeg -i input.mp4 --watermark "RAJSARASWATI JATAV" -o branded.mp4',
        python: 'from rsj_ffmpeg import RSJToolkit\n\ntoolkit = RSJToolkit()\ntoolkit.add_watermark(\n    "input.mp4",\n    "branded.mp4",\n    text="RAJSARASWATI JATAV"\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/watermark \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "input.mp4", "output_file": "branded.mp4", "text": "RAJSARASWATI JATAV"}\''
    },
    gif: {
        cli: '# Create GIF\nrsj-ffmpeg -i video.mp4 --to-gif -o animation.gif',
        python: 'from rsj_ffmpeg import RSJToolkit\n\ntoolkit = RSJToolkit()\ntoolkit.create_gif(\n    "video.mp4",\n    "animation.gif",\n    fps=15,\n    scale=480\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/gif \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "video.mp4", "output_file": "animation.gif"}\''
    },
    audio: {
        cli: '# Extract audio\nrsj-ffmpeg -i video.mp4 --extract-audio -o audio.mp3',
        python: 'from rsj_ffmpeg import RSJToolkit\n\ntoolkit = RSJToolkit()\ntoolkit.extract_audio(\n    "video.mp4",\n    "audio.mp3"\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/audio/extract \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "video.mp4", "output_file": "audio.mp3"}\''
    },
    batch: {
        cli: '# Batch processing\nrsj-ffmpeg --batch ./videos/ --ai-upscale 4x --enhance --export ./output/',
        python: 'from rsj_ffmpeg import RSJToolkit\n\ntoolkit = RSJToolkit()\ntoolkit.batch_convert(\n    input_dir="./videos/",\n    output_dir="./output/",\n    ai_upscale="4x",\n    enhance=True\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/batch \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_dir": "./videos/", "output_dir": "./output/", "ai_upscale": "4x", "enhance": true}\''
    },
    stream: {
        cli: '# Start live stream\nrsj-ffmpeg --stream-yt YOUR_KEY --input webcam --overlay logo.png',
        python: 'from rsj_ffmpeg.streaming import StreamManager\n\nstream_manager = StreamManager(config)\nstream_manager.start_stream(\n    stream_id="live_001",\n    platform="youtube",\n    key="YOUR_KEY",\n    input_source="webcam"\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/stream/start \\\n  -H "Content-Type: application/json" \\\n  -d \'{"platform": "youtube", "key": "YOUR_KEY", "input_source": "webcam"}\''
    },
    enhance: {
        cli: '# AI enhance video\nrsj-ffmpeg -i video.mp4 --enhance --denoise --stabilize -o enhanced.mp4',
        python: 'from rsj_ffmpeg import RSJToolkit\nfrom rsj_ffmpeg.ai_engine import AIEngine\n\ntoolkit = RSJToolkit()\nai_engine = AIEngine(toolkit.config)\nai_engine.enhance_video(\n    "video.mp4",\n    "enhanced.mp4",\n    denoise=True,\n    stabilize=True\n)',
        api: 'curl -X POST http://localhost:8080/api/v1/enhance \\\n  -H "Content-Type: application/json" \\\n  -d \'{"input_file": "video.mp4", "output_file": "enhanced.mp4", "denoise": true, "stabilize": true}\''
    }
};

// Current language
let currentLang = 'cli';

// Template button handlers
document.addEventListener('DOMContentLoaded', () => {
    const templateButtons = document.querySelectorAll('.template-btn');
    
    templateButtons.forEach(button => {
        button.addEventListener('click', () => {
            const template = button.getAttribute('data-template');
            loadTemplate(template);
        });
    });
});

// Load template
function loadTemplate(templateName) {
    const template = templates[templateName];
    if (!template) return;
    
    // Update all editors
    document.getElementById('cliEditor').value = template.cli;
    document.getElementById('pythonEditor').value = template.python;
    document.getElementById('apiEditor').value = template.api;
    
    // Show success message
    addOutputLine('Template loaded: ' + templateName, 'success');
}

// Language tab switching
document.addEventListener('DOMContentLoaded', () => {
    const editorTabs = document.querySelectorAll('.editor-tab');
    const editorPanels = document.querySelectorAll('.editor-panel');
    
    editorTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const lang = tab.getAttribute('data-lang');
            currentLang = lang;
            
            // Update tabs
            editorTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update panels
            editorPanels.forEach(panel => panel.classList.remove('active'));
            const targetPanel = document.querySelector(`[data-panel="${lang}"]`);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });
});

// Run code
document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runCode');
    
    runBtn.addEventListener('click', () => {
        runCode();
    });
});

function runCode() {
    const editors = {
        cli: document.getElementById('cliEditor'),
        python: document.getElementById('pythonEditor'),
        api: document.getElementById('apiEditor')
    };
    
    const code = editors[currentLang].value;
    
    if (!code.trim()) {
        addOutputLine('Error: No code to run', 'error');
        return;
    }
    
    // Clear previous output
    const outputContent = document.getElementById('outputContent');
    outputContent.innerHTML = '';
    
    // Simulate execution
    addOutputLine('🚀 Executing command...', 'info');
    
    setTimeout(() => {
        addOutputLine('✓ Checking dependencies...', 'success');
    }, 500);
    
    setTimeout(() => {
        addOutputLine('✓ Validating input files...', 'success');
    }, 1000);
    
    setTimeout(() => {
        addOutputLine('✓ Processing started...', 'success');
    }, 1500);
    
    setTimeout(() => {
        if (currentLang === 'cli') {
            simulateCLIOutput(code);
        } else if (currentLang === 'python') {
            simulatePythonOutput(code);
        } else if (currentLang === 'api') {
            simulateAPIOutput(code);
        }
    }, 2000);
}

function simulateCLIOutput(code) {
    addOutputLine('', 'info');
    addOutputLine('[RSJ-FFMPEG] Starting conversion...', 'info');
    addOutputLine('[FFmpeg] Input: input.mp4', 'info');
    addOutputLine('[FFmpeg] Duration: 00:02:30.00', 'info');
    addOutputLine('[FFmpeg] Resolution: 1920x1080', 'info');
    addOutputLine('[FFmpeg] Codec: h264', 'info');
    addOutputLine('', 'info');
    addOutputLine('[Progress] ████████████████████ 100%', 'success');
    addOutputLine('', 'info');
    addOutputLine('✅ Conversion completed successfully!', 'success');
    addOutputLine('Output file: output.mp4', 'success');
    addOutputLine('Processing time: 45.2 seconds', 'info');
}

function simulatePythonOutput(code) {
    addOutputLine('', 'info');
    addOutputLine('RSJToolkit initialized', 'info');
    addOutputLine('Loading configuration...', 'info');
    addOutputLine('FFmpeg version: 6.0', 'info');
    addOutputLine('', 'info');
    addOutputLine('Processing video...', 'info');
    addOutputLine('Progress: [████████████████████] 100%', 'success');
    addOutputLine('', 'info');
    addOutputLine('✅ Success!', 'success');
    addOutputLine('Output saved to: output.mp4', 'success');
}

function simulateAPIOutput(code) {
    addOutputLine('', 'info');
    addOutputLine('HTTP/1.1 200 OK', 'success');
    addOutputLine('Content-Type: application/json', 'info');
    addOutputLine('', 'info');
    addOutputLine('{', 'info');
    addOutputLine('  "status": "success",', 'success');
    addOutputLine('  "job_id": "job_' + Math.random().toString(36).substr(2, 9) + '",', 'info');
    addOutputLine('  "message": "Processing started",', 'info');
    addOutputLine('  "output_file": "output.mp4",', 'info');
    addOutputLine('  "estimated_time": "45 seconds"', 'info');
    addOutputLine('}', 'info');
}

function addOutputLine(text, type = 'info') {
    const outputContent = document.getElementById('outputContent');
    const line = document.createElement('div');
    line.className = `output-line ${type}`;
    line.textContent = text;
    outputContent.appendChild(line);
    outputContent.scrollTop = outputContent.scrollHeight;
}

// Clear output
document.addEventListener('DOMContentLoaded', () => {
    const clearBtn = document.getElementById('clearOutput');
    
    clearBtn.addEventListener('click', () => {
        const outputContent = document.getElementById('outputContent');
        outputContent.innerHTML = `
            <div class="output-welcome">
                <div class="welcome-icon">⚡</div>
                <p>Select a template or write your own command</p>
                <p class="welcome-hint">Click "Run" to see the output</p>
            </div>
        `;
    });
});

// Options handlers
document.addEventListener('DOMContentLoaded', () => {
    const enhanceOpt = document.getElementById('opt-enhance');
    const watermarkOpt = document.getElementById('opt-watermark');
    const normalizeOpt = document.getElementById('opt-normalize');
    const upscaleFactor = document.getElementById('upscale-factor');
    
    // Add event listeners for options
    enhanceOpt?.addEventListener('change', updateCommandWithOptions);
    watermarkOpt?.addEventListener('change', updateCommandWithOptions);
    normalizeOpt?.addEventListener('change', updateCommandWithOptions);
    upscaleFactor?.addEventListener('change', updateCommandWithOptions);
});

function updateCommandWithOptions() {
    const enhance = document.getElementById('opt-enhance')?.checked;
    const watermark = document.getElementById('opt-watermark')?.checked;
    const normalize = document.getElementById('opt-normalize')?.checked;
    const upscale = document.getElementById('upscale-factor')?.value;
    
    // Get current editor
    const editor = document.getElementById('cliEditor');
    let command = editor.value;
    
    // Add options to command
    if (enhance && !command.includes('--enhance')) {
        command += ' --enhance';
    }
    if (watermark && !command.includes('--watermark')) {
        command += ' --watermark "RSJ"';
    }
    if (normalize && !command.includes('--normalize')) {
        command += ' --normalize';
    }
    
    editor.value = command;
}