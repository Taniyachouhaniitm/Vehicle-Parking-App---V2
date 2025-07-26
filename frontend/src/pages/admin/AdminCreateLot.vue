<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-2xl font-bold mb-4 text-center">Create Parking Lot</h2>

    <form @submit.prevent="create_parking_lot" class="space-y-4">
      <div>
        <label class="block mb-1 font-semibold">Prime Location:</label>
        <input v-model="new_ParkingLot.name" required class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block mb-1 font-semibold">Price (per hour):</label>
        <input v-model.number="new_ParkingLot.price" type="number" required class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block mb-1 font-semibold">Address:</label>
        <input v-model="new_ParkingLot.address" required class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block mb-1 font-semibold">Pincode:</label>
        <input v-model="new_ParkingLot.pin_code" required class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block mb-1 font-semibold">Number of Spots:</label>
        <input v-model.number="new_ParkingLot.number_of_spots" type="number" required class="border p-2 w-full rounded" />
      </div>

      <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" type="submit">Create Lot</button>

      <div v-if="error" class="text-red-600 mt-2 text-center">{{ error }}</div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AdminCreateLot',
  data() {
    return {
      new_ParkingLot: {
        name: '',
        price: null,
        address: '',
        pin_code: '',
        number_of_spots: null
      },
      error: ''
    };
  },
  methods: {
    async create_parking_lot() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Unauthorized: No token found.';
          return;
        }

        const response = await fetch(import.meta.env.VITE_BASEURL + '/admin/parking_lots', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify(this.new_ParkingLot),
        });

        const result = await response.json();

        if (!response.ok) {
          this.error = result.msg || 'Failed to create lot.';
          return;
        }

        alert('Parking lot created successfully!');
        this.error = '';
        // Optional: Reset form
        this.new_ParkingLot = {
          name: '',
          price: null,
          address: '',
          pin_code: '',
          number_of_spots: null
        };
      } catch (error) {
        console.error('Error creating lot:', error);
        this.error = 'Server error. Please try again later.';
      }
    }
  }
}
</script>

<style scoped>
input {
  outline: none;
}
</style>
