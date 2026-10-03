const analyzeButton = document.getElementById("analyzeBtn");

const messageInput = document.getElementById("message");

const resultBox = document.getElementById("result");

const riskTitle = document.getElementById("riskTitle");

const riskDescription =
    document.getElementById("riskDescription");

const riskIcon =
    document.getElementById("riskIcon");

const scoreBar =
    document.getElementById("scoreBar");

const scoreValue =
    document.getElementById("scoreValue");

const indicators =
    document.getElementById("indicators");

const recommendationText =
    document.getElementById("recommendationText");


// =====================================================
// DISPLAY RESULT
// =====================================================

function displayResult(data) {

    const score = data.score;


    // Risk information
    if (score >= 70) {

        riskTitle.textContent = "Potential Scam";

        riskDescription.textContent =
            "Several high-risk indicators were detected.";

        riskIcon.textContent = "🚨";

        recommendationText.textContent =
            "Do not click links or share OTPs, passwords, PINs, or banking information.";

    }

    else if (score >= 40) {

        riskTitle.textContent = "Suspicious Message";

        riskDescription.textContent =
            "Some suspicious indicators were detected.";

        riskIcon.textContent = "⚠️";

        recommendationText.textContent =
            "Verify the sender and message independently before taking action.";

    }

    else {

        riskTitle.textContent = "Low Risk";

        riskDescription.textContent =
            "No major scam indicators were detected.";

        riskIcon.textContent = "✅";

        recommendationText.textContent =
            "No major indicators were detected, but always verify unexpected requests.";
    }


    // Score
    scoreValue.textContent =
        `${score} / 100`;

    scoreBar.style.width =
        `${score}%`;


    // Indicators
    indicators.innerHTML = "";


    if (!data.detected || data.detected.length === 0) {

        indicators.innerHTML =
            `<span class="indicator">
                ✓ No major indicators detected
             </span>`;

    }

    else {

        data.detected.forEach(function (indicator) {

            const item =
                document.createElement("span");

            item.className = "indicator";


            let displayName =
                indicator.replaceAll("_", " ");


            if (displayName.startsWith("url ")) {

                displayName =
                    "URL: " +
                    displayName.substring(4);
            }


            displayName =
                displayName.replace(
                    "url shortener",
                    "URL Shortener"
                );


            item.textContent =
                "🔴 " + displayName;


            indicators.appendChild(item);

        });
    }


    // ML result
    if (data.ml_prediction) {

        const mlIndicator =
            document.createElement("span");

        mlIndicator.className =
            "indicator";

        mlIndicator.textContent =
            `🤖 ML: ${data.ml_prediction} (${data.ml_probability}%)`;

        indicators.appendChild(mlIndicator);
    }


    // OCR result
    if (data.extracted_text) {

        let existingOcrBox =
            document.getElementById("ocrTextBox");


        if (existingOcrBox) {

            existingOcrBox.remove();
        }


        const ocrBox =
            document.createElement("div");

        ocrBox.id =
            "ocrTextBox";

        ocrBox.className =
            "ocr-text-box";


        const ocrTitle =
            document.createElement("h3");

        ocrTitle.textContent =
            "📸 Extracted Screenshot Text";


        const ocrText =
            document.createElement("pre");

        ocrText.textContent =
            data.extracted_text.trim();


        ocrBox.appendChild(ocrTitle);

        ocrBox.appendChild(ocrText);


        resultBox.appendChild(ocrBox);


        messageInput.value =
            data.extracted_text.trim();
    }


    // Show result
    resultBox.classList.remove("hidden");


    resultBox.scrollIntoView({
        behavior: "smooth"
    });
}


// =====================================================
// NORMAL MESSAGE ANALYSIS
// =====================================================

analyzeButton.addEventListener(
    "click",
    async function () {

        const message =
            messageInput.value.trim();


        if (!message) {

            alert("Please enter a message first.");

            return;
        }


        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";


        try {

            const response =
                await fetch("/analyze", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                });


            const data =
                await response.json();


            if (!response.ok) {

                alert(data.error);

                return;
            }


            displayResult(data);

        }

        catch (error) {

            console.error(error);

            alert(
                "Something went wrong. Please try again."
            );

        }

        finally {

            analyzeButton.disabled = false;

            analyzeButton.textContent =
                "🔍 Analyze Message";
        }
    }
);


// =====================================================
// SCREENSHOT SCANNER
// =====================================================

const scanButton =
    Array.from(
        document.querySelectorAll("button")
    ).find(function (button) {

        return button.textContent.includes(
            "Scan Screenshot"
        );

    });


if (scanButton) {

    const fileInput =
        document.createElement("input");


    fileInput.type = "file";

    fileInput.accept =
        "image/png,image/jpeg,image/jpg,image/webp";

    fileInput.style.display =
        "none";


    document.body.appendChild(fileInput);


    // Open file picker
    scanButton.addEventListener(
        "click",
        function () {

            fileInput.click();

        }
    );


    // Image selected
    fileInput.addEventListener(
        "change",
        async function () {

            const file =
                fileInput.files[0];


            if (!file) {

                return;
            }


            scanButton.disabled = true;

            scanButton.textContent =
                "📸 Scanning...";


            try {

                const formData =
                    new FormData();


                formData.append(
                    "image",
                    file
                );


                const response =
                    await fetch(
                        "/scan-screenshot",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    alert(
                        data.error ||
                        "Could not scan screenshot."
                    );

                    return;
                }


                displayResult(data);

            }

            catch (error) {

                console.error(error);

                alert(
                    "Something went wrong while scanning the screenshot."
                );

            }

            finally {

                scanButton.disabled = false;

                scanButton.textContent =
                    "📷 Scan Screenshot";

                fileInput.value = "";
            }
        }
    );
}