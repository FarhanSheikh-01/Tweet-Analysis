function updateForm() {
    let option = document.getElementById("optionSelect").value;
    let inputLabel = document.getElementById("inputLabel");
    let inputField = document.getElementById("inputField");
    let actionButton = document.getElementById("actionButton");

    if (option === "tweets") {
        inputLabel.textContent = "Enter Twitter Username";
        inputField.placeholder = "Enter username";
        actionButton.textContent = "Fetch Tweets";
    } else {
        inputLabel.textContent = "Enter your comment";
        inputField.placeholder = "Enter comment text";
        actionButton.textContent = "Analyze Sentiment";
    }
}

function fetchData() {
    let option = document.getElementById("optionSelect").value;
    let inputValue = document.getElementById("inputField").value.trim();
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    if (!inputValue) {
        alert("Please enter a value!");
        return;
    }

    fetch(option === "tweets" ? "/fetch_tweets/" : "/msg/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken
        },
        body: "inputValue=" + encodeURIComponent(inputValue)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        if (option === "tweets") {
            displayTweets(data.tweets);
        } else {
            document.getElementById("sentimentOutput").style.display = "block";
            document.getElementById("sentimentPrediction").textContent = data.prediction;
        }
    })
    .catch(error => console.error("Error:", error));
}

function displayTweets(tweets) {
    let container = document.getElementById("tweetsContainer");
    container.innerHTML = ""; // Clear previous tweets

    tweets.forEach(tweet => {
        let card = document.createElement("div");
        card.classList.add("tweet-card");

        // Assign class based on sentiment
        if (tweet.sentiment.toLowerCase() === "positive") {
            card.classList.add("positive");
        } else if (tweet.sentiment.toLowerCase() === "negative") {
            card.classList.add("negative");
        } else {
            card.classList.add("neutral");
        }

        card.innerHTML = `
            <h5>@${tweet.username}</h5>
            <p>${tweet.text}</p>
            <strong>Sentiment: ${tweet.sentiment}</strong>
        `;

        container.appendChild(card);
    });
}