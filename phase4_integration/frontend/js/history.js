// history.js - prediction history table
let historyCount = 0;

function addHistoryRow(type, region, month, result) {
  historyCount++;
  const tbody = document.getElementById('history-body');
  if (historyCount === 1) tbody.innerHTML = '';
  const monthNames = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const row = document.createElement('tr');
  row.innerHTML = `<td>${historyCount}</td><td>${type}</td><td>${region === 0 ? 'Mandi A' : 'Mandi B'}</td><td>${monthNames[month]}</td><td>${result}</td>`;
  tbody.insertBefore(row, tbody.firstChild);
}
