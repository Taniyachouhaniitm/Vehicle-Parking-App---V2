<template>
  <div class="container mt-4">
    <div class="text-center mb-4">
      <h2 class="fw-bold">🚗 Welcome to Your Parking Dashboard</h2>
      <p class="text-muted">
        Easily view available parking lots, check spot availability, and manage your reservations—all in one place.
      </p>
    </div>

    <!-- Dashboard section -->
    <div class="card shadow-sm p-4 mb-4">
      <h4 class="mb-3">🔍 Quick View: Available Parking Lots</h4>
      
      <!-- Use the reusable component -->
      <AvailableParkingLots />
      
      <!-- Call-to-action button -->
      <router-link to="/user/available-lots" class="btn btn-primary mt-3">
        View & Book from All Parking Lots →
      </router-link>

      <router-link to="/user/reservations" class="btn btn-secondary mt-3">
        View My Reservations Details →
      </router-link>
    </div>

    </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
  background: #f9f9f9;
}
h2 {
  color: #2c3e50;
}
.btn-primary {
  background-color: #007bff;
  border: none;
}
.btn-primary:hover {
  background-color: #0056b3;
}
</style>


