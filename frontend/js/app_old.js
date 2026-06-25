// ===========================================================
// AI Powered Vehicle Valuation System
// Frontend Application
// Author : Srivignesh
// ===========================================================

const API_URL =
"https://orange-funicular-5g4q579x4qqphw9g-8000.app.github.dev";

// ===========================================================
// Load Available Brands
// ===========================================================

async function loadBrands() {

    try {

        const response = await fetch(`${API_URL}/brands`);

        const brands = await response.json();

        const brandSelect = document.getElementById("oem");

        brandSelect.innerHTML =
            '<option value="">Select Brand</option>';

        brands.forEach((brand) => {

            brandSelect.innerHTML +=
                `<option value="${brand}">${brand}</option>`;

        });

    }

    catch (error) {

        console.log(error);

    }

}

// ===========================================================
// Load Models
// ===========================================================

document.getElementById("oem").addEventListener(

    "change",

    async function () {

        const brand = this.value;

        const response =
            await fetch(`${API_URL}/models/${brand}`);

        const models =
            await response.json();

        const modelSelect =
            document.getElementById("model");

        modelSelect.innerHTML =
            '<option value="">Select Model</option>';

        models.forEach((model) => {

            modelSelect.innerHTML +=
                `<option value="${model}">${model}</option>`;

        });

    }

);

// ===========================================================
// Load Vehicle Details
// ===========================================================

document.getElementById("model").addEventListener(

    "change",

    async function () {

        const brand =
            document.getElementById("oem").value;

        const model =
            this.value;

        const response =
            await fetch(`${API_URL}/vehicle/${brand}/${model}`);

        const vehicle =
            await response.json();

        // Variant

        const variant =
            document.getElementById("variant");

        variant.innerHTML = "";

        vehicle.variants.forEach((item) => {

            variant.innerHTML +=
                `<option value="${item}">${item}</option>`;

        });

        // Fuel

        const fuel =
            document.getElementById("fuel");

        fuel.innerHTML = "";

        vehicle.fuel.forEach((item) => {

            fuel.innerHTML +=
                `<option value="${item}">${item}</option>`;

        });

        // Transmission

        const transmission =
            document.getElementById("transmission");

        transmission.innerHTML = "";

        vehicle.transmission.forEach((item) => {

            transmission.innerHTML +=
                `<option value="${item}">${item}</option>`;

        });

        // Body

        document.getElementById("body").value =
            vehicle.body;

    }

);

// ===========================================================
// Prediction
// ===========================================================

document.getElementById("valuationForm").addEventListener(

    "submit",

    async function (event) {

        event.preventDefault();

        // Loading

        document.getElementById("loading").style.display =
            "block";

        document.getElementById("resultContent").style.display =
            "none";

        const vehicleData = {

            oem:
                document.getElementById("oem").value,

            model:
                document.getElementById("model").value,

            variant:
                document.getElementById("variant").value,

            fuel:
                document.getElementById("fuel").value,

            transmission:
                document.getElementById("transmission").value,

            body:
                document.getElementById("body").value,

            owner_type:
                document.getElementById("owner_type").value,

            City:
                document.getElementById("City").value,

            state:
                document.getElementById("state").value,

            km:
                Number(document.getElementById("km").value),

            car_age:
                Number(document.getElementById("car_age").value),

            premium_brand:
                Number(document.getElementById("premium_brand").value)

        };

        try {

            const response =
                await fetch(`${API_URL}/predict`, {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body:
                        JSON.stringify(vehicleData)

                });

            const result =
                await response.json();

            document.getElementById("loading").style.display =
                "none";

            document.getElementById("resultContent").style.display =
                "block";

            document.getElementById("price").innerHTML =
                "₹ " +
                Number(result.predicted_price).toLocaleString("en-IN");

            document.getElementById("status").innerHTML =
                "Prediction Successful";

            // ==========================================
            // Prediction History
            // ==========================================

            let history =
                JSON.parse(
                    localStorage.getItem("predictionHistory")
                ) || [];

            history.unshift({

                vehicle:
                    vehicleData.oem +
                    " " +
                    vehicleData.model,

                price:
                    Number(result.predicted_price)
                        .toLocaleString("en-IN")

            });

            history =
                history.slice(0, 5);

            localStorage.setItem(

                "predictionHistory",

                JSON.stringify(history)

            );

            loadHistory();

        }

        catch (error) {

            console.log(error);

            document.getElementById("loading").style.display =
                "none";

            document.getElementById("resultContent").style.display =
                "block";

            document.getElementById("price").innerHTML =
                "Error";

            document.getElementById("status").innerHTML =
                "Unable to connect to API";

        }

    }

);

// ===========================================================
// Load Prediction History
// ===========================================================

function loadHistory() {

    const history =
        JSON.parse(
            localStorage.getItem("predictionHistory")
        ) || [];

    const historyList =
        document.getElementById("historyList");

    historyList.innerHTML = "";

    history.forEach((item) => {

        historyList.innerHTML +=

            `<li>

                ${item.vehicle}

                -

                ₹ ${item.price}

            </li>`;

    });

}

// ===========================================================
// Initialize Page
// ===========================================================

loadBrands();

loadHistory();