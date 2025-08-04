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
     * Checks if the District/Region number is a real district or region
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


    /**
     * Scrapes tables and displays on UI
     */
    document.getElementById("scrapeForm").addEventListener("submit", async (e) => {
        console.log("Start Scraping...");

        e.preventDefault(); // Prevent page reload since that's submit's default

        const form = e.target;

        const year = form.year.value;
        const event = form.event.value;
        const conference = form.conference.value;
        const level = form.level.value;
        const levelInput = level === "district" ? form.districtInput.value 
                            : level === "region" ? form.regionInput.value 
                            : level === "state" ? "1" : "";

        // Checks that all fields are completed
        if (!conference) {
            alert("Please select a conference.");
            return;
        }
        if (!level) {
            alert("Please select a level.");
            return;
        }
        if (levelInput === "") {
            alert(`Please input a ${level} number`);
            return;
        }
        
        const payload = {
            year: year,
            event: event,
            conference: conference,
            level: level,
            levelInput: levelInput
        };

        console.log("Sending paylod to server: ", payload);

        try {
            const response = await fetch("http://127.0.0.1:5000/scrape", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error("Failed to scrape data");
            }

            const data = await response.json();

            renderTable("individualTableContainer", data.individual_results);
            renderTable("teamTableContainer", data.team_results);

            console.log("Data loaded successfully!");
        }
        catch (error) {
            console.error("Scrape failed:", error);
            alert("Something went wrong during scraping. Check console for details.");
        }
    });


    /**
     * adds table elements to HTML to display
     * 
     * @param {*} containerId Div container in HTML where table will be displayed
     * @param {*} data JSON of table data
     */
    function renderTable(containerId, data) {
        const container = document.getElementById(containerId);
        container.innerHTML = "";   // Clear previous

        if (!data.length) {
            container.innerHTML = "<p>No data found</p>";
            return;
        }

        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElementNS("tbody");

        //Create header row
        const headers = Object.keys(data[0]);
        const trHead = document.createElement("tr");
        headers.forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            trHead.appendChild(th);
        });
        thead.appendChild(trHead);

        // Create body rows
        data.forEach(row => {
            const tr = document.createElement("tr");
            headers.forEach(h => {
                const td = document.createElement("td");
                td.textContent = row[h];
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });

        table.appendChild(thead);
        table.appendChild(tbody);
        container.appendChild(table);
    }
});