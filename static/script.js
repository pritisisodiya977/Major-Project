document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('expense-form');
    const expenseList = document.getElementById('expense-list');
    const totalAmountSpan = document.getElementById('total-amount');

    // Function to fetch and display expenses from Backend
    async function loadExpenses() {
        const response = await fetch('/get_expense');
        const expenses = await response.json();
        
        expenseList.innerHTML = '';
        let total = 0;

        expenses.forEach(exp => {
            total += exp.amount;
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <strong>${exp.title}</strong> 
                    <span class="expense-category">${exp.category}</span>
                </div>
                <span>₹${exp.amount.toFixed(2)}</span>
            `;
            expenseList.appendChild(li);
        });

        totalAmountSpan.textContent = total.toFixed(2);
    }

    // Function to handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('title').value;
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value;

        const expenseData = { title, amount, category };

        // Sending data to Flask Backend via POST request
        const response = await fetch('/add_expense', { // Adjust if endpoint renamed to /add_expense
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(expenseData)
        });

        if (response.ok) {
            form.reset();
            loadExpenses(); // Refresh the list without reloading the page
        } else {
            alert('Failed to save expense');
        }
    });

    // Initial load
    loadExpenses();
});