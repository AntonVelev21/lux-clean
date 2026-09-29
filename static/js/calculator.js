function initCalculator() {
    const accordions = document.querySelectorAll('.accordion-trigger');

    if (accordions.length === 0) {
        return;
    }

    accordions.forEach((acc) => {
        if (acc.dataset.initialized === 'true') {
            return;
        }

        acc.dataset.initialized = 'true';

        acc.addEventListener('click', function () {
            const content = this.nextElementSibling;
            const arrow = this.querySelector('.arrow-icon');

            if (!content) {
                return;
            }

            content.classList.toggle('hidden');

            if (arrow) {
                arrow.classList.toggle('rotate-180');
            }
        });
    });


    const quantityInputs = document.querySelectorAll('.variant-input');
    const minusBtns = document.querySelectorAll('.qty-btn.minus');
    const plusBtns = document.querySelectorAll('.qty-btn.plus');

    const totalDisplay = document.getElementById(
        'total-price-display'
    );

    const servicesContainer = document.getElementById(
        'selected-services-container'
    );

    const originalTotalDisplay = document.getElementById(
        'original-price-display'
    );


    function calculateTotal() {
        if (!totalDisplay) {
            return;
        }

        let originalTotal = 0;
        let finalTotal = 0;

        let selectedServicesHTML = '';


        quantityInputs.forEach((input) => {
            let qty = parseInt(input.value, 10) || 0;

            const max = parseInt(input.max, 10) || 99;

            qty = Math.max(0, Math.min(qty, max));

            input.value = qty;

            const price =
                parseFloat(input.dataset.price) || 0;

            const name =
                input.dataset.name || 'Услуга';


            if (qty > 0) {
                const lineTotal = qty * price;

                originalTotal += lineTotal;


                selectedServicesHTML += `
                    <div class="flex justify-between items-center bg-slate-50 p-3 rounded-xl border border-slate-100 shadow-sm transition-all gap-3">

                        <div class="flex-1 min-w-0">
                            <h5
                                class="text-slate-800 font-bold text-sm truncate"
                                title="${name}"
                            >
                                ${name}
                            </h5>

                            <p class="text-slate-500 text-xs mt-0.5">
                                ${qty} бр. × ${price.toFixed(2)} €
                            </p>
                        </div>

                        <span class="text-[#00AEEF] font-black text-sm whitespace-nowrap flex-shrink-0">
                            ${lineTotal.toFixed(2)} €
                        </span>

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
                        <h5
                            class="text-green-800 font-bold text-sm truncate"
                            title="Отстъпка"
                        >
                            Отстъпка
                        </h5>

                        <p class="text-green-600 text-xs mt-0.5">
                            За поръчка над 200 €
                        </p>
                    </div>

                    <span class="text-green-600 font-black text-sm whitespace-nowrap flex-shrink-0">
                        -5%
                    </span>

                </div>
            `;


            if (originalTotalDisplay) {
                originalTotalDisplay.innerText =
                    originalTotal.toFixed(2) + ' €';

                originalTotalDisplay.classList.remove('hidden');
            }

        } else {

            if (originalTotalDisplay) {
                originalTotalDisplay.classList.add('hidden');
            }
        }


        totalDisplay.innerText =
            finalTotal.toFixed(2);


        if (servicesContainer) {

            if (originalTotal > 0) {

                servicesContainer.innerHTML =
                    selectedServicesHTML;

            } else {

                servicesContainer.innerHTML = `
                    <div class="text-slate-400 italic text-sm p-4 bg-slate-50 rounded-xl border border-slate-100 text-center">
                        Все още нямате избрани услуги.
                    </div>
                `;
            }
        }


        totalDisplay.classList.add(
            'text-[#00AEEF]',
            'scale-110'
        );

        setTimeout(() => {
            totalDisplay.classList.remove(
                'text-[#00AEEF]',
                'scale-110'
            );
        }, 200);
    }


    minusBtns.forEach((btn) => {

        if (btn.dataset.initialized === 'true') {
            return;
        }

        btn.dataset.initialized = 'true';

        btn.addEventListener('click', function () {

            const input = this.nextElementSibling;

            if (!input) {
                return;
            }

            let val =
                parseInt(input.value, 10) || 0;

            if (val > 0) {
                val--;

                input.value = val;
                input.setAttribute('value', val);

                calculateTotal();
            }
        });
    });


    plusBtns.forEach((btn) => {

        if (btn.dataset.initialized === 'true') {
            return;
        }

        btn.dataset.initialized = 'true';

        btn.addEventListener('click', function () {

            const input = this.previousElementSibling;

            if (!input) {
                return;
            }

            let val =
                parseInt(input.value, 10) || 0;

            const max =
                parseInt(input.max, 10) || 99;

            if (val < max) {
                val++;

                input.value = val;
                input.setAttribute('value', val);

                calculateTotal();
            }
        });
    });


    quantityInputs.forEach((input) => {

        if (input.dataset.initialized === 'true') {
            return;
        }

        input.dataset.initialized = 'true';

        input.addEventListener('input', function () {

            const max =
                parseInt(this.max, 10) || 99;

            let value =
                parseInt(this.value, 10);

            if (isNaN(value) || value < 0) {
                value = 0;
            }

            if (value > max) {
                value = max;
            }

            this.value = value;

            this.setAttribute(
                'value',
                value
            );

            calculateTotal();
        });
    });


    calculateTotal();
}


function initCalculatorSteps() {

    const calculatorStep =
        document.getElementById('calculator-step');

    const detailsStep =
        document.getElementById('details-step');

    const continueBtn =
        document.getElementById(
            'continue-to-details-btn'
        );

    const backBtn =
        document.getElementById(
            'back-to-calculator-btn'
        );

    const continueError =
        document.getElementById(
            'continue-error'
        );

    const totalDisplay =
        document.getElementById(
            'total-price-display'
        );


    if (
        !calculatorStep ||
        !detailsStep ||
        !continueBtn
    ) {
        return;
    }


    if (continueBtn.dataset.initialized !== 'true') {

        continueBtn.dataset.initialized = 'true';

        continueBtn.addEventListener(
            'click',
            () => {

                const total =
                    totalDisplay
                        ? parseFloat(totalDisplay.innerText) || 0
                        : 0;


                if (total <= 0) {

                    if (continueError) {
                        continueError.classList.remove('hidden');
                    }

                    return;
                }


                if (continueError) {
                    continueError.classList.add('hidden');
                }


                calculatorStep.classList.add('hidden');

                detailsStep.classList.remove('hidden');

                detailsStep.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        );
    }


    if (
        backBtn &&
        backBtn.dataset.initialized !== 'true'
    ) {

        backBtn.dataset.initialized = 'true';

        backBtn.addEventListener(
            'click',
            () => {

                detailsStep.classList.add('hidden');

                calculatorStep.classList.remove('hidden');

                calculatorStep.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        );
    }
}


function initializeCalculatorPage() {
    initCalculator();
    initCalculatorSteps();
}

initializeCalculatorPage();