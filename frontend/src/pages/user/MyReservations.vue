<template>
  <div class="container mt-4">
    <h2 class="mb-3 fw-bold">🧾 My Reservations</h2>

    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Spot ID</th>
          <th>Parking Time</th>
          <th>Leaving Time</th>
          <th>Cost</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in reservations" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.spot_id }}</td>
          <td>{{ r.parking_timestamp }}</td>
          <td>{{ r.leaving_timestamp || '—' }}</td>
          <td>{{ r.parking_cost ?? '—' }}</td>
           <button class="btn btn-danger btn-sm" @click="releaseReservation(r.id)" v-if="!r.leaving_timestamp">
              Release
            </button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'UserReservations',
  data() {
    return {
      reservations: []
    };
  },
  methods: {
    async loadReservations() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(import.meta.env.VITE_BASEURL + '/user/reservations', {
          headers: {
            Authorization: 'Bearer ' + token
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
    },

    async releaseReservation(id) {
      if (!confirm('Are you sure you want to release this reservation?')) return;

      try {
        const token = localStorage.getItem('token');
        const response = await fetch(import.meta.env.VITE_BASEURL + `/user/release-reservation/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        });

        const data = await response.json();

        if (response.ok) {
            alert("Released successfully!");
            this.loadReservations();
        } else {
            alert("Something went wrong");
        }

    } catch (error) {
        console.error('Release failed:', error);
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
