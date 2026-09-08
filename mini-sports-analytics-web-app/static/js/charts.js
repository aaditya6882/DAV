/* =========================================================
   MATCHIQ — Chart.js Helpers
   ========================================================= */

(function () {
  'use strict';

  function isDark() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  function chartColors() {
    return {
      text:     isDark() ? '#F1F5F9' : '#111827',
      muted:    isDark() ? '#8899B4' : '#6B7280',
      grid:     isDark() ? '#263047' : '#DDE1E9',
      surface:  isDark() ? '#111827' : '#FFFFFF',
      primary:  '#8A1538',
      gold:     '#C8A45D',
      palette: [
        '#8A1538', '#C8A45D', '#2563EB', '#16A34A',
        '#D97706', '#7C3AED', '#DC2626', '#0891B2',
        '#BE185D', '#065F46', '#1D4ED8', '#B45309',
      ],
    };
  }

  function baseOptions(title) {
    const c = chartColors();
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: c.text, font: { family: 'Inter', size: 12 } },
        },
        title: title ? {
          display: true,
          text: title,
          color: c.text,
          font: { family: 'Space Grotesk', size: 14, weight: '700' },
          padding: { bottom: 12 },
        } : { display: false },
        tooltip: {
          backgroundColor: c.surface,
          titleColor: c.text,
          bodyColor: c.muted,
          borderColor: c.grid,
          borderWidth: 1,
          cornerRadius: 8,
          padding: 10,
        },
      },
      scales: {
        x: {
          grid: { color: c.grid },
          ticks: { color: c.muted, font: { size: 11 } },
        },
        y: {
          grid: { color: c.grid },
          ticks: { color: c.muted, font: { size: 11 } },
          beginAtZero: true,
        },
      },
    };
  }

  /* ---- Bar Chart ---- */
  window.mqBarChart = function (canvasId, labels, data, label, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: label || '',
          data: data,
          backgroundColor: c.primary,
          borderRadius: 4,
          borderSkipped: false,
        }],
      },
      options: Object.assign(baseOptions(title), { plugins: Object.assign(baseOptions(title).plugins, {
        legend: { display: false },
      })}),
    });
  };

  /* ---- Horizontal Bar Chart ---- */
  window.mqHBarChart = function (canvasId, labels, data, label, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    const opts = baseOptions(title);
    opts.indexAxis = 'y';
    opts.scales = {
      x: { grid: { color: c.grid }, ticks: { color: c.muted, font: { size: 11 } }, beginAtZero: true },
      y: { grid: { display: false }, ticks: { color: c.muted, font: { size: 11 } } },
    };
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: label || '',
          data: data,
          backgroundColor: labels.map(function (_, i) { return c.palette[i % c.palette.length]; }),
          borderRadius: 4,
          borderSkipped: false,
        }],
      },
      options: Object.assign(opts, { plugins: Object.assign(opts.plugins, { legend: { display: false } }) }),
    });
  };

  /* ---- Doughnut Chart ---- */
  window.mqDoughnutChart = function (canvasId, labels, data, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    const opts = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: c.text, font: { family: 'Inter', size: 12 }, padding: 12 },
        },
        tooltip: baseOptions().plugins.tooltip,
        title: title ? {
          display: true, text: title, color: c.text,
          font: { family: 'Space Grotesk', size: 14, weight: '700' },
          padding: { bottom: 12 },
        } : { display: false },
      },
    };
    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: [c.primary, c.gold, '#2563EB', '#16A34A', '#D97706', '#7C3AED'],
          borderColor: c.surface,
          borderWidth: 3,
          hoverOffset: 6,
        }],
      },
      options: opts,
    });
  };

  /* ---- Line Chart ---- */
  window.mqLineChart = function (canvasId, labels, data, label, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: label || '',
          data: data,
          borderColor: c.primary,
          backgroundColor: 'rgba(138,21,56,.12)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: c.primary,
          pointRadius: 4,
        }],
      },
      options: baseOptions(title),
    });
  };

  /* ---- Radar Chart ---- */
  window.mqRadarChart = function (canvasId, labels, datasetA, datasetB, nameA, nameB) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    return new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: nameA,
            data: datasetA,
            borderColor: c.primary,
            backgroundColor: 'rgba(138,21,56,.15)',
            pointBackgroundColor: c.primary,
          },
          {
            label: nameB,
            data: datasetB,
            borderColor: c.gold,
            backgroundColor: 'rgba(200,164,93,.15)',
            pointBackgroundColor: c.gold,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: c.text } },
          tooltip: baseOptions().plugins.tooltip,
        },
        scales: {
          r: {
            grid: { color: c.grid },
            ticks: { color: c.muted, backdropColor: 'transparent', font: { size: 10 } },
            pointLabels: { color: c.text, font: { size: 11 } },
            beginAtZero: true,
          },
        },
      },
    });
  };

  /* ---- Multi-series Bar Chart (for Compare) ---- */
  window.mqCompareBar = function (canvasId, labels, dataA, dataB, nameA, nameB) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const c = chartColors();
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: nameA,
            data: dataA,
            backgroundColor: c.primary,
            borderRadius: 4,
          },
          {
            label: nameB,
            data: dataB,
            backgroundColor: c.gold,
            borderRadius: 4,
          },
        ],
      },
      options: baseOptions(),
    });
  };

  /* ---- Update chart colors on theme toggle ---- */
  document.addEventListener('DOMContentLoaded', function () {
    const themeBtn = document.getElementById('mq-theme-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        setTimeout(function () {
          if (window.Chart) {
            Chart.instances = Chart.instances || {};
            Object.values(Chart.instances).forEach(function (chart) {
              chart.update();
            });
          }
        }, 50);
      });
    }
  });

})();
