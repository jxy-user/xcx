// ============ 全局配置 ============
const CONFIG = {
    COUNTDOWN_TIME: 800,
    BLESSING_TIME: 2000,
    FINAL_BLESSING_TIME: 3500,
    TRANSITION_DURATION: 2500,
    PARTICLE_SIZE: 3,
    SAMPLE_INTERVAL: 8,

    EXPLODE_FORCE_MIN: 15,
    EXPLODE_FORCE_MAX: 30,
    AIR_RESISTANCE: 0.985,

    REFORM_EASE_FACTOR: 0.04,

    EXPLODE_START: 0,
    REFORM_START: 0.35,

    FONT_SIZE: 200
};

// ============ 私人定制配置（从API加载）============
let PERSONALIZED_CONFIG = {};
let DEFAULT_BLESSINGS = [];

// ============ 状态管理 ============
const state = {
    isPlaying: false,
    userName: '',
    phase: 'idle',
    currentText: '',
    nextText: '',
    displayStartTime: 0,
    transitionStartTime: 0,
    particles: [],
    targetPositions: [],
    extraParticles: [],
    animationId: null,
    hasAssignedTargets: false,
    canvasWidth: 0,
    canvasHeight: 0
};

// ============ API 加载配置 ============
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        PERSONALIZED_CONFIG = data.personalized_config;
        DEFAULT_BLESSINGS = data.default_blessings;
        console.log('✅ 配置加载成功');
    } catch (error) {
        console.error('❌ 配置加载失败:', error);
        // 使用默认配置作为后备
        PERSONALIZED_CONFIG = {};
        DEFAULT_BLESSINGS = ['金榜题名', '前程似锦', '梦想成真'];
    }
}

// ============ 矩阵雨背景 ============
const matrixCanvas = document.getElementById('matrix-canvas');
const matrixCtx = matrixCanvas.getContext('2d');

const chars = '金榜题名前程似锦梦想成真学业有成鹏程万里一帆风顺万事如意心想事成成功胜利努力奋斗拼搏坚持加油未来可期';
const fontSize = 16;
let drops = [];

function initMatrix() {
    let canvasWidth, canvasHeight;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    const isMobilePortrait = screenWidth < 768 && screenHeight > screenWidth;

    if (isMobilePortrait) {
        canvasWidth = screenHeight;
        canvasHeight = screenWidth;
    } else {
        canvasWidth = screenWidth;
        canvasHeight = screenHeight;
    }

    matrixCanvas.width = canvasWidth;
    matrixCanvas.height = canvasHeight;
    const columns = matrixCanvas.width / fontSize;
    drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }
}

function drawMatrix() {
    matrixCtx.fillStyle = 'rgba(0, 0, 0, 0.15)';
    matrixCtx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
    matrixCtx.fillStyle = '#FFD700';
    matrixCtx.font = `${fontSize}px Microsoft YaHei`;
    matrixCtx.shadowBlur = 0;

    for (let i = 0; i < drops.length; i++) {
        const char = chars[Math.floor(Math.random() * chars.length)];
        matrixCtx.fillText(char, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}

let lastMatrixTime = 0;
function matrixLoop(timestamp) {
    if (timestamp - lastMatrixTime >= 50) {
        drawMatrix();
        lastMatrixTime = timestamp;
    }
    requestAnimationFrame(matrixLoop);
}

// ============ 粒子系统 ============
const particleCanvas = document.getElementById('particle-canvas');
const particleCtx = particleCanvas.getContext('2d');

function initParticleCanvas() {
    let canvasWidth, canvasHeight;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    const isMobilePortrait = screenWidth < 768 && screenHeight > screenWidth;

    if (isMobilePortrait) {
        canvasWidth = screenHeight;
        canvasHeight = screenWidth;
    } else {
        canvasWidth = screenWidth;
        canvasHeight = screenHeight;
    }

    particleCanvas.width = canvasWidth;
    particleCanvas.height = canvasHeight;
    state.canvasWidth = particleCanvas.width;
    state.canvasHeight = particleCanvas.height;
}

class Particle {
    constructor(x, y, isNew = false) {
        this.x = x;
        this.y = y;
        this.originX = x;
        this.originY = y;
        this.targetX = x;
        this.targetY = y;
        this.size = CONFIG.PARTICLE_SIZE + (Math.random() - 0.5) * 2;
        this.brightness = 0.8 + Math.random() * 0.2;

        this.vx = 0;
        this.vy = 0;

        this.state = isNew ? 'entering' : 'stable';
        this.life = isNew ? 0 : 1;
        this.isExtra = isNew;
    }

    explode() {
        if (this.state === 'stable') {
            this.state = 'exploding';
            const angle = Math.random() * Math.PI * 2;
            const force = CONFIG.EXPLODE_FORCE_MIN +
                           Math.random() * (CONFIG.EXPLODE_FORCE_MAX - CONFIG.EXPLODE_FORCE_MIN);
            this.vx = Math.cos(angle) * force;
            this.vy = Math.sin(angle) * force;
        }
    }

    setTarget(x, y) {
        this.targetX = x;
        this.targetY = y;
        if (this.state === 'exploding') {
            this.state = 'reforming';
        } else if (this.state === 'entering') {
            this.state = 'reforming';
        }
    }

    update(progress = 0) {
        const time = Date.now() * 0.001;

        switch (this.state) {
            case 'stable':
                this.x = this.originX + Math.sin(time + this.originY * 0.01) * 0.5;
                this.y = this.originY + Math.cos(time + this.originX * 0.01) * 0.5;
                break;

            case 'exploding':
                this.x += this.vx;
                this.y += this.vy;
                this.vx *= CONFIG.AIR_RESISTANCE;
                this.vy *= CONFIG.AIR_RESISTANCE;
                this.life = Math.max(0.4, 1 - progress * 0.35);
                break;

            case 'reforming':
                const dx = this.targetX - this.x;
                const dy = this.targetY - this.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance > 2) {
                    const moveRatio = 0.055;
                    this.x += dx * moveRatio;
                    this.y += dy * moveRatio;
                } else if (this.state === 'reforming') {
                    this.state = 'stable';
                    this.originX = this.x;
                    this.originY = this.y;
                }

                const targetLife = 1;
                this.life += (targetLife - this.life) * 0.1;
                break;

            case 'entering':
                this.life = Math.min(1, this.life + 0.03);
                break;
        }
    }

    draw(alpha = 1) {
        if (this.life <= 0) return;

        particleCtx.save();
        particleCtx.globalAlpha = alpha * this.life * this.brightness;
        particleCtx.fillStyle = '#fff';
        particleCtx.shadowBlur = 8;
        particleCtx.shadowColor = '#fff';
        particleCtx.beginPath();
        particleCtx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        particleCtx.fill();
        particleCtx.restore();
    }
}

function createParticleFromOutside(targetX, targetY) {
    const side = Math.floor(Math.random() * 4);
    let x, y;

    switch (side) {
        case 0:
            x = Math.random() * state.canvasWidth;
            y = -50 - Math.random() * 100;
            break;
        case 1:
            x = state.canvasWidth + 50 + Math.random() * 100;
            y = Math.random() * state.canvasHeight;
            break;
        case 2:
            x = Math.random() * state.canvasWidth;
            y = state.canvasHeight + 50 + Math.random() * 100;
            break;
        case 3:
            x = -50 - Math.random() * 100;
            y = Math.random() * state.canvasHeight;
            break;
    }

    const p = new Particle(x, y, true);
    p.setTarget(targetX, targetY);
    return p;
}

function getResponsiveFontSize(text) {
    let displayWidth, displayHeight;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    const isMobilePortrait = screenWidth < 768 && screenHeight > screenWidth;

    if (isMobilePortrait) {
        displayWidth = screenHeight;
        displayHeight = screenWidth;
    } else {
        displayWidth = screenWidth;
        displayHeight = screenHeight;
    }

    let fontSize = CONFIG.FONT_SIZE;

    const isMobile = displayWidth < 1024;

    if (isMobile) {
        const charCount = text.length;
        const maxWidth = displayWidth * 0.9;
        const maxHeight = displayHeight * 0.6;

        let fontSizeByWidth, fontSizeByHeight;

        if (charCount <= 2) {
            fontSizeByWidth = Math.floor(maxWidth / (charCount * 0.8));
            fontSizeByHeight = Math.floor(maxHeight);
        } else if (charCount <= 4) {
            fontSizeByWidth = Math.floor(maxWidth / (charCount * 0.75));
            fontSizeByHeight = Math.floor(maxHeight);
        } else if (charCount <= 6) {
            fontSizeByWidth = Math.floor(maxWidth / (charCount * 0.7));
            fontSizeByHeight = Math.floor(maxHeight * 0.9);
        } else {
            fontSizeByWidth = Math.floor(maxWidth / (charCount * 0.65));
            fontSizeByHeight = Math.floor(maxHeight * 0.8);
        }

        fontSize = Math.min(fontSizeByWidth, fontSizeByHeight, fontSize);

        const minDimension = Math.min(displayWidth, displayHeight);
        if (charCount <= 2) {
            fontSize = Math.min(fontSize, Math.floor(minDimension * 0.45));
        } else if (charCount <= 4) {
            fontSize = Math.min(fontSize, Math.floor(minDimension * 0.35));
        } else if (charCount <= 6) {
            fontSize = Math.min(fontSize, Math.floor(minDimension * 0.28));
        } else {
            fontSize = Math.min(fontSize, Math.floor(minDimension * 0.22));
        }

        fontSize = Math.max(40, Math.min(fontSize, 120));

    } else if (displayWidth < 1400) {
        fontSize = Math.min(fontSize, 160);
    }

    return fontSize;
}

function getTextTargetPositions(text) {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = particleCanvas.width;
    tempCanvas.height = particleCanvas.height;

    const responsiveFontSize = getResponsiveFontSize(text);

    tempCtx.font = `bold ${responsiveFontSize}px Microsoft YaHei`;
    const measuredWidth = tempCtx.measureText(text).width;

    let finalFontSize = responsiveFontSize;
    if (measuredWidth > particleCanvas.width * 0.85) {
        finalFontSize = Math.floor(responsiveFontSize * (particleCanvas.width * 0.85) / measuredWidth);
        finalFontSize = Math.max(25, finalFontSize);
    }

    tempCtx.fillStyle = '#fff';
    tempCtx.font = `bold ${finalFontSize}px Microsoft YaHei`;
    tempCtx.textAlign = 'center';
    tempCtx.textBaseline = 'middle';
    tempCtx.fillText(text, tempCanvas.width / 2, tempCanvas.height / 2);

    const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const data = imageData.data;
    const positions = [];

    for (let y = 0; y < tempCanvas.height; y += CONFIG.SAMPLE_INTERVAL) {
        for (let x = 0; x < tempCanvas.width; x += CONFIG.SAMPLE_INTERVAL) {
            const index = (y * tempCanvas.width + x) * 4;
            if (data[index + 3] > 128) {
                positions.push({ x, y });
            }
        }
    }

    return positions;
}

function assignTargets(currentParticles, targetPositions) {
    if (targetPositions.length === 0) return { used: [], extras: [] };

    const currentCount = currentParticles.length;
    const targetCount = targetPositions.length;
    const result = { used: [], extras: [] };

    const usedTargets = new Set();

    currentParticles.forEach((particle, index) => {
        let targetIndex;

        if (currentCount <= targetCount) {
            targetIndex = Math.floor((index / currentCount) * targetCount);
            targetIndex = (targetIndex + Math.floor(Math.random() * 3)) % targetCount;
        } else {
            targetIndex = index % targetCount;
            if (Math.random() > 0.7) {
                targetIndex = Math.floor(Math.random() * targetCount);
            }
        }

        const target = targetPositions[targetIndex];
        particle.setTarget(target.x, target.y);
        usedTargets.add(targetIndex);
        result.used.push(index);
    });

    for (let i = 0; i < targetCount; i++) {
        if (!usedTargets.has(i)) {
            result.extras.push(targetPositions[i]);
        }
    }

    return result;
}

function animate(timestamp) {
    particleCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);

    if (!state.isPlaying || state.phase === 'idle') {
        state.animationId = requestAnimationFrame(animate);
        return;
    }

    if (state.phase === 'display') {
        if (state.particles.length > 0) {
            state.particles.forEach(p => {
                p.update();
                p.draw(1);
            });
        }

        const elapsed = timestamp - state.displayStartTime;
        const displayTime = getDisplayTime(state.currentText);

        if (elapsed >= displayTime && state.nextText) {
            state.phase = 'transition';
            state.transitionStartTime = timestamp;
            state.targetPositions = getTextTargetPositions(state.nextText);
        }

    } else if (state.phase === 'transition') {
        const elapsed = timestamp - state.transitionStartTime;
        const progress = Math.min(1, elapsed / CONFIG.TRANSITION_DURATION);

        if (progress < CONFIG.REFORM_START) {
            state.particles.forEach(p => {
                if (p.state === 'stable') {
                    p.explode();
                }
                p.update(progress);
                p.draw(1);
            });
        } else {
            if (!state.hasAssignedTargets) {
                const assignment = assignTargets(state.particles, state.targetPositions);

                state.extraParticles = assignment.extras.map(pos =>
                    createParticleFromOutside(pos.x, pos.y)
                );

                state.hasAssignedTargets = true;
            }

            const allParticles = [...state.particles, ...state.extraParticles];
            allParticles.forEach(p => {
                p.update(progress);
                p.draw(1);
            });
        }

        if (progress >= 1) {
            state.particles = [...state.particles.filter(p => !p.isExtra), ...state.extraParticles];
            state.extraParticles = [];
            state.hasAssignedTargets = false;
            state.currentText = state.nextText;
            state.nextText = null;
            state.phase = 'display';
            state.displayStartTime = timestamp;
        }
    }

    state.animationId = requestAnimationFrame(animate);
}

