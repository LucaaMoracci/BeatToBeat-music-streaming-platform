(function () {
	const audioInput = document.getElementById('id_audio_file');
	const durationInput = document.getElementById('id_duration');
	if (!audioInput || !durationInput) return;

	function format(seconds) {
		const h = Math.floor(seconds / 3600);
		const m = Math.floor((seconds % 3600) / 60);
		const s = Math.floor(seconds % 60);
		const pad = function (n) { return String(n).padStart(2, '0'); };
		return (h > 0 ? pad(h) + ':' : '') + pad(m) + ':' + pad(s);
	}

	audioInput.addEventListener('change', function () {
		const file = audioInput.files[0];
		if (!file) return;
		const url = URL.createObjectURL(file);
		const probe = new Audio(url);
		probe.addEventListener('loadedmetadata', function () {
			if (isFinite(probe.duration)) {
				durationInput.value = format(probe.duration);
			}
			URL.revokeObjectURL(url);
		});
		probe.addEventListener('error', function () {
			URL.revokeObjectURL(url);
		});
	});
})();
