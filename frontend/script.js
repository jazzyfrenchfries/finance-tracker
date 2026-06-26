const form = document.getElementById("transaction-form");


form.addEventListener("submit", async (event) => {

    event.preventDefault();


    const transaction = {

        merchant: document.getElementById("merchant").value,

        amount: Number(
            document.getElementById("amount").value
        ),

        category: document.getElementById("category").value,

        date: new Date()
            .toISOString()
            .split("T")[0],

        notes: ""

    };


    const response = await fetch(
        "http://127.0.0.1:8000/transactions",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(transaction)
        }
    );


    const data = await response.json();

    console.log(data);

});