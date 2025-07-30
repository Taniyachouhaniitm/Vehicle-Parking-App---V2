<template>
  <div class="container mt-4">

    <h4 class="mt-5">Revenue Per Lot Chart</h4>
    <canvas id="revenueChart" height="100"></canvas>

    <h2 class="fw-bold mb-4"> Statistical Analytics</h2>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card shadow-sm p-3">
            <h5>Total Revenue</h5>
            <p class="fs-4 text-success">₹ {{ analytics.total_revenue }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm p-3">
            <h5>Total Reservations</h5>
            <p class="fs-4">{{ analytics.total_reservations }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-sm p-3">
            <h5>Total Parking Lots</h5>
            <p class="fs-4">{{ analytics.total_lots }}</p>
          </div>
        </div>
      </div>

      <div>
        <h4>Revenue Per Lot</h4>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between" v-for="lot in analytics.revenue_per_lot" :key="lot.location">
            <span>{{ lot.location }}</span>
            <span>₹ {{ lot.revenue }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script>
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: 'AdminAnalytics',
  data() {
    return {
      analytics: {},
      loading: true,
      error: '',
      chart: null
    };
  },
  methods: {
    async loadAnalytics() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(import.meta.env.VITE_BASEURL + '/admin/analytics', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch');
        }

        const data = await response.json();
        this.analytics = data;

        this.$nextTick(() => {
          this.renderChart(); // draw chart after DOM is updated
        });
      } catch (err) {
        console.error('Failed to load analytics:', err);
        this.error = err.message === 'Failed to fetch'
          ? 'Failed to fetch analytics data from the server.'
          : 'An error occurred while loading analytics.';
      } finally {
        this.loading = false;
      }
    },

    renderChart() {
      const ctx = document.getElementById('revenueChart');
      if (!ctx || !this.analytics.revenue_per_lot) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const labels = this.analytics.revenue_per_lot.map(lot => lot.location);
      const data = this.analytics.revenue_per_lot.map(lot => lot.revenue);

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Revenue (₹)',
              data,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: value => `₹ ${value}`
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.loadAnalytics();
  }
};
</script>
