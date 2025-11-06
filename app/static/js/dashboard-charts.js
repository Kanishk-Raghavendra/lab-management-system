// Dashboard Charts Configuration

// Color scheme for charts
const chartColors = {
    primary: '#6610f2',
    info: '#17a2b8',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    gray: '#6c757d'
};

// Inventory Usage Chart
function createInventoryChart(canvas, data) {
    return new Chart(canvas, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Equipment Usage',
                data: data.equipment,
                borderColor: chartColors.primary,
                tension: 0.4
            }, {
                label: 'Consumables Usage',
                data: data.consumables,
                borderColor: chartColors.info,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Monthly Inventory Usage'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Lab Utilization Chart
function createLabUtilizationChart(canvas, data) {
    return new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    chartColors.success,
                    chartColors.warning,
                    chartColors.danger
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Lab Space Utilization'
                }
            }
        }
    });
}

// Experiment Statistics Chart
function createExperimentChart(canvas, data) {
    return new Chart(canvas, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Completed',
                data: data.completed,
                backgroundColor: chartColors.success
            }, {
                label: 'Pending',
                data: data.pending,
                backgroundColor: chartColors.warning
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Monthly Experiment Statistics'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true
                },
                x: {
                    stacked: true
                }
            }
        }
    });
}