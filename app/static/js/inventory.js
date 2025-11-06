// Inventory Management Functions

// Filter inventory items based on search and filters
function filterItems() {
    const searchTerm = document.getElementById('itemSearch').value.toLowerCase();
    const labFilter = document.getElementById('labFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    
    const rows = document.querySelectorAll('#inventoryTable tbody tr');
    
    rows.forEach(row => {
        const itemName = row.querySelector('td:first-child').textContent.toLowerCase();
        const lab = row.querySelector('td:nth-child(2)').textContent;
        const status = row.querySelector('td:nth-child(4)').textContent.trim();
        
        const matchesSearch = itemName.includes(searchTerm);
        const matchesLab = !labFilter || lab === labFilter;
        const matchesStatus = !statusFilter || status === statusFilter;
        
        row.style.display = matchesSearch && matchesLab && matchesStatus ? '' : 'none';
    });
}

// Reset all filters
function resetFilters() {
    document.getElementById('itemSearch').value = '';
    document.getElementById('labFilter').value = '';
    document.getElementById('statusFilter').value = '';
    filterItems();
}

// Show item history modal
function showItemHistory(inventoryId) {
    // TODO: Fetch and display item history
    const modal = new bootstrap.Modal(document.getElementById('itemHistoryModal'));
    modal.show();
}

// Export inventory to CSV
function exportToCSV() {
    const table = document.getElementById('inventoryTable');
    const rows = table.querySelectorAll('tr');
    
    let csv = [];
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols)
            .map(col => col.textContent.trim())
            .filter(text => text !== 'Actions')
            .join(',');
        if (rowData) {
            csv.push(rowData);
        }
    });
    
    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'inventory.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Print inventory
function printInventory() {
    window.print();
}