<template>
  <div class="profile-container">
    <h2>Delivery Partner Profile</h2>
    <div class="profile-wrapper">
      <!-- Delivery Partner Details Section -->
      <div class="delivery-details">
        <form @submit.prevent="toggleEdit">
          <label>Name</label>
          <input type="text" v-model="profile.username" disabled class="readonly" />

          <label>Email</label>
          <input type="email" v-model="profile.email" disabled class="readonly" />

          <label>Phone Number</label>
          <input
            type="text"
            v-model="profile.phone_number"
            :disabled="!isEditing"
            :class="{ editable: isEditing, readonly: !isEditing }"
          />

          <label>Availability</label>
          <select v-model="profile.is_available" :disabled="!isEditing">
            <option :value="true">Available</option>
            <option :value="false">Not Available</option>
          </select>

          <button type="submit">{{ isEditing ? "Save Changes" : "Update Profile" }}</button>
        </form>

        <button @click="verifyPhone" class="verify-btn">Verify Phone</button>
        <p v-if="phoneVerified" class="success">Verification message has been sent.</p>
      </div>

      <!-- History Section -->
      <div class="history-section">
        <h3>History</h3>
        <div class="history-content">
          <p>Delivery history and past actions will be displayed here.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      profile: {
        username: "",
        email: "",
        phone_number: "",
        is_available: true
      },
      phoneVerified: false,
      isEditing: false // Editing is disabled by default
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const username = localStorage.getItem("username");

        if (!username) {
          console.error("Username not found in localStorage.");
          return;
        }

        const response = await axios.get(`http://127.0.0.1:8000/user/delivery/profile/${username}/`, {
          headers: { Authorization: `Token ${token}` }
        });
        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },

    async toggleEdit() {
      if (this.isEditing) {
        try {
          const token = localStorage.getItem("token");
          const username = localStorage.getItem("username");

          if (!username) {
            console.error("Username not found in localStorage.");
            return;
          }

          await axios.put(`http://127.0.0.1:8000/user/delivery/profile/update/${username}/`, this.profile, {
            headers: { Authorization: `Token ${token}` }
          });
          alert("Profile updated successfully!");
        } catch (error) {
          console.error("Error updating profile:", error);
        }
      }
      this.isEditing = !this.isEditing;
    },
    verifyPhone() {
      alert("Verification message has been sent.");
      this.phoneVerified = true;
    }
  }
};
</script>

<style scoped>
.profile-container {
  width: 90%;
  max-width: 900px;
  margin: 5vh auto;
  padding: 2rem;
  background: rgb(35, 35, 35);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 255, 170, 255);
}

.delivery-details {
  margin-bottom: 20px;
}

input, textarea, select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.readonly {
  background-color: transparent;
  color: white;
  border: 1px solid #ccc;
}

.editable {
  background-color: white;
  color: black;
}

button {
  background: transparent;
  border: 2px solid #41b883;
  padding: 10px;
  font-size: 16px;
  color: white;
  cursor: pointer;
  transition: color 0.3s ease-in-out, border-color 0.3s ease-in-out;
  border-radius: 5px;
  width: 100%;
}

button:hover {
  color: #41b883;
  border-color: #41b883;
}

.verify-btn {
  margin-top: 10px;
  border: 2px solid #ff9900;
}

.verify-btn:hover {
  color: #ff9900;
  border-color: #ff9900;
}

.success {
  color: green;
  margin-top: 10px;
}

.history-section {
  background: rgb(15, 15, 15);
  padding: 15px;
  border-radius: 5px;
  max-height: 300px;
  overflow-y: auto;
}

.history-content {
  height: 400px;
}
</style>