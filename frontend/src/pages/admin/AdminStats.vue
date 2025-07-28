<template>
  <div class="container mt-4">
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
export default {
  name: 'AdminAnalytics',
  data() {
    return {
      analytics: {},
      loading: true,
      error: ''
    };
  },
  methods: {
    async loadAnalytics() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(import.meta.env.VITE_BASEURL +'/admin/analytics', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch');
        }

        const data = await response.json();
        this.analytics = data;
      } catch (err) {
        console.error("Failed to load analytics:", err);
        if (err.message === 'Failed to fetch') {
          this.error = "Failed to fetch analytics data from the server.";
        } else {
          this.error = "An error occurred while loading analytics.";
        }
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.loadAnalytics();
  }
};
</script>
