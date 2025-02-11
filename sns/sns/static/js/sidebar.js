document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const sidebarLeft = document.getElementById('sidebar-left');
    const sidebarRight = document.getElementById('sidebar-right');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    let touchStartX = 0;
    let touchMoveX = 0;
    let isSwiping = false;
    let activeSidebar = null;

    // スワイプ開始
    function handleTouchStart(event) {
        touchStartX = event.touches[0].clientX;
        isSwiping = false;

        const screenWidth = window.innerWidth;
        // スワイプ開始位置による判定を調整
        if (touchStartX < screenWidth * 0.2) { // 画面の20%まで
            activeSidebar = 'left';
        } else if (touchStartX > screenWidth * 0.8) { // 画面の80%以降
            activeSidebar = 'right';
        } else {
            activeSidebar = null;
        }
    }

    // スワイプ中
    function handleTouchMove(event) {
        if (event.touches.length > 1 || !activeSidebar) return;

        touchMoveX = event.touches[0].clientX;
        const deltaX = touchMoveX - touchStartX;

        // 左サイドバーの処理
        if (activeSidebar === 'left' && deltaX > 0 && !body.classList.contains('sidebar-left-visible') && !body.classList.contains('sidebar-right-visible')) {
            isSwiping = true;
            event.preventDefault();

            const translateX = Math.min(deltaX, 280);
            sidebarLeft.style.transform = `translateX(${translateX - 280}px)`;
            updateOverlay(translateX / 280);
        }
        // 右サイドバーの処理
        else if (activeSidebar === 'right' && deltaX < 0 && !body.classList.contains('sidebar-right-visible') && !body.classList.contains('sidebar-left-visible')) {
            isSwiping = true;
            event.preventDefault();

            const translateX = Math.max(deltaX, -280);
            sidebarRight.style.transform = `translateX(${translateX + 280}px)`;
            updateOverlay(Math.abs(translateX) / 280);
        }
    }

    // スワイプ終了
    function handleTouchEnd() {
        if (!isSwiping || !activeSidebar) return;

        const deltaX = touchMoveX - touchStartX;
        
        if (activeSidebar === 'left' && deltaX > 50) { // 閾値を50pxに下げる
            showSidebar('left');
        } else if (activeSidebar === 'right' && deltaX < -50) { // 閾値を50pxに下げる
            showSidebar('right');
        } else {
            hideSidebar(activeSidebar);
        }

        isSwiping = false;
        activeSidebar = null;
    }

    // オーバーレイの表示を更新
    function updateOverlay(opacity) {
        sidebarOverlay.style.display = 'block';
        sidebarOverlay.style.opacity = opacity * 0.5;
    }

    // サイドバーを表示
    function showSidebar(side) {
        // 片方のサイドバーが表示されている場合、もう片方を閉じる
        if (side === 'left' && body.classList.contains('sidebar-right-visible')) {
            hideSidebar('right');
        } else if (side === 'right' && body.classList.contains('sidebar-left-visible')) {
            hideSidebar('left');
        }

        if (side === 'left') {
            body.classList.add('sidebar-left-visible');
            sidebarLeft.style.transform = '';
        } else {
            body.classList.add('sidebar-right-visible');
            sidebarRight.style.transform = '';
        }
        sidebarOverlay.style.opacity = '';
    }

    // サイドバーを非表示
    function hideSidebar(side) {
        if (side === 'left') {
            body.classList.remove('sidebar-left-visible');
            sidebarLeft.style.transform = 'translateX(-100%)';
        } else {
            body.classList.remove('sidebar-right-visible');
            sidebarRight.style.transform = 'translateX(100%)';
        }
        sidebarOverlay.style.opacity = '0';
        
        // アニメーション完了後にオーバーレイを非表示
        setTimeout(() => {
            if (!body.classList.contains('sidebar-left-visible') && 
                !body.classList.contains('sidebar-right-visible')) {
                sidebarOverlay.style.display = 'none';
            }
        }, 300);
    }

    // オーバーレイクリックで両方のサイドバーを閉じる
    sidebarOverlay.addEventListener('click', () => {
        if (body.classList.contains('sidebar-left-visible')) {
            hideSidebar('left');
        }
        if (body.classList.contains('sidebar-right-visible')) {
            hideSidebar('right');
        }
    });

    // タッチイベントの登録
    document.addEventListener('touchstart', handleTouchStart, { passive: true });
    document.addEventListener('touchmove', handleTouchMove, { passive: false });
    document.addEventListener('touchend', handleTouchEnd);

    // メッセージの自動消去
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        message.style.transition = 'opacity 0.5s ease-in-out';
        
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000);
    });
});
