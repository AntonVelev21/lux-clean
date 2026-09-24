let calendarSelectedTime = null;
let calendarSelectedLabel = null;

function openCalendarModal() {
    const backdrop = document.getElementById('calendar-modal-backdrop');
    if (!backdrop) return;
    backdrop.classList.remove('hidden');
    backdrop.classList.add('flex');
}

function closeCalendarModal() {
    const backdrop = document.getElementById('calendar-modal-backdrop');
    if (!backdrop) return;
    backdrop.classList.add('hidden');
    backdrop.classList.remove('flex');
}

function resetCalendarHourSelection() {
    calendarSelectedTime = null;
    calendarSelectedLabel = null;

    const confirmBtn = document.getElementById('calendar-confirm-btn');
    if (confirmBtn) confirmBtn.disabled = true;
}


function initCalendarHourPicker() {
    const dataEl = document.getElementById('calendar-slots-data');
    const hourCol = document.getElementById('hour-picker-col');
    const minuteCol = document.getElementById('minute-picker-col');
    const confirmBtn = document.getElementById('calendar-confirm-btn');
    const invalidMsg = document.getElementById('calendar-invalid-msg');

    if (!dataEl || !hourCol || !minuteCol) return;

    const slots = JSON.parse(dataEl.textContent);


    const availability = {};
    const hours = [];

    slots.forEach(function (slot) {
        const [h, m] = slot.time.split(':');
        if (!availability[h]) {
            availability[h] = {};
            hours.push(h);
        }
        availability[h][m] = slot.available;
    });

    const minutes = ['00', '30'];
    const isPastSlot = buildPastSlotChecker();

    function isSlotUsable(h, m) {
        return !!(h && availability[h] && availability[h][m]) && !isPastSlot(h, m);
    }

    function buildColumn(col, values) {
        col.innerHTML = '';
        values.forEach(function (v) {
            const item = document.createElement('div');
            item.className = 'calendar-picker-item';
            item.dataset.value = v;
            item.textContent = v;
            col.appendChild(item);
        });
    }

    buildColumn(hourCol, hours);
    buildColumn(minuteCol, minutes);

    let selectedHour = hours.length ? hours[0] : null;
    let selectedMinute = minutes[0];

    function refreshValidity() {
        Array.from(minuteCol.children).forEach(function (item) {
            const invalid = !isSlotUsable(selectedHour, item.dataset.value);
            item.classList.toggle('is-invalid', invalid);
            item.classList.toggle('is-selected', item.dataset.value === selectedMinute && !invalid);
        });
        Array.from(hourCol.children).forEach(function (item) {
            item.classList.toggle('is-selected', item.dataset.value === selectedHour);
        });

        const usable = isSlotUsable(selectedHour, selectedMinute);

        calendarSelectedTime = usable ? (selectedHour + ':' + selectedMinute) : null;
        calendarSelectedLabel = usable ? (selectedHour + ':' + selectedMinute) : null;

        if (confirmBtn) confirmBtn.disabled = !usable;
        if (invalidMsg) invalidMsg.classList.toggle('hidden', usable);
    }

    function centerOffset(col, item) {
        return item.offsetTop - (col.clientHeight / 2 - item.clientHeight / 2);
    }

    function scrollToValue(col, value, smooth) {
        const item = Array.from(col.children).find(function (i) { return i.dataset.value === value; });
        if (!item) return;
        const top = centerOffset(col, item);
        if (smooth) {
            col.scrollTo({ top: top, behavior: 'smooth' });
        } else {
            col.scrollTop = top;
        }
    }

    function closestItem(col) {
        const center = col.scrollTop + col.clientHeight / 2;
        let closest = null;
        let closestDist = Infinity;
        Array.from(col.children).forEach(function (item) {
            const dist = Math.abs((item.offsetTop + item.clientHeight / 2) - center);
            if (dist < closestDist) {
                closestDist = dist;
                closest = item;
            }
        });
        return closest;
    }

    function onScrollEnd(col, onPick) {
        let timeout = null;
        col.addEventListener('scroll', function () {
            clearTimeout(timeout);
            timeout = setTimeout(function () {
                const closest = closestItem(col);
                if (closest) onPick(closest.dataset.value);
            }, 120);
        });
    }

    function attachClickSelect(col) {
        col.addEventListener('click', function (evt) {
            const item = evt.target.closest('.calendar-picker-item');
            if (!item) return;
            scrollToValue(col, item.dataset.value, true);
        });
    }

    function attachPointerDrag(col) {
        let dragging = false;
        let startY = 0;
        let startScrollTop = 0;
        let moved = 0;

        col.addEventListener('pointerdown', function (evt) {
            if (evt.pointerType === 'touch') return;
            dragging = true;
            moved = 0;
            startY = evt.clientY;
            startScrollTop = col.scrollTop;
            col.classList.add('is-dragging');
            col.setPointerCapture(evt.pointerId);
        });

        col.addEventListener('pointermove', function (evt) {
            if (!dragging) return;
            const delta = evt.clientY - startY;
            moved = Math.max(moved, Math.abs(delta));
            col.scrollTop = startScrollTop - delta;
        });

        function endDrag(evt) {
            if (!dragging) return;
            dragging = false;
            col.classList.remove('is-dragging');
            try { col.releasePointerCapture(evt.pointerId); } catch (e) { /* no-op */ }

            const closest = closestItem(col);
            if (closest) scrollToValue(col, closest.dataset.value, true);
        }

        col.addEventListener('pointerup', endDrag);
        col.addEventListener('pointercancel', endDrag);
        col.addEventListener('pointerleave', function (evt) {
            if (dragging) endDrag(evt);
        });
    }

    attachClickSelect(hourCol);
    attachClickSelect(minuteCol);
    attachPointerDrag(hourCol);
    attachPointerDrag(minuteCol);

    onScrollEnd(hourCol, function (h) {
        selectedHour = h;
        refreshValidity();
    });
    onScrollEnd(minuteCol, function (m) {
        selectedMinute = m;
        refreshValidity();
    });

    if (selectedHour) {
        scrollToValue(hourCol, selectedHour, false);
        scrollToValue(minuteCol, selectedMinute, false);
        refreshValidity();
    } else if (confirmBtn) {
        confirmBtn.disabled = true;
    }
}

