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

function selectCalendarHour(button) {
    if (button.disabled) return;

    document.querySelectorAll('.hour-slot-btn').forEach(function (btn) {
        btn.classList.remove('border-[#00AEEF]', 'bg-sky-50', 'ring-2', 'ring-[#00AEEF]');
    });
    button.classList.add('border-[#00AEEF]', 'bg-sky-50', 'ring-2', 'ring-[#00AEEF]');

    calendarSelectedTime = button.dataset.time;
    calendarSelectedLabel = button.textContent.trim();

    const confirmBtn = document.getElementById('calendar-confirm-btn');
    if (confirmBtn) confirmBtn.disabled = false;
}

function disablePastHourSlots() {
    const dateInput = document.getElementById('calendar-date-input');
    if (!dateInput || !dateInput.value) return;

    const now = new Date();
    const todayValue = now.getFullYear() + '-'
        + String(now.getMonth() + 1).padStart(2, '0') + '-'
        + String(now.getDate()).padStart(2, '0');

    if (dateInput.value !== todayValue) return;

    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    document.querySelectorAll('#calendar-hours-slots .hour-slot-btn').forEach(function (btn) {
        const [hours, minutes] = btn.dataset.time.split(':').map(Number);
        if ((hours * 60 + minutes) <= currentMinutes) {
            btn.disabled = true;
            btn.classList.add('border-slate-100', 'text-slate-300', 'bg-slate-50', 'cursor-not-allowed', 'line-through');
            btn.classList.remove('border-slate-200', 'text-slate-700', 'hover:border-[#00AEEF]', 'hover:bg-sky-50');
        }
    });
}

document.body.addEventListener('htmx:afterSwap', function (evt) {
    if (!evt.target || evt.target.id !== 'calendar-hours-slots') return;
    resetCalendarHourSelection();
    disablePastHourSlots();
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
