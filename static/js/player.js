(function () {
	const bar = document.getElementById('player');
	const audio = document.getElementById('player-audio');
	if (!bar || !audio) return;

	const el = {
		cover: document.getElementById('player-cover'),
		title: document.getElementById('player-title'),
		artist: document.getElementById('player-artist'),
		toggle: document.getElementById('player-toggle'),
		progress: document.getElementById('player-progress'),
		fill: document.getElementById('player-fill'),
		current: document.getElementById('player-current'),
		duration: document.getElementById('player-duration'),
		close: document.getElementById('player-close'),
	};

	const ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
	const ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>';

	function fmt(s) {
		if (!isFinite(s) || s < 0) return '0:00';
		const m = Math.floor(s / 60);
		const sec = Math.floor(s % 60);
		return m + ':' + String(sec).padStart(2, '0');
	}

	function syncIcon() {
		el.toggle.innerHTML = audio.paused ? ICON_PLAY : ICON_PAUSE;
	}

	const STORE_KEY = 'b2b_player';

	function saveState() {
		try {
			sessionStorage.setItem(STORE_KEY, JSON.stringify({
				src: audio.getAttribute('src') || '',
				title: el.title.textContent,
				artist: el.artist.textContent,
				time: audio.currentTime || 0,
				playing: !audio.paused,
			}));
		} catch (e) {}
	}

	function clearState() {
		try { sessionStorage.removeItem(STORE_KEY); } catch (e) {}
	}

	function registerPlay(id) {
		if (!id) return;
		const token = document.querySelector('meta[name="csrf-token"]');
		fetch('/music/songs/' + id + '/played/', {
			method: 'POST',
			headers: { 'X-CSRFToken': token ? token.content : '' },
		}).then(function (r) {
			return r.ok ? r.json() : null;
		}).then(function (data) {
			if (!data) return;
			document.querySelectorAll('.play-count[data-song="' + id + '"]').forEach(function (el) {
				el.textContent = data.play_count;
			});
		}).catch(function () {});
	}

	function play(data) {
		if (audio.getAttribute('src') !== data.src) {
			audio.src = data.src;
		}
		el.title.textContent = data.title || '';
		el.artist.textContent = data.artist || '';
		bar.classList.add('is-visible');
		document.body.classList.add('is-playing');
		audio.play().catch(function () {});
		registerPlay(data.id);
		saveState();
	}

	document.addEventListener('click', function (e) {
		const btn = e.target.closest('.play-btn');
		if (!btn) return;
		e.preventDefault();
		e.stopPropagation();
		play({ src: btn.dataset.src, title: btn.dataset.title, artist: btn.dataset.artist, id: btn.dataset.id });
	});

	el.toggle.addEventListener('click', function () {
		if (audio.paused) {
			audio.play().catch(function () {});
		} else {
			audio.pause();
		}
	});

	audio.addEventListener('play', function () { syncIcon(); saveState(); });
	audio.addEventListener('pause', function () { syncIcon(); saveState(); });
	audio.addEventListener('ended', function () { syncIcon(); clearState(); });

	audio.addEventListener('timeupdate', function () {
		const pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
		el.fill.style.width = pct + '%';
		el.current.textContent = fmt(audio.currentTime);
		el.duration.textContent = fmt(audio.duration);
		saveState();
	});

	el.progress.addEventListener('click', function (e) {
		const rect = el.progress.getBoundingClientRect();
		const ratio = (e.clientX - rect.left) / rect.width;
		if (audio.duration) audio.currentTime = ratio * audio.duration;
	});

	el.close.addEventListener('click', function () {
		audio.pause();
		bar.classList.remove('is-visible');
		document.body.classList.remove('is-playing');
		clearState();
	});

	document.addEventListener('keydown', function (e) {
		if (e.code === 'Space' && bar.classList.contains('is-visible')) {
			const tag = document.activeElement ? document.activeElement.tagName : '';
			if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'BUTTON') return;
			e.preventDefault();
			audio.paused ? audio.play().catch(function () {}) : audio.pause();
		}
	});

	(function restore() {
		let data;
		try { data = JSON.parse(sessionStorage.getItem(STORE_KEY) || 'null'); } catch (e) { return; }
		if (!data || !data.src) return;
		el.title.textContent = data.title || '';
		el.artist.textContent = data.artist || '';
		audio.src = data.src;
		bar.classList.add('is-visible');
		document.body.classList.add('is-playing');
		audio.addEventListener('loadedmetadata', function () {
			if (data.time && isFinite(data.time)) {
				try { audio.currentTime = data.time; } catch (e) {}
			}
			if (data.playing) audio.play().catch(function () {});
		}, { once: true });
	})();

	syncIcon();
})();
