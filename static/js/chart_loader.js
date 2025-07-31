// Example: load a bar chart using Chart.js
const ctx = document.getElementById('salesChart');
if (ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: JSON.parse(ctx.dataset.labels),
            datasets: [{
                label: 'Sales',
                data: JSON.parse(ctx.dataset.values),
                backgroundColor: '#ffc107'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}
