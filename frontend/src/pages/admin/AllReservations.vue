<template>
  <div class="container mt-4">
    <h2 class="mb-3 fw-bold">All Reservations</h2>

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
        } else {
          alert(data.msg || 'Failed to load reservations');
        }
      } catch (err) {
        console.error(err);
        alert('Error loading reservations');
      }
    }
  },
  mounted() {
    this.loadReservations();
  }
};
</script>

<style scoped>
.container {
  max-width: 900px;
}
.table th, .table td {
  text-align: center;
}
</style>
