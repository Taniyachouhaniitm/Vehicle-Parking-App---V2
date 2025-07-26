<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Available Parking Lots</h2>

    <!-- Error message shown only if no data is loaded -->
    <div v-if="error && !parkingLots.length" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- No-data message -->
    <div v-else-if="!parkingLots.length" class="alert alert-info">
      No parking lots available.
    </div>

    <!-- Table of parking lots -->
    <table v-if="parkingLots.length" class="table table-bordered table-striped">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Location</th>
          <th>Price</th>
          <th>Address</th>
          <th>Pin Code</th>
          <th>Number of Spots</th>
          <th>Available Spots</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in parkingLots" :key="lot.id">
          <td>{{ lot.id }}</td>
          <td>{{ lot.prime_location_name }}</td>
          <td>₹{{ lot.price }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.pin_code }}</td>
          <td>{{ lot.number_of_spots }}</td>
          <td>{{ lot.number_of_spots - lot.reserved_spots }}</td>
          <td>
            <button
              class="btn btn-primary btn-sm"
              @click="bookSpot(lot.id)"
              :disabled="bookingLotId === lot.id"
            >
              {{ bookingLotId === lot.id ? 'Booking...' : 'Book' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Success message -->
    <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>

    <!-- Error message after booking -->
    <div v-if="error && parkingLots.length" class="alert alert-danger mt-3">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const parkingLots = ref([])
const error = ref('')
const message = ref('')
const bookingLotId = ref(null)

async function loadParkingLots() {
  try {
    error.value = ''
    const token = localStorage.getItem('token')

    if (!token) {
      error.value = 'Please login to view parking lots.'
      return
    }

    const res = await fetch(import.meta.env.VITE_BASEURL+`/user/available-lots`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.msg || 'Failed to load parking lots.'
      parkingLots.value = []
    } else {
      parkingLots.value = data
    }
  } catch (err) {
    console.error(err)
    error.value = 'Server error. Please try again later.'
    parkingLots.value = []
  }
}

async function bookSpot(lotId) {
  try {
    message.value = ''
    error.value = ''
    bookingLotId.value = lotId

    const token = localStorage.getItem('token')

    if (!token) {
      error.value = 'Please login to book a spot.'
      return
    }

    const res = await fetch(import.meta.env.VITE_BASEURL+`/user/available-lots/${lotId}/book`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        spot_id: lotId,  // assuming you're using the lot ID as spot_id
      }),
    })

    const data = await res.json()

    if (res.ok) {
      message.value = `Spot booked! Reservation ID: ${data.reservation_id}`
      error.value = ''
      await loadParkingLots()
      setTimeout(() => (message.value = ''), 4000)
    } else {
      error.value = data.msg || 'Booking failed.'
    }
  } catch (err) {
    console.error(err)
    error.value = 'Server error during booking.'
  } finally {
    bookingLotId.value = null
  }
}

onMounted(loadParkingLots)
</script>

