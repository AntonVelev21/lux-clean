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
    const originalTotalDisplay = document.getElementById('original-price-display'); // Добавено за задрасканата цена

    function calculateTotal() {
        if (!totalDisplay) return;

        let originalTotal = 0;
        let finalTotal = 0;
        let selectedServicesHTML = '';

        quantityInputs.forEach(input => {
            const qty = parseInt(input.value) || 0;
            const price = parseFloat(input.dataset.price) || 0;
            const name = input.dataset.name || 'Услуга';

            if (qty > 0) {
                const lineTotal = qty * price;
                originalTotal += lineTotal;

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

        finalTotal = originalTotal;

        if (originalTotal >= 200) {
            finalTotal = originalTotal * 0.95;

            selectedServicesHTML += `
                <div class="flex justify-between items-center bg-green-50 p-3 rounded-xl border border-green-200 shadow-sm transition-all gap-3 mt-2">
                    <div class="flex-1 min-w-0">
                        <h5 class="text-green-800 font-bold text-sm truncate" title="Отстъпка">Отстъпка</h5>
                        <p class="text-green-600 text-xs mt-0.5">За поръчка над 200 €</p>
                    </div>
                    <span class="text-green-600 font-black text-sm whitespace-nowrap flex-shrink-0">-5 % €</span>
                </div>
            `;

            if (originalTotalDisplay) {
                originalTotalDisplay.innerText = originalTotal.toFixed(2) + ' €';
                originalTotalDisplay.classList.remove('hidden');
            }
        } else {
            if (originalTotalDisplay) {
                originalTotalDisplay.classList.add('hidden');
            }
        }

        totalDisplay.innerText = finalTotal.toFixed(2);

        if (servicesContainer) {
            if (originalTotal > 0) {
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

function initCalculatorSteps() {
    const calculatorStep = document.getElementById('calculator-step');
    const detailsStep = document.getElementById('details-step');
    const continueBtn = document.getElementById('continue-to-details-btn');
    const backBtn = document.getElementById('back-to-calculator-btn');
    const continueError = document.getElementById('continue-error');
    const totalDisplay = document.getElementById('total-price-display');

    if (!calculatorStep || !detailsStep || !continueBtn) return;

    continueBtn.onclick = function() {
        const total = totalDisplay ? parseFloat(totalDisplay.innerText) || 0 : 0;

        if (total <= 0) {
            if (continueError) continueError.classList.remove('hidden');
            return;
        }

        if (continueError) continueError.classList.add('hidden');
        calculatorStep.classList.add('hidden');
        detailsStep.classList.remove('hidden');
        detailsStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    if (backBtn) {
        backBtn.onclick = function() {
            detailsStep.classList.add('hidden');
            calculatorStep.classList.remove('hidden');
            calculatorStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
        };
    }
}

initCalculatorSteps();

if (!window.calculatorStepsListenerAttached) {
    document.body.addEventListener('htmx:load', function() {
        initCalculatorSteps();
    });
    window.calculatorStepsListenerAttached = true;
}