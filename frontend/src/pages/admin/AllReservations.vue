<template>
  <div class="container mt-4">
    <h2 class="mb-3 fw-bold">All Reservations and Analysis graph</h2>

    <!-- Chart Canvas -->
    <canvas id="revenueChart" height="200" class="mb-5"></canvas>

    <!-- Reservation Table -->
    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>User ID</th>
          <th>Spot ID</th>
          <th>Parking Time</th>
          <th>Leaving Time</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in reservations" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.user_id }}</td>
          <td>{{ r.spot_id }}</td>
          <td>{{ r.parking_timestamp }}</td>
          <td>{{ r.leaving_timestamp || '—' }}</td>
          <td>{{ r.parking_cost ?? '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'AdminReservations',
  data() {
    return {
      reservations: []
    };
  },
  methods: {
    async loadReservations() {
      try {
        const response = await fetch(import.meta.env.VITE_BASEURL + '/admin/reservations', {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.reservations = data.reservations;
          this.generateRevenueChart(data.reservations);
        } else {
          alert(data.msg || 'Failed to load reservations');
        }
      } catch (err) {
        console.error(err);
        alert('Error loading reservations');
      }
    },
    generateRevenueChart(reservations) {
      const dailyRevenue = {};

      // Group cost by date
      reservations.forEach(r => {
        if (r.parking_cost && r.parking_timestamp) {
          const date = r.parking_timestamp.split('T')[0];
          dailyRevenue[date] = (dailyRevenue[date] || 0) + r.parking_cost;
        }
      });

      const labels = Object.keys(dailyRevenue).sort();
      const data = labels.map(date => dailyRevenue[date]);

      const ctx = document.getElementById('revenueChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Revenue (₹)',
            data,
            backgroundColor: 'rgba(0, 51, 102, 0.8)',
            borderColor: 'rgba(0, 51, 102, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Daily Revenue Summary'
            }
          }
        }
      });
    }
  },
  mounted() {
    this.loadReservations();
  }
};
</script>

<style scoped>
.container {
  max-width: 1000px;
}
.table th, .table td {
  text-align: center;
}
</style>