function buildPastSlotChecker() {
    const dateInput = document.getElementById('calendar-date-input');
    if (!dateInput || !dateInput.value) return function () { return false; };

    const now = new Date();
    const todayValue = now.getFullYear() + '-'
        + String(now.getMonth() + 1).padStart(2, '0') + '-'
        + String(now.getDate()).padStart(2, '0');

    if (dateInput.value !== todayValue) return function () { return false; };

    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    return function (h, m) {
        return (Number(h) * 60 + Number(m)) <= currentMinutes;
    };
}

document.body.addEventListener('htmx:afterSwap', function (evt) {
    if (!evt.target || evt.target.id !== 'calendar-hours-slots') return;
    resetCalendarHourSelection();
    initCalendarHourPicker();
});

document.addEventListener('DOMContentLoaded', function () {
    initCalendarHourPicker();
});

function confirmCalendarSelection() {
    const dateInput = document.getElementById('calendar-date-input');
    const hiddenInput = document.getElementById('id_requested_date');
    const display = document.getElementById('selected-datetime-display');

    if (!dateInput || !dateInput.value || !calendarSelectedTime || !hiddenInput) return;

    hiddenInput.value = dateInput.value + 'T' + calendarSelectedTime;
    hiddenInput.setAttribute('value', hiddenInput.value);

    if (display) {
        const [year, month, day] = dateInput.value.split('-');
        display.textContent = day + '.' + month + '.' + year + ' г. в ' + calendarSelectedLabel + ' ч.';
        display.classList.remove('text-slate-400');
        display.classList.add('text-slate-700', 'font-semibold');
    }

    closeCalendarModal();
}