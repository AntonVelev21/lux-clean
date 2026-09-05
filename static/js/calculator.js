function initCalculator() {
    const accordions = document.querySelectorAll('.accordion-trigger');
    if (accordions.length === 0) return;

    accordions.forEach(acc => {
        acc.onclick = function() {
            const content = this.nextElementSibling;
            const arrow = this.querySelector('.arrow-icon');
            content.classList.toggle('hidden');
            arrow.classList.toggle('rotate-180');
        };
    });

    const quantityInputs = document.querySelectorAll('.variant-input');
    const minusBtns = document.querySelectorAll('.qty-btn.minus');
    const plusBtns = document.querySelectorAll('.qty-btn.plus');
    const totalDisplay = document.getElementById('total-price-display');
    const servicesContainer = document.getElementById('selected-services-container');

    function calculateTotal() {
        if (!totalDisplay) return;

        let total = 0;
        let selectedServicesHTML = '';

        quantityInputs.forEach(input => {
            const qty = parseInt(input.value) || 0;
            const price = parseFloat(input.dataset.price) || 0;
            const name = input.dataset.name || 'Услуга';

            if (qty > 0) {
                const lineTotal = qty * price;
                total += lineTotal;

                selectedServicesHTML += `
                    <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl border border-slate-100 shadow-sm transition-all gap-3">
                        <div class="flex-1 min-w-0">
                            <h5 class="text-slate-800 font-bold text-sm truncate" title="${name}">${name}</h5>
                            <p class="text-slate-500 text-xs mt-0.5">${qty} бр. × ${price.toFixed(2)} €</p>
                        </div>
                        <span class="text-[#00AEEF] font-black text-sm whitespace-nowrap flex-shrink-0">${lineTotal.toFixed(2)} €</span>
                    </div>
                `;
            }
        });

        totalDisplay.innerText = total.toFixed(2);

        if (servicesContainer) {
            if (total > 0) {
                servicesContainer.innerHTML = selectedServicesHTML;
            } else {
                servicesContainer.innerHTML = `
                    <div class="text-slate-400 italic text-sm p-4 bg-slate-50 rounded-xl border border-slate-100 text-center">
                        Все още нямате избрани услуги.
                    </div>
                `;
            }
        }

        totalDisplay.classList.add('text-[#00AEEF]', 'scale-110');
        setTimeout(() => {
            totalDisplay.classList.remove('text-[#00AEEF]', 'scale-110');
        }, 200);
    }

    minusBtns.forEach(btn => {
        btn.onclick = function() {
            const input = this.nextElementSibling;
            let val = parseInt(input.value) || 0;
            if (val > 0) {
                input.value = val - 1;
                input.setAttribute('value', input.value);
                calculateTotal();
            }
        };
    });

    plusBtns.forEach(btn => {
        btn.onclick = function() {
            const input = this.previousElementSibling;
            let val = parseInt(input.value) || 0;
            input.value = val + 1;
            input.setAttribute('value', input.value);
            calculateTotal();
        };
    });

    quantityInputs.forEach(input => {
        input.oninput = function() {
            if (this.value < 0 || isNaN(this.value) || this.value === '') {
                this.value = 0;
            }
            input.setAttribute('value', this.value);
            calculateTotal();
        };
    });

    calculateTotal();
}

initCalculator();

if (!window.calculatorListenerAttached) {
    document.body.addEventListener('htmx:load', function() {
        initCalculator();
    });
    window.calculatorListenerAttached = true;
}