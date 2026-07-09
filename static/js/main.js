(function () {
	document.addEventListener('submit', function (e) {
		const form = e.target.closest('.like-form');
		if (!form) return;
		e.preventDefault();
		const token = document.querySelector('meta[name="csrf-token"]');
		fetch(form.action, {
			method: 'POST',
			headers: {
				'X-Requested-With': 'XMLHttpRequest',
				'X-CSRFToken': token ? token.content : '',
			},
		}).then(function (r) {
			return r.ok ? r.json() : Promise.reject();
		}).then(function (data) {
			const btn = form.querySelector('.like-btn');
			btn.classList.toggle('liked', data.liked);
			const count = form.querySelector('.like-count');
			if (count) count.textContent = data.count;
			btn.classList.remove('pop');
			void btn.offsetWidth;
			btn.classList.add('pop');
		}).catch(function () {
			form.submit();
		});
	});

	document.querySelectorAll('.alert').forEach(function (alert) {
		setTimeout(function () {
			alert.style.opacity = '0';
			setTimeout(function () { alert.remove(); }, 400);
		}, 5000);
	});

	if ('IntersectionObserver' in window) {
		const observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (entry.isIntersecting) {
					entry.target.style.opacity = '1';
					entry.target.style.transform = 'none';
					observer.unobserve(entry.target);
				}
			});
		}, { threshold: 0.08 });

		document.querySelectorAll('.list-row').forEach(function (row) {
			row.style.opacity = '0';
			row.style.transform = 'translateY(8px)';
			row.style.transition = 'opacity 0.4s cubic-bezier(0.4,0,0.2,1), transform 0.4s cubic-bezier(0.4,0,0.2,1)';
			observer.observe(row);
		});
	}
})();
