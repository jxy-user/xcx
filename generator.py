import json
import random
from datetime import datetime
import webbrowser
import os
import math

class BlessingConfigManager:
    """
    祝福语配置管理器
    在这里修改所有私人定制的祝福语，运行后自动生成HTML
    """

    def __init__(self):
        # ✨✨✨ 在这里修改每个人的专属祝福语 ✨✨✨
        # 格式：'名字': {'use_particle_animation': True/False, 'blessings': ['祝福语1', '祝福语2', ...]}
        self.personalized_config = {
            '赵慧敏': {
                'use_particle_animation': True,
                'blessings': [
                    '加油 赵慧敏',
                    '金榜题名',
                    '必胜',
                    '前程似锦',
                    '梦想成真'
                ]
            },
            '葛林轩': {
                'use_particle_animation': False,
                'blessings': [
                    '祝福语1',
                    '祝福语2',
                    '祝福语3'
                ]
            },
            '赵子杰': {
                'use_particle_animation': False,
                'blessings': [
                    '祝福语1',
                    '祝福语2',
                    '祝福语3'
                ]
            },
            '王博杰': {
                'use_particle_animation': False,
                'blessings': [
                    '祝福语1',
                    '祝福语2',
                    '祝福语3'
                ]
            },
            '李恬静': {
                'use_particle_animation': False,
                'blessings': [
                    '祝福语1',
                    '祝福语2',
                    '祝福语3'
                ]
            },
            '张琳苒': {
                'use_particle_animation': False,
                'blessings': [
                    '祝福语1',
                    '祝福语2',
                    '祝福语3'
                ]
            }
        }

        self.default_blessings = ['金榜题名', '前程似锦', '梦想成真']

    def get_user_config(self, name):
        if name in self.personalized_config:
            return self.personalized_config[name]
        return None

    def is_special_user(self, name):
        config = self.get_user_config(name)
        return config and config.get('use_particle_animation', False)

    def get_blessings_for_user(self, name):
        config = self.get_user_config(name)
        if config and 'blessings' in config:
            return config['blessings']
        return list(self.default_blessings)

    def generate_html(self):
        """生成完整的HTML文件"""
        html_content = self._build_complete_html()

        output_file = "index.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ HTML文件已生成！")
        print(f"📂 文件位置: {os.path.abspath(output_file)}")

        return output_file

    def _build_complete_html(self):
        """构建完整的HTML内容（与index.html完全一致）"""

        personalized_config_json = json.dumps(self.personalized_config, indent=12, ensure_ascii=False)
        default_blessings_json = json.dumps(self.default_blessings, ensure_ascii=False)

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>高考祝福</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}

        body {{
            background: #000;
            font-family: 'Microsoft YaHei', sans-serif;
        }}

        /* 横屏提示层 */
        #landscape-reminder {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            z-index: 9999;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #FFD700;
            text-align: center;
            padding: 20px;
        }}

        #landscape-reminder .rotate-icon {{
            font-size: 80px;
            margin-bottom: 30px;
            animation: rotateHint 2s ease-in-out infinite;
        }}

        #landscape-reminder h2 {{
            font-size: clamp(24px, 5vw, 36px);
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(255,215,0,0.8);
        }}

        #landscape-reminder p {{
            font-size: clamp(16px, 3vw, 22px);
            opacity: 0.9;
            max-width: 80%;
        }}

        @keyframes rotateHint {{
            0%, 100% {{ transform: rotate(0deg); }}
            50% {{ transform: rotate(90deg); }}
        }}

        /* 竖屏时显示横屏提示 */
        @media screen and (orientation: portrait) and (max-width: 768px) {{
            #landscape-reminder {{
                display: flex !important;
            }}

            .container,
            #matrix-canvas,
            #particle-canvas,
            #text-display,
            #control-btn {{
                display: none !important;
            }}
        }}

        @media screen and (orientation: landscape) or (min-width: 769px) {{
            #landscape-reminder {{
                display: none !important;
            }}
        }}

        #matrix-canvas {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}

        .container {{
            position: relative;
            z-index: 10;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        #input-screen {{
            text-align: center;
            color: #fff;
            padding: 20px;
        }}

        #input-screen h1 {{
            font-size: clamp(28px, 6vw, 48px);
            margin-bottom: 30px;
            text-shadow: 0 0 20px rgba(255,215,0,0.8);
            color: #FFD700;
        }}

        #name-input {{
            font-size: clamp(16px, 3vw, 24px);
            padding: 15px 30px;
            width: min(300px, 80vw);
            border: 2px solid #FFD700;
            border-radius: 10px;
            background: rgba(0,0,0,0.7);
            color: #fff;
            outline: none;
            margin-bottom: 20px;
        }}

        #name-input::placeholder {{
            color: rgba(255,215,0,0.5);
        }}

        #start-btn {{
            font-size: clamp(16px, 3vw, 24px);
            padding: 15px 50px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            color: #000;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 0 30px rgba(255,215,0,0.5);
        }}

        #start-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 40px rgba(255,215,0,0.8);
        }}

        #particle-canvas {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 5;
            pointer-events: none;
        }}

        .hidden {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <!-- 横屏提示（手机竖屏时显示） -->
    <div id="landscape-reminder">
        <div class="rotate-icon">📱</div>
        <h2>请横屏观看以获得最佳体验</h2>
        <p>旋转您的手机至横屏模式<br>享受完整的高考祝福动画效果 ✨</p>
    </div>

    <canvas id="matrix-canvas"></canvas>
    <canvas id="particle-canvas"></canvas>

    <div id="text-display" style="
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 50;
        justify-content: center;
        align-items: center;
        pointer-events: none;
    ">
        <div id="text-content" style="
            color: #FFD700;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            text-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700, 0 0 60px #FFD700;
            opacity: 0;
            transform: scale(0.1);
            transition: all 2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        "></div>
    </div>

    <button id="control-btn" style="
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 100;
        padding: 12px 25px;
        font-size: 16px;
        border: none;
        border-radius: 25px;
        background: rgba(255, 215, 0, 0.9);
        color: #000;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
        transition: all 0.3s ease;
    ">⏹️ 停止播放</button>

    <div class="container">
        <div id="input-screen">
            <h1>✨ JXY的高考祝福 ✨</h1>
            <input type="text" id="name-input" placeholder="请输入你的名字">
            <br>
            <button id="start-btn">🎬 开始播放</button>
        </div>
    </div>

    <script>
        // ============ 全局配置 ============
        const CONFIG = {{
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
        }};

        // ============ 私人定制配置（由Python生成）============
        const PERSONALIZED_CONFIG = {personalized_config_json};

        const DEFAULT_BLESSINGS = {default_blessings_json};

        // ============ 状态管理 ============
        const state = {{
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
        }};

        // ============ 矩阵雨背景 ============
        const matrixCanvas = document.getElementById('matrix-canvas');
        const matrixCtx = matrixCanvas.getContext('2d');

        const chars = '金榜题名前程似锦梦想成真学业有成鹏程万里一帆风顺万事如意心想事成成功胜利努力奋斗拼搏坚持加油未来可期';
        const fontSize = 16;
        let drops = [];

        function initMatrix() {{
            matrixCanvas.width = window.innerWidth;
            matrixCanvas.height = window.innerHeight;
            const columns = matrixCanvas.width / fontSize;
            drops = [];
            for (let i = 0; i < columns; i++) {{
                drops[i] = Math.random() * -100;
            }}
        }}

        function drawMatrix() {{
            matrixCtx.fillStyle = 'rgba(0, 0, 0, 0.15)';
            matrixCtx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
            matrixCtx.fillStyle = '#FFD700';
            matrixCtx.font = `${{fontSize}}px Microsoft YaHei`;
            matrixCtx.shadowBlur = 0;

            for (let i = 0; i < drops.length; i++) {{
                const char = chars[Math.floor(Math.random() * chars.length)];
                matrixCtx.fillText(char, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975) {{
                    drops[i] = 0;
                }}
                drops[i]++;
            }}
        }}

        let lastMatrixTime = 0;
        function matrixLoop(timestamp) {{
            if (timestamp - lastMatrixTime >= 50) {{
                drawMatrix();
                lastMatrixTime = timestamp;
            }}
            requestAnimationFrame(matrixLoop);
        }}

        // ============ 粒子系统（动态数量 + 温柔效果）============
        const particleCanvas = document.getElementById('particle-canvas');
        const particleCtx = particleCanvas.getContext('2d');

        function initParticleCanvas() {{
            particleCanvas.width = window.innerWidth;
            particleCanvas.height = window.innerHeight;
            state.canvasWidth = particleCanvas.width;
            state.canvasHeight = particleCanvas.height;
        }}

        class Particle {{
            constructor(x, y, isNew = false) {{
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
            }}

            explode() {{
                if (this.state === 'stable') {{
                    this.state = 'exploding';
                    const angle = Math.random() * Math.PI * 2;
                    const force = CONFIG.EXPLODE_FORCE_MIN +
                                   Math.random() * (CONFIG.EXPLODE_FORCE_MAX - CONFIG.EXPLODE_FORCE_MIN);
                    this.vx = Math.cos(angle) * force;
                    this.vy = Math.sin(angle) * force;
                }}
            }}

            setTarget(x, y) {{
                this.targetX = x;
                this.targetY = y;
                if (this.state === 'exploding') {{
                    this.state = 'reforming';
                }} else if (this.state === 'entering') {{
                    this.state = 'reforming';
                }}
            }}

            update(progress = 0) {{
                const time = Date.now() * 0.001;

                switch (this.state) {{
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

                        if (distance > 2) {{
                            const moveRatio = 0.055;
                            this.x += dx * moveRatio;
                            this.y += dy * moveRatio;
                        }} else if (this.state === 'reforming') {{
                            this.state = 'stable';
                            this.originX = this.x;
                            this.originY = this.y;
                        }}

                        const targetLife = 1;
                        this.life += (targetLife - this.life) * 0.1;
                        break;

                    case 'entering':
                        this.life = Math.min(1, this.life + 0.03);
                        break;
                }}
            }}

            draw(alpha = 1) {{
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
            }}
        }}

        function createParticleFromOutside(targetX, targetY) {{
            const side = Math.floor(Math.random() * 4);
            let x, y;

            switch (side) {{
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
            }}

            const p = new Particle(x, y, true);
            p.setTarget(targetX, targetY);
            return p;
        }}

        // 响应式字体大小计算（确保文字不溢出屏幕）
        function getResponsiveFontSize(text) {{
            const canvasWidth = particleCanvas.width || window.innerWidth;
            const canvasHeight = particleCanvas.height || window.innerHeight;

            // 基础字体大小
            let fontSize = CONFIG.FONT_SIZE;

            // 根据屏幕宽度调整（手机端缩小字体）
            if (canvasWidth < 768) {{
                // 手机横屏：宽度有限，按比例缩放
                // 预估每个字符约占宽度的比例
                const charCount = text.length;
                const estimatedCharWidth = fontSize * 0.7; // 中文字符约为字号的70%
                const totalTextWidth = charCount * estimatedCharWidth;

                // 如果文字总宽度超过屏幕80%，则缩小字体
                if (totalTextWidth > canvasWidth * 0.8) {{
                    fontSize = Math.floor((canvasWidth * 0.8) / (charCount * 0.7));
                }}

                // 确保字体不会太小或太大
                fontSize = Math.max(40, Math.min(fontSize, 120));
            }} else if (canvasWidth < 1200) {{
                // 平板或小屏幕笔记本：适度缩小
                fontSize = Math.min(fontSize, 160);
            }}

            return fontSize;
        }}

        function getTextTargetPositions(text) {{
            const tempCanvas = document.createElement('canvas');
            const tempCtx = tempCanvas.getContext('2d');
            tempCanvas.width = particleCanvas.width;
            tempCanvas.height = particleCanvas.height;

            // 使用响应式字体大小
            const responsiveFontSize = getResponsiveFontSize(text);

            tempCtx.fillStyle = '#fff';
            tempCtx.font = `bold ${{responsiveFontSize}}px Microsoft YaHei`;
            tempCtx.textAlign = 'center';
            tempCtx.textBaseline = 'middle';
            tempCtx.fillText(text, tempCanvas.width / 2, tempCanvas.height / 2);

            const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
            const data = imageData.data;
            const positions = [];

            for (let y = 0; y < tempCanvas.height; y += CONFIG.SAMPLE_INTERVAL) {{
                for (let x = 0; x < tempCanvas.width; x += CONFIG.SAMPLE_INTERVAL) {{
                    const index = (y * tempCanvas.width + x) * 4;
                    if (data[index + 3] > 128) {{
                        positions.push({{ x, y }});
                    }}
                }}
            }}

            return positions;
        }}

        function assignTargets(currentParticles, targetPositions) {{
            if (targetPositions.length === 0) return {{ used: [], extras: [] }};

            const currentCount = currentParticles.length;
            const targetCount = targetPositions.length;
            const result = {{
                used: [],
                extras: []
            }};

            const usedTargets = new Set();

            currentParticles.forEach((particle, index) => {{
                let targetIndex;

                if (currentCount <= targetCount) {{
                    targetIndex = Math.floor((index / currentCount) * targetCount);
                    targetIndex = (targetIndex + Math.floor(Math.random() * 3)) % targetCount;
                }} else {{
                    targetIndex = index % targetCount;
                    if (Math.random() > 0.7) {{
                        targetIndex = Math.floor(Math.random() * targetCount);
                    }}
                }}

                const target = targetPositions[targetIndex];
                particle.setTarget(target.x, target.y);
                usedTargets.add(targetIndex);
                result.used.push(index);
            }});

            for (let i = 0; i < targetCount; i++) {{
                if (!usedTargets.has(i)) {{
                    result.extras.push(targetPositions[i]);
                }}
            }}

            return result;
        }}

        function animate(timestamp) {{
            particleCtx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);

            if (!state.isPlaying || state.phase === 'idle') {{
                state.animationId = requestAnimationFrame(animate);
                return;
            }}

            if (state.phase === 'display') {{
                if (state.particles.length > 0) {{
                    state.particles.forEach(p => {{
                        p.update();
                        p.draw(1);
                    }});
                }}

                const elapsed = timestamp - state.displayStartTime;
                const displayTime = getDisplayTime(state.currentText);

                if (elapsed >= displayTime && state.nextText) {{
                    state.phase = 'transition';
                    state.transitionStartTime = timestamp;
                    state.targetPositions = getTextTargetPositions(state.nextText);
                }}

            }} else if (state.phase === 'transition') {{
                const elapsed = timestamp - state.transitionStartTime;
                const progress = Math.min(1, elapsed / CONFIG.TRANSITION_DURATION);

                if (progress < CONFIG.REFORM_START) {{
                    state.particles.forEach(p => {{
                        if (p.state === 'stable') {{
                            p.explode();
                        }}
                        p.update(progress);
                        p.draw(1);
                    }});
                }} else {{
                    if (!state.hasAssignedTargets) {{
                        const assignment = assignTargets(state.particles, state.targetPositions);

                        state.extraParticles = assignment.extras.map(pos =>
                            createParticleFromOutside(pos.x, pos.y)
                        );

                        state.hasAssignedTargets = true;
                    }}

                    state.particles.forEach(p => {{
                        p.update(progress);
                        p.draw(1);
                    }});

                    state.extraParticles.forEach(p => {{
                        p.update(progress);
                        p.draw(1);
                    }});
                }}

                if (progress >= 1) {{
                    const allParticles = [...state.particles, ...state.extraParticles];

                    allParticles.forEach(p => {{
                        if (p.state === 'reforming') {{
                            p.state = 'stable';
                            p.originX = p.targetX;
                            p.originY = p.targetY;
                        }}
                        p.isExtra = false;
                    }});

                    state.particles = allParticles;
                    state.currentText = state.nextText;
                    state.nextText = '';
                    state.targetPositions = [];
                    state.extraParticles = [];
                    state.hasAssignedTargets = false;
                    state.phase = 'display';
                    state.displayStartTime = timestamp;

                    if (window._onTransitionComplete) {{
                        window._onTransitionComplete();
                        window._onTransitionComplete = null;
                    }}
                }}
            }}

            state.animationId = requestAnimationFrame(animate);
        }}

        function easeInOutCubic(t) {{
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }}

        function getDisplayTime(text) {{
            const countdownNumbers = ['3', '2', '1'];
            if (countdownNumbers.includes(text)) {{
                return CONFIG.COUNTDOWN_TIME;
            }}
            return CONFIG.BLESSING_TIME;
        }}

        async function showText(text) {{
            return new Promise((resolve) => {{
                state.currentText = text;
                state.phase = 'display';
                state.displayStartTime = performance.now();

                const targetPositions = getTextTargetPositions(text);
                state.particles = targetPositions.map(pos => new Particle(pos.x, pos.y));

                const checkReady = () => {{
                    if (state.particles.length > 0) {{
                        resolve();
                    }} else {{
                        requestAnimationFrame(checkReady);
                    }}
                }};
                checkReady();
            }});
        }}

        async function transitionTo(nextText) {{
            return new Promise((resolve) => {{
                state.nextText = nextText;
                window._onTransitionComplete = resolve;
            }});
        }}

        async function playParticleAnimation(userName, customBlessings) {{
            const countdownNumbers = ['3', '2', '1'];
            const allTexts = [...countdownNumbers, ...customBlessings];

            while (state.isPlaying) {{
                state.particles = [];
                state.extraParticles = [];
                state.targetPositions = [];

                await showText(allTexts[0]);

                for (let i = 1; i < allTexts.length; i++) {{
                    if (!state.isPlaying) break;
                    await transitionTo(allTexts[i]);
                }}

                if (!state.isPlaying) break;
                await transitionTo(countdownNumbers[0]);
            }}
        }}

        async function showScalingText(element, text) {{
            return new Promise((resolve) => {{
                element.textContent = text;
                element.style.opacity = '1';
                element.style.transform = 'scale(1)';

                setTimeout(resolve, 100);
            }});
        }}

        function hideScalingText(element) {{
            element.style.opacity = '0';
            element.style.transform = 'scale(0.1)';
        }}

        async function playTextScaleAnimation(userName, blessings) {{
            const textDisplay = document.getElementById('text-display');
            const textContent = document.getElementById('text-content');
            const particleCanvasEl = document.getElementById('particle-canvas');

            textDisplay.style.display = 'flex';
            particleCanvasEl.style.display = 'none';

            const allTexts = [userName, ...blessings];

            while (state.isPlaying) {{
                for (let i = 0; i < allTexts.length; i++) {{
                    if (!state.isPlaying) break;

                    await showScalingText(textContent, allTexts[i]);
                    await new Promise(r => setTimeout(r, 1500));

                    hideScalingText(textContent);
                    await new Promise(r => setTimeout(r, 500));
                }}

                if (!state.isPlaying) break;
                await new Promise(r => setTimeout(r, 1000));
            }}

            textDisplay.style.display = 'none';
            particleCanvasEl.style.display = 'block';
        }}

        async function playSequence(userName) {{
            const config = PERSONALIZED_CONFIG[userName];
            const isSpecialUser = config && config.use_particle_animation;

            if (isSpecialUser) {{
                await playParticleAnimation(userName, config.blessings);
            }} else {{
                const blessings = config ? config.blessings : [...DEFAULT_BLESSINGS];
                await playTextScaleAnimation(userName, blessings);
            }}
        }}

        function startAnimation(userName) {{
            state.userName = userName;
            state.isPlaying = true;
            state.phase = 'idle';

            const inputScreen = document.getElementById('input-screen');
            const controlBtn = document.getElementById('control-btn');

            inputScreen.classList.add('hidden');
            controlBtn.style.display = 'block';

            initMatrix();
            initParticleCanvas();

            if (!state.animationId) {{
                animate(performance.now());
            }}

            if (!matrixCanvas.dataset.initialized) {{
                matrixLoop(performance.now());
                matrixCanvas.dataset.initialized = 'true';
            }}

            playSequence(userName).catch(console.error);
        }}

        function stopAnimation() {{
            state.isPlaying = false;
            state.phase = 'idle';

            const inputScreen = document.getElementById('input-screen');
            const controlBtn = document.getElementById('control-btn');
            const textDisplay = document.getElementById('text-display');
            const particleCanvasEl = document.getElementById('particle-canvas');

            inputScreen.classList.remove('hidden');
            controlBtn.style.display = 'none';
            textDisplay.style.display = 'none';
            particleCanvasEl.style.display = 'none';

            if (state.animationId) {{
                cancelAnimationFrame(state.animationId);
                state.animationId = null;
            }}

            state.particles = [];
            state.extraParticles = [];
            state.targetPositions = [];
            state.currentText = '';
            state.nextText = '';
            state.hasAssignedTargets = false;

            const particleCtx2 = particleCanvas.getContext('2d');
            particleCtx2.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
        }}

        const inputScreen = document.getElementById('input-screen');
        const startBtn = document.getElementById('start-btn');
        const nameInput = document.getElementById('name-input');
        const controlBtn = document.getElementById('control-btn');

        startBtn.addEventListener('click', () => {{
            const name = nameInput.value.trim();
            if (!name) {{
                alert('请输入名字！');
                return;
            }}
            startAnimation(name);
        }});

        nameInput.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') {{
                startBtn.click();
            }}
        }});

        controlBtn.addEventListener('click', () => {{
            stopAnimation();
        }});

        window.addEventListener('resize', () => {{
            if (state.isPlaying) {{
                initParticleCanvas();
            }}
            initMatrix();
            checkOrientation();
        }});

        // ============ 横屏检测（手机端）============
        function checkOrientation() {{
            const isMobile = window.innerWidth <= 768;
            const isPortrait = window.innerHeight > window.innerWidth;
            const reminder = document.getElementById('landscape-reminder');

            if (isMobile && isPortrait) {{
                if (reminder) reminder.style.display = 'flex';
            }} else {{
                if (reminder) reminder.style.display = 'none';
            }}
        }}

        window.addEventListener('orientationchange', () => {{
            setTimeout(checkOrientation, 100);
        }});

        // 初始化时检查
        checkOrientation();
    </script>
</body>
</html>'''

        return html


def main():
    print("=" * 60)
    print("🎬 高考私人定制祝福动画生成器")
    print("=" * 60)

    manager = BlessingConfigManager()

    print("\n📋 当前配置的私人定制用户：\n")
    for name, config in manager.personalized_config.items():
        mode = "✨ 粒子动画" if config['use_particle_animation'] else "🔤 文字放大警示"
        has_placeholder = any('祝福语' in b for b in config['blessings'])
        warning = " ⚠️  包含占位符祝福语（需要修改）" if has_placeholder else ""

        print(f"  • {name}")
        print(f"    模式: {mode}")
        print(f"    祝福语数量: {len(config['blessings'])} 句{warning}\n")

    manager.generate_html()

    print("\n" + "=" * 60)
    print("💡 使用方法：")
    print("   1. 打开 generator.py 修改 personalized_config 字典")
    print("   2. 运行 python generator.py 重新生成")
    print("   3. 在浏览器中打开 index.html 预览效果")
    print("=" * 60)


if __name__ == "__main__":
    main()
