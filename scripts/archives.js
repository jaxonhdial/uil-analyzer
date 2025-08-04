document.addEventListener("DOMContentLoaded", () => {
    const districtRadio = document.getElementById("levelDistrict");
    const regionRadio = document.getElementById("levelRegion");
    const stateRadio = document.getElementById("levelState");

    const districtInputContainer = document.getElementById("districtInputContainer");
    const regionInputContainer = document.getElementById("regionInputContainer");

    const districtInput = document.getElementById("districtInput");
    const regionInput = document.getElementById("regionInput");

    /**
     * Updates the visibility of the number input field when a 
     * level radio button is checked
     */
    const updateNumberInputVisibility = () => {
        console.log("Updating Visibility");
        if (districtRadio.checked) {
            districtInputContainer.style.display = "inline";
            regionInputContainer.style.display = "none";
            regionInput.value = "";
        }
        else if (regionRadio.checked) {
            regionInputContainer.style.display = "inline";
            districtInputContainer.style.display = "none";
            districtInput.value = "";
        }
        else {
            districtInputContainer.style.display = "none";
            regionInputContainer.style.display = "none";
            districtInput.value = "";
            regionInput.value = "";
        }
    };

    [districtRadio, regionRadio, stateRadio].forEach(radio => {
        radio.addEventListener("change", updateNumberInputVisibility);
    });


    /**
     * 
     * @param {number} input - number from input field for district or region level
     * @param {number} min - minimum value allowed in field
     * @param {number} max - maximum value allowed in field
     */
    const validateNumber = (input, min, max) => {
        // despite the input type being number, input.value is always type string in JS
        const val = input.value.trim();
        if (val === "") {
            return;
        }

        const num = Number(val);
        if (Number.isNaN(num) || num < min) {
            input.value = min;
        }
        else if (num > max) {
            input.value = max;
        }
        else {
            input.value = Math.floor(num); // force integer
        }
    };

    districtInput.addEventListener("input", () => {
        const minDistrict = 1;
        const maxDistrict = 32;
        console.log("Invalid District Number. Rejected value:", districtInput.value);
        validateNumber(districtInput, minDistrict, maxDistrict);
    });

    regionInput.addEventListener("input", () => {
        const minRegion = 1;
        const maxRegion = 4;
        console.log("Invalid Region Number. Rejected value:", regionInput.value);
        validateNumber(regionInput, minRegion, maxRegion);
    });
});