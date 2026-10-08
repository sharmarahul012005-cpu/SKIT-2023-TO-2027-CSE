// utils.js - shared helper functions

// Rough seasonal boost: prices/demand a bit higher in winter months
function seasonBoost(month) {
  if (month >= 11 || month <= 2) return 1;   // winter
  if (month >= 6 && month <= 9) return -1;   // monsoon
  return 0;
}
