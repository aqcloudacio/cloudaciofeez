<template lang="html">
  <v-container class="pa-0">
    <v-form  @submit.prevent="addStaff" ref="form">
      <v-row dense
        v-for="staff in practice.staff"
        :key="staff.id">
        <v-col>
          <v-container class="py-1 px-0 d-flex">
            <v-icon class="pr-4" large color="primary" v-if="staffIsAdmin(staff)">
              mdi-cowboy
            </v-icon>
            <v-icon class="pr-4" large color="primary" v-else>
              mdi-account
            </v-icon>
            <v-card width="100%" class="rounded-card grey2" elevation="0">
              <v-row dense>
                <v-col>
                  <v-card-text class="title py-1 pl-4">

                    {{emailOrName(staff)}}
                  </v-card-text>
                </v-col>
                <v-card-actions v-if="isAdmin" class="justify-end">
                  <v-spacer></v-spacer>
                  <v-menu offset-y>
                     <template v-slot:activator="{ on }">
                       <v-btn
                          icon
                         v-on="on"
                         class="mr-2">
                         <v-icon color="primary">
                           mdi-settings
                         </v-icon>
                       </v-btn>
                     </template>
                     <v-list>
                       <v-list-item
                        v-if="!staffIsAdmin(staff)"
                        @click="promoteToAdmin(staff)">
                         <v-list-item-title>Promote to admin</v-list-item-title>
                       </v-list-item>
                       <v-list-item
                        v-if="staffIsAdmin(staff)"
                        @click="demoteToStaff(staff)">
                         <v-list-item-title>Demote to staff</v-list-item-title>
                       </v-list-item>
                         <DeleteStaff
                          v-on="$listeners"
                          :staff="staff"
                          :practice="practice"
                          @update-staff="updatePractice($event)"
                        />
                     </v-list>
                   </v-menu>
                 </v-card-actions>
              </v-row>
            </v-card>
          </v-container>
        </v-col>
      </v-row>
      <v-row dense
        v-for="pending in practice.pending_staff"
        :key="pending.id">
        <v-col>
          <v-container class="py-1 px-0 d-flex">
            <v-icon class="pr-4" large color="primary">
              mdi-account-convert
            </v-icon>
            <v-card class="grey2 rounded-card" width="100%" flat>
              <v-row dense>
                <v-col>
                  <v-card-text class="title  py-1 pl-4">

                    {{pending.email}}
                  </v-card-text>
                </v-col>
                <v-card-actions class="justify-end" v-if="isAdmin" >
                  <v-spacer></v-spacer>
                  <v-menu offset-y>
                     <template v-slot:activator="{ on }">
                       <v-btn
                          icon
                          v-on="on"
                          class="mr-2">
                          <v-icon color="primary">
                            mdi-settings
                          </v-icon>
                       </v-btn>
                     </template>
                     <v-list>
                       <DeleteStaff
                        :staff="pending"
                        :practice="practice"
                        @update-staff="updatePractice($event)"
                      />
                     </v-list>
                   </v-menu>
                 </v-card-actions>
              </v-row>
            </v-card>
          </v-container>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            class="rounded-card"
            v-model="newStaff"
            label="Invite a colleague by entering their email address"
            dense outlined
            :error-messages="error ? error.message : null"
            @click="error = null"
            :rules="$ruleEmail"
            hide-details="auto"
            validate-on-blur
          >
            <template v-slot:append-outer>
              <v-slide-x-reverse-transition
                 mode="out-in"
                 >
                <v-icon
                  @click="addStaff"
                  color="primary"
                  :key="`icon-${isSaving}`"
                >
                  mdi-plus
                </v-icon>
              </v-slide-x-reverse-transition>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import DeleteStaff from "@/components/DeleteStaff.vue";
import { ruleEmail } from "@/components/mixins/Rules.js"

export default {
  name: "StaffTable",
  mixins: [ruleEmail],
  props: {
    isAdmin: {
      type: Boolean,
      required: true,
    },
    practice: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      newStaff: "",
      error: null,
      isSaving: false,
    };
  },
  components: {
    DeleteStaff,
  },
  methods: {
    emailOrName(staff) {
      if (staff.name != null) {
        return staff.name
      } else {
        return staff.email
      }
    },
    staffIsAdmin(staff) {
      if (this.practice.admins) {
        if (this.practice.admins.filter(i => i.id === staff.id).length > 0) {
          return true
        } else {
          return false
        }
      }
    },
    promoteToAdmin(staff) {
      let adminArray = this.practice.admins.map(function (obj) {
        return obj.id })
      adminArray.push(staff.id);
      let endpoint = `/api/practices/${this.practice.id}/`;
      apiService(endpoint, "PATCH", {
        admins_id: adminArray,
      }).then(data => {
        this.practice.admins = data.admins;
      })
    },
    demoteToStaff(staff) {
      let staffRemoved = this.practice.admins.filter(i => i.id !== staff.id);
      // Prevents a practice from having no admins
      if (staffRemoved.length > 0) {
          let adminArray = staffRemoved.map(function (obj) {
            return obj.id })
        let endpoint = `/api/practices/${this.practice.id}/`;
        apiService(endpoint, "PATCH", {
          admins_id: adminArray,
        }).then(data => {
          this.practice.admins = data.admins;
        })
      }
    },
    updatePractice(data) {
      if (data.id) {
        this.$emit('update-practice', data);
      }
    },
    addStaff() {
      if (this.$refs.form.validate()) {
        if (this.newStaff != '') {
          this.isSaving = true;
          let endpoint = `/api/practices/${this.practice.id}/`;
          apiService(endpoint, "PATCH", {
            add_staff: this.newStaff,
          }).then( data => {
            this.$emit('update-practice', data);
            this.practice.pending_staff = data.pending_staff;
            this.newStaff = ''
            this.isSaving = false;
          }).catch(error => {
            this.error = error.data;
            this.isSaving = false;
          })
        }
      }
    },
  },
};
</script>
