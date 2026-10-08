// price.js - price prediction via the ML API (needs api.js and history.js)
async function predictPrice() {
  const region = parseInt(document.getElementById('p-region').value);
  const month  = parseInt(document.getElementById('p-month').value);
  const wheat  = parseFloat(document.getElementById('p-wheat').value);
  const rain   = parseFloat(document.getElementById('p-rain').value);
  const price7 = parseFloat(document.getElementById('p-price7').value);

  try {
    const value = await apiPredict('price', {
      region, month, wheat_price: wheat, rainfall: rain, price_7d_avg: price7
    });
    const price = Math.round(value);
    document.getElementById('price-out').textContent = '₹ ' + price.toLocaleString('en-IN');

    const tips = [];
    if (rain > 30) tips.push('High rainfall — prices may drop a bit due to more supply.');
    if (month >= 11 || month <= 2) tips.push('Winter season — demand and prices tend to be higher.');
    if (wheat > 2600) tips.push('Wheat is expensive — farmers may grow more millet, increasing supply.');
    document.getElementById('price-tips').innerHTML =
      tips.map(t => `<div class="tip">${t}</div>`).join('');

    addHistoryRow('Price', region, month, '₹' + price.toLocaleString('en-IN'));
  } catch (err) {
    document.getElementById('price-out').textContent = '⚠';
    document.getElementById('price-tips').innerHTML =
      `<div class="tip">Could not reach the prediction server. ${err.message}</div>`;
  }
}