function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

function getDisplayTime(text) {
    const len = text.length;
    if (len <= 3) return CONFIG.COUNTDOWN_TIME;
    if (len <= 6) return CONFIG.BLESSING_TIME;
    return CONFIG.FINAL_BLESSING_TIME;
}

async function showText(text) {
    return new Promise(resolve => {
        const textDisplay = document.getElementById('text-display');
        const textContent = document.getElementById('text-content');

        textContent.textContent = text;
        textDisplay.style.display = 'flex';

        requestAnimationFrame(() => {
            textContent.style.opacity = '1';
            textContent.style.transform = 'scale(1)';
        });

        setTimeout(() => {
            resolve();
        }, getDisplayTime(text));
    });
}

async function transitionTo(nextText) {
    return new Promise(resolve => {
        setTimeout(() => {
            state.nextText = nextText;
            resolve();
        }, 300);
    });
}

async function playParticleAnimation(userName, customBlessings) {
    initParticleCanvas();
    state.particles = [];
    state.isPlaying = true;
    state.phase = 'idle';

    const countdowns = ['3', '2', '1'];
    const blessings = customBlessings || DEFAULT_BLESSINGS;
    const sequence = [...countdowns, ...blessings];

    for (let i = 0; i < sequence.length; i++) {
        const text = sequence[i];
        state.currentText = text;
        state.targetPositions = getTextTargetPositions(text);

        if (i === 0) {
            state.particles = state.targetPositions.map(pos =>
                new Particle(pos.x, pos.y)
            );
        }

        state.phase = 'display';
        state.displayStartTime = performance.now();
        state.nextText = null;

        await showText(text);

        if (i < sequence.length - 1) {
            await transitionTo(sequence[i + 1]);
            state.phase = 'transition';
            state.transitionStartTime = performance.now();
            state.hasAssignedTargets = false;

            await new Promise(resolve => {
                const checkTransition = () => {
                    if (state.phase === 'display') {
                        resolve();
                    } else {
                        requestAnimationFrame(checkTransition);
                    }
                };
                requestAnimationFrame(checkTransition);
            });
        }
    }

    state.isPlaying = false;
    state.phase = 'idle';
}

async function showScalingText(element, text) {
    element.textContent = text;
    element.style.opacity = '1';
    element.style.transform = 'scale(1)';

    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, getDisplayTime(text));
    });
}

function hideScalingText(element) {
    return new Promise(resolve => {
        element.style.opacity = '0';
        element.style.transform = 'scale(0.1)';

        setTimeout(() => {
            element.style.display = 'none';
            resolve();
        }, 500);
    });
}

async function playTextScaleAnimation(userName, blessings) {
    const textDisplay = document.getElementById('text-display');
    const textContent = document.getElementById('text-content');

    textDisplay.style.display = 'flex';

    for (let i = 0; i < blessings.length; i++) {
        await showScalingText(textContent, blessings[i]);

        if (i < blessings.length - 1) {
            await hideScalingText(textContent);
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }

    await new Promise(resolve => setTimeout(resolve, 1500));
    await hideScalingText(textContent);
}

async function playSequence(userName) {
    const config = PERSONALIZED_CONFIG[userName];
    const useParticleAnimation = config && config['use_particle_animation'];
    const blessings = config ? config['blessings'] : DEFAULT_BLESSINGS;

    document.getElementById('input-screen').style.display = 'none';
    document.getElementById('control-btn').style.display = 'block';

    if (!state.animationId) {
        animate(performance.now());
    }

    if (useParticleAnimation) {
        await playParticleAnimation(userName, blessings);
    } else {
        await playTextScaleAnimation(userName, blessings);
    }

    stopAnimation();
}

function startAnimation(userName) {
    if (state.isPlaying) return;

    state.userName = userName;
    playSequence(userName);
}

function stopAnimation() {
    state.isPlaying = false;
    state.phase = 'idle';

    if (state.animationId) {
        cancelAnimationFrame(state.animationId);
        state.animationId = null;
    }

    particleCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
    state.particles = [];
    state.targetPositions = [];
    state.extraParticles = [];

    const textDisplay = document.getElementById('text-display');
    if (textDisplay) {
        textDisplay.style.display = 'none';
    }

    document.getElementById('input-screen').style.display = 'flex';
    document.getElementById('control-btn').style.display = 'none';
}

// ============ 初始化 ============
document.addEventListener('DOMContentLoaded', async () => {
    // 先从API加载配置
    await loadConfig();

    // 初始化画布
    initMatrix();
    initParticleCanvas();

    // 启动矩阵雨
    requestAnimationFrame(matrixLoop);

    // 启动粒子动画循环
    animate(performance.now());

    // 绑定事件
    const inputScreen = document.getElementById('input-screen');
    const startBtn = document.getElementById('start-btn');
    const nameInput = document.getElementById('name-input');
    const controlBtn = document.getElementById('control-btn');

    startBtn.addEventListener('click', () => {
        const name = nameInput.value.trim();
        if (name) {
            startAnimation(name);
        }
    });

    nameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            startBtn.click();
        }
    });

    controlBtn.addEventListener('click', () => {
        stopAnimation();
    });

    window.addEventListener('resize', () => {
        if (state.isPlaying) {
            initParticleCanvas();
        }
        initMatrix();
    });
});
