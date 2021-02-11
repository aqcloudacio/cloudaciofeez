<template>
  <v-dialog v-model="dialog" max-width="400">
    <template v-slot:activator="{ on }">
      <v-list-item v-on="on">
        <v-list-item-title>
          Remove from practice
        </v-list-item-title>
      </v-list-item>
    </template>
    <v-card>
      <v-card-title class="headline grey lighten-2 pr-3">
        Remove Staff
      </v-card-title>
      <v-container class="pa-3">
        <v-card-text>
          Are you sure you want to remove {{emailOrName}}
          from your practice? <br> <br>
          This action will:<br>
          <ul>
            <li>Remove their access to all clients shared with your practice.</li>
            <li>Allow your practice to retain access to clients shared by them.</li>
          </ul>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">
            Cancel
          </v-btn>
          <v-btn text @click="deleteStaff(staff)" color="primary">
            Remove Staff
          </v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "DeleteStaff",
  props: {
    staff: {
      type: Object,
      required: true
    },
    practice: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      error: null,
      dialog: false,
    };
  },
  computed: {
    emailOrName() {
      if (this.practice.pending_staff.includes(this.staff)) {
        return this.staff.email
      } else {
        if (this.staff.name != null) {
          return this.staff.name
        } else {
          return this.staff.email
        }
      }
    },
  },
  methods: {
    findStaffIndex(array, staff) {
      return this.practice[array].findIndex(i => i.id === staff.id);
    },
    removeFromArray(array,index) {
      if (index != -1) {
      this.practice[array].splice(index,1);
      }
    },
    deleteStaff(staff) {
      // let arrays = ['staff','admins','pending_staff'];
      // for (let array of arrays) {
      //   this.removeFromArray(array,this.findStaffIndex(array,staff));
      // }
      //
      // let staffArray = this.practice.staff.map(function (obj) {
      //   return obj.id })
      //
      // let adminArray = this.practice.admins.map(function (obj) {
      //   return obj.id })
      //
      // let pendingStaffArray = this.practice.pending_staff.map(function (obj) {
      //   return obj.id })
      // console.log(pendingStaffArray)
      let endpoint = `/api/practices/${this.practice.id}/`;
      console.log("remove staff js");
      apiService(endpoint, "PATCH", {
        remove_staff: staff.id,
      }).then(data => {
        this.$emit('update-staff', data);
      })
      this.dialog = false;
    },
  }
};
</script>
