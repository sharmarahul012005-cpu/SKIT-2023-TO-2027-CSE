// demand.js - demand prediction via the ML API (needs api.js and history.js)
async function predictDemand() {
  const region = parseInt(document.getElementById('d-region').value);
  const month  = parseInt(document.getElementById('d-month').value);
  const price  = parseFloat(document.getElementById('d-price').value);
  const dem7   = parseFloat(document.getElementById('d-dem7').value);

  try {
    const value = await apiPredict('demand', {
      region, month, price, demand_7d_avg: dem7
    });
    const demand = Math.max(0, Math.round(value));
    document.getElementById('demand-out').textContent = demand + ' T';

    const tips = [];
    if (demand > 200) tips.push('High demand expected — plan for enough stock.');
    if (demand < 100) tips.push('Low demand expected — buy conservatively.');
    if (price > 2900) tips.push('Price is high, which may reduce buyer interest.');
    document.getElementById('demand-tips').innerHTML =
      tips.map(t => `<div class="tip">${t}</div>`).join('');

    addHistoryRow('Demand', region, month, demand + ' T');
  } catch (err) {
    document.getElementById('demand-out').textContent = '⚠';
    document.getElementById('demand-tips').innerHTML =
      `<div class="tip">Could not reach the prediction server. ${err.message}</div>`;
  }
}
