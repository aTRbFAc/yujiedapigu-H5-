// 等待页面完全加载后再执行
window.addEventListener('load', function () {
  // 获取元素
  const scene1 = document.getElementById('scene1');
  const scene2 = document.getElementById('scene2');
  const startBtn = document.getElementById('start-btn');
  const scoreDisplay = document.getElementById('score');
  const yujie2 = document.getElementById('yujie2');
  const bgm = document.getElementById('bgm');
  const dpbltSound = document.getElementById('dpblt');

  // 设置音量
  bgm.volume = 0.1;
  dpbltSound.volume = 1.0;

  // 当前状态
  let currentScene = 1;
  let score = 0;
  let yujieJumping = false;
  let yujieJumpOffset = 0;
  let yujieJumpSpeed = 4;
  const yujieJumpGravity = 0.2;
  let yujieJumpPhase = "falling";

  const bzyInstances = [];

  // ========== 修复：确保按钮存在再绑定事件 ==========
  if (startBtn) {
    startBtn.addEventListener('click', function () {
      console.log("开始按钮被点击！");
      currentScene = 2;
      scene1.style.display = 'none';
      scene2.style.display = 'block';

      // 尝试播放背景音乐（需用户交互）
      bgm.play().catch(e => {
        console.warn("音频播放被阻止，请手动点一下屏幕", e);
      });
    });
  }

  // ========== 游戏主场景点击事件 ==========
  scene2.addEventListener('click', (e) => {
    const yujieRect = yujie2.getBoundingClientRect();
    const clickY = e.clientY;

    // 只响应于姐下半身1/3区域
    const bottomThirdStart = yujieRect.top + (2 * yujieRect.height / 3);

    if (
      e.clientX >= yujieRect.left &&
      e.clientX <= yujieRect.right &&
      clickY >= bottomThirdStart &&
      clickY <= yujieRect.bottom
    ) {
      // 创建巴掌
      const bzy = document.createElement('img');
      bzy.src = './image/bzy.png';
      bzy.classList.add('bzy');
      scene2.appendChild(bzy); // 添加到 scene2 内

      const angle = Math.random() * 180 - 90;
      const left = e.clientX - 30;
      const top = e.clientY - 30;

      bzy.style.left = `${left}px`;
      bzy.style.top = `${top}px`;
      bzy.style.transform = `rotate(${angle}deg)`;

      // 存储实例
      const instance = {
        element: bzy,
        x: left,
        y: top,
        angle: angle,
        jumpOffset: 0,
        jumpSpeed: 4,
        jumpPhase: 'falling',
        jumping: true
      };
      bzyInstances.push(instance);

      // 播放音效
      dpbltSound.currentTime = 0;
      dpbltSound.play();

      // 更新分数
      score++;
      scoreDisplay.textContent = `Score: ${score}`;

      // 触发跳跃（如果没在跳）
      if (!yujieJumping) {
        yujieJumping = true;
        yujieJumpPhase = 'falling';
        yujieJumpSpeed = 4;
        bzyInstances.forEach(b => { b.jumping = true; });
      }
    }
  });

  // ========== 主动画循环 ==========
  function gameLoop() {
    // 于姐跳跃
    if (yujieJumping) {
      if (yujieJumpPhase === 'falling') {
        yujieJumpOffset += yujieJumpSpeed;
        yujieJumpSpeed -= yujieJumpGravity;
        if (yujieJumpSpeed <= 0) {
          yujieJumpPhase = 'rising';
        }
      } else if (yujieJumpPhase === 'rising') {
        yujieJumpSpeed += yujieJumpGravity;
        yujieJumpOffset -= yujieJumpSpeed;
        if (yujieJumpOffset <= 0) {
          yujieJumpOffset = 0;
          yujieJumping = false;
          yujieJumpPhase = 'falling';
          yujieJumpSpeed = 4;
        }
      }
      yujie2.style.transform = `translateY(${-yujieJumpOffset}px)`;
    }

    // 巴掌动画
    bzyInstances.forEach(b => {
      if (b.jumping) {
        if (b.jumpPhase === 'falling') {
          b.jumpOffset += b.jumpSpeed;
          b.jumpSpeed -= yujieJumpGravity;
          if (b.jumpSpeed <= 0) {
            b.jumpPhase = 'rising';
          }
        } else {
          b.jumpSpeed += yujieJumpGravity;
          b.jumpOffset -= b.jumpSpeed;
          if (b.jumpOffset <= 0) {
            b.jumpOffset = 0;
            b.jumping = false;
          }
        }
        b.element.style.transform = `rotate(${b.angle}deg) translateY(${-b.jumpOffset}px)`;
      }
    });

    requestAnimationFrame(gameLoop);
  }

  gameLoop();

  // 允许用户点击任意位置恢复音频（以防被拦截）
  document.body.addEventListener('touchstart', () => {
    if (bgm.paused) bgm.play().catch(() => {});
  }, { once: false });
});
