const API = "";


async function loadDashboard() {

    const summaryResponse = await fetch(
        `${API}/summary/monthly?year=2026&month=7`
    );

    const summary = await summaryResponse.json();


    document.getElementById("balance").textContent =
        "£" + summary.balance.toFixed(2);

    document.getElementById("income").textContent =
        "£" + summary.income.toFixed(2);

    document.getElementById("expenses").textContent =
        "£" + summary.expenses.toFixed(2);



    const transactionsResponse = await fetch(
        `${API}/transactions`
    );

    const transactions =
        await transactionsResponse.json();


    const container =
        document.getElementById("transactions");


    container.innerHTML = "";


    transactions
        .slice(-5)
        .reverse()
        .forEach(transaction => {

            const div =
                document.createElement("div");

            div.className = "transaction";


            const sign =
                transaction.transaction_type === "income"
                ? "+"
                : "-";


            div.innerHTML = `
                <strong>
                    ${transaction.merchant}
                </strong>
                <br>
                ${transaction.category}
                <br>
                ${transaction.date}
                <br>
                ${sign}£${transaction.amount.toFixed(2)}
            `;


            container.appendChild(div);

        });
}


loadDashboard();
function showAddTransaction() {

    const form =
        document.getElementById("addTransaction");

    form.style.display = "block";
}



async function addTransaction() {

    const transaction = {

        amount:
            Number(
                document.getElementById("amount").value
            ),

        transaction_type:
            document.getElementById("type").value,

        category:
            document.getElementById("category").value,

        merchant:
            document.getElementById("merchant").value,

        date:
            document.getElementById("date").value || 
            new Date().toISOString().split("T")[0],

        notes:
            document.getElementById("notes").value

    };


    const response = await fetch(
        `${API}/transactions`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body:
                JSON.stringify(transaction)
        }
    );


    if(response.ok) {

        alert("Transaction saved!");

        location.reload();

    } else {

        const error = await response.json();
        console.log(error);
        alert(JSON.stringify(error));
    }

}
const balanceResponse = await fetch(
    `${API}/summary`
);

const balance =
    await balanceResponse.json();


document.getElementById("balance summary").textContent =
    "£" + balance.balance.toFixed(2);