<template lang="html">
  <v-container class="pa-0 small-text">
      <v-row align="center">
        <v-col
        :cols="6">
          <v-select
            class="rounded-card"
            v-if="!editGroupName"
            :items="riskProfileGroups"
            item-text="name"
            item-value="id"
            v-model="shownRP"
            label="Risk Profile Group Name"
            placeholder="Select a Risk Profile Group"
            outlined dense hide-details="auto">
            <template v-slot:append-outer v-if="canEdit && !_.isEmpty(shownRPObject)">
              <v-icon
                v-if="!editGroupName"
                color="primary" icon
                @click="editGroupName = !editGroupName">mdi-pencil-circle</v-icon>
            </template>
            <template v-slot:append-outer v-else-if="!_.isEmpty(shownRPObject)">
              <v-tooltip bottom>
                 <template v-slot:activator="{ on }">
                    <v-icon
                      v-on='on'
                      color="primary" icon
                      >mdi-lock</v-icon>
                </template>
                <span>{{lockMessage}}</span>
              </v-tooltip>
            </template>
          </v-select>
          <v-text-field
            v-else
            label="Risk Profile Group Name"
            :value="shownRPObject.name"
            @change="newGroupName = $event"
            dense outlined
            hide-details="auto">
            <template v-slot:append-outer v-if="canEdit">
              <v-icon
                v-if="editGroupName"
                color="primary" icon
                @click="updateGroupName()">mdi-check-circle</v-icon>
            </template>
          </v-text-field>
        </v-col>
        <v-col>
          <v-container class="pa-0 d-flex">
            <v-switch
              inset
              v-if="!_.isEmpty(shownRPObject)"
              v-model="activeSwitch"
              label="Active Risk Profile Group"
              />
            <v-spacer />
            <v-card-actions class="pr-0">
              <DeleteObj
                v-if="canEdit && !_.isEmpty(shownRPObject)"
                :objectType="'riskprofilegroup'"
                :objectToDelete="shownRPObject"
                @delete-object="deleteRPGroup($event)"
                :color="'primary'"

              />
              <AddRPGroup
                :userID="activeUser.id"
                @add-rpgroup="addRPGroup($event)"/>


            </v-card-actions>
          </v-container>
        </v-col>
      </v-row>
      <v-divider class="mt-1 mb-4" v-if="!_.isEmpty(shownRPObject)"/>
      <v-row dense v-if="!_.isEmpty(shownRPObject)">
        <v-col
          :cols="2">

        </v-col>
        <v-col
          v-for="AAName in nameSet"
          :key="Object.keys(AAName)[0]"
          >
          <v-tooltip top>
             <template v-slot:activator="{ on }">
              <v-card
                outlined
                class="grey1 rounded-card"

                flat
                v-on="on">
                <v-card-subtitle class="text-center py-2">
                  {{ getAcronym(Object.values(AAName)[0]) }}
                </v-card-subtitle>
              </v-card>
            </template>
            <span>{{ Object.values(AAName)[0] }}</span>
          </v-tooltip>
        </v-col>
        <v-col :cols="1">
          <v-container class="pa-0 pt-1 d-flex">
            <v-spacer />
            <AANameConfig
              v-if="canEdit"
              :RPAANames="RPAANames"/>
          </v-container>
        </v-col>
      </v-row>
      <v-form
        @submit.prevent="onSubmit"
        ref="mainForm">
        <v-row
          v-for="profile in riskProfiles"
          :key="profile.id"
          dense

          >
          <v-col
            :cols="2">
            <v-text-field
              :style="checkColor(profile) "
              class="rounded-card small-text-9em"
              :error ="!checkComplete(profile)"
              @change="addToChanged(profile)"
              v-model="profile.name"
              dense outlined
              :rules="[v => !!(v) || 'Must enter a name']"
              validate-on-blur
              hide-details="auto"
              :read-only="!canEdit">
              <template
                v-if="checkHint(profile)"
                v-slot:append>
                <v-tooltip
                  bottom
                >
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" color="red">
                      mdi-alert-rhombus-outline
                    </v-icon>
                  </template>
                  {{ checkHint(profile)}}
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col
            v-for="AAName in nameSet"
            :key="Object.keys(AAName)[0]"
          >
              <v-text-field
                :style='checkColor(profile)'
                :error ="!checkComplete(profile)"
                :disabled="!canEdit"
                @change="addToChanged(profile)"
                :value = "getAAPercentage(AAName,profile)"
                @blur = "setAAPercentage($event.target.value, AAName, profile)"
                class="allocationNumber rounded-card"
                type="number"
                outlined dense hide-details/>
          </v-col>
          <v-col
            :cols="1"
            >
            <v-container class="pa-0 pt-1 d-flex">
              <v-spacer />
              <v-btn icon>
                <DeleteObj
                  v-if="canEdit"
                  :objectType="'riskprofile'"
                  :objectToDelete="profile"
                  :shownRP="shownRP"
                  @delete-object="deleteRP"
                  v-on="$listeners"
                  :color="'primary'"
                />
              </v-btn>
            </v-container>
          </v-col>
        </v-row>
      </v-form>
      <v-form
        @submit.prevent="onSubmit"
        ref="addForm">
        <v-row v-if="canEdit && !_.isEmpty(shownRPObject)"
          dense>
          <v-col
            :cols="2">
              <v-text-field
                class="rounded-card"
                v-model="newRP.name"
                outlined dense
                :rules="[v => !!(v) || 'Must enter a name']"
                validate-on-blur
                hide-details="auto"/>
          </v-col>
          <v-col
            v-for="AAName in nameSet"
            :key="Object.keys(AAName)[0]">
              <v-text-field
                class="rounded-card allocationNumber"
                type="number"
                v-model="newRP.allocations[Object.keys(AAName)[0]]"
                outlined dense hide-details/>
          </v-col>
          <v-col
            :cols="1">
            <v-container class="pa-0 pt-1 d-flex">
              <v-spacer />
              <v-btn type="button" color="primary" dark dense
                @click="addRP" icon>
                <v-icon>
                  mdi-plus-circle
                </v-icon>
              </v-btn>
            </v-container>
          </v-col>
        </v-row>
      </v-form>
      <v-divider class="mt-4" v-if="!_.isEmpty(shownRPObject)" />
      <v-row v-if="riskProfiles.length && canEdit">
        <v-col class="text-right">
          <v-btn @click="onSubmit" class="primary-action-button" >Update All</v-btn>
        </v-col>
      </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AANameConfig from "@/components/AANameConfig.vue";
import DeleteObj from "@/components/DeleteObj.vue";
import AddRPGroup from "@/components/AddRPGroup.vue";
import WithoutWatchers from "@/components/mixins/WithoutWatchers.js";

import { mapGetters } from "vuex";
import {
  USER_UPDATE
} from "@/store/actions.type";
import {
  SET_ACTIVE_USER_PROP
} from "@/store/mutations.type";

export default {
  name: "RiskProfileTable",
  mixins: [WithoutWatchers],
  props: {
    riskProfileGroups: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      activeSwitch: false,
      newGroupName: "",
      editGroupName: false,
      riskProfiles: [],
      RPAANames: [],
      error: null,
      shownRP: null,
      changeList: [],
      newRP: {
        name:"",
        order:null,
        allocations:{},
      },
    };
  },
  components: {
    AANameConfig,
    DeleteObj,
    AddRPGroup,

  },
  computed: {
    ...mapGetters(["activeUser"]),
    lockMessage() {
      let msg = '';
      if (!this.isNotAFSLLimited) {
        msg += 'You cannot edit AFSL Risk Profiles'
      }
      else if (!this.isPracticeAdmin) {
        msg += 'You are not an admin of this Practice'
      }
      return msg
    },
    canEdit() {
      if (this.isPracticeAdmin && this.isNotAFSLLimited && this.isNotDefaultTemplate ) {
        return true
      } else {
        return false
      }
    },
    isPracticeAdmin() {
      if (this.riskProfileGroups && this.shownRP && this.shownRPObject.id) {
        if (this.shownRPObject.active_practices.length > 0) {
          return this.shownRPObject.active_practices.some(item => this.activeUser.admin_practices.includes(item));
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isNotDefaultTemplate() {
      if (this.riskProfileGroups && this.shownRP) {
        if (this.shownRPObject.template && this.shownRPObject.default) {
          return false
        } else {
          return true
        }
      } else {
        return true
      }
    },
    isNotAFSLLimited() {
      if (this.riskProfileGroups && this.shownRP) {
        if (this._.isEmpty(this.shownRPObject.afsls)) {
          return true
        } else {
          return false
        }
      } else {
        return true
      }
    },
    shownRPObject() {
      if (this.riskProfileGroups && this.shownRP) {
          const i = this.riskProfileGroups.findIndex(item => item.id == this.shownRP);
          if (i != -1) {
            //The id is added to the array before the group data comes back from
            // Profile view, so this avoids errors while it comes in.
            return this.riskProfileGroups[i];
          } else {
            return {}
          }
      } else {
        return {}
      }
    },
    nameSet: function (){
      let AANameList = [];
      let checkList = []
      for (let i = 0; i < this.RPAANames.length; i++) {
        let found = false;
        let aaName = this.RPAANames[i];
          if (checkList.includes(aaName.custom_name)) {
            found = true;
          }
          if (!found) {
            let newAA = {};
            newAA[aaName.id] = aaName.custom_name;
            AANameList.push(newAA);
            found = false;
            checkList.push(aaName.custom_name);
          }
      }
      return (AANameList)
    },
    selectedIsActive() {
      if (this.shownRP) {
        if (this.shownRP === this.activeUser.active_rp) {
          return true;
        } else {
          return false;
        }
      } else {
        return false
      }
    },
  },
  watch: {
    shownRP: function () {
      this.setActiveSwitch()
      this.getRPAANameData();
      this.getRiskProfiles();
      this.changeList = [];
    },
    activeSwitch: function () {
      this.setActiveRP()
    },
  },
  methods: {
    setActiveSwitch() {
      this.$withoutWatchers(() => {
        if (this.selectedIsActive) {
          this.activeSwitch = true;
        } else {
          this.activeSwitch = false;
        }
      })
    },
    getAcronym(n) {
      // returns the first letters of each word in name as an abbreviation
      if (n) {
        let matches = n.match(/\b(\w)/g);
        let acronym = matches.join('');
        return acronym
      } else {
        return n
      }
    },
    checkHint(profile) {
      if (!this.checkComplete(profile)) {
        return "Allocations do not equal 100%"
      }
    },
    checkColor(profile){
      if (!this.checkComplete(profile)) {
        return ({
          backgroundColor: '#ffebee',
        })
      }
    },
    checkComplete(profile) {
      if (profile.allocations) {
        let value = profile.allocations.reduce( function (a,b) {
          return parseFloat(a) + parseFloat(b.percentage);
        }, 0);
        if (value.toFixed(4) === '1.0000') {
          return true
        } else {
          return false
        }
      } else {
        return false
      }
    },
    updateGroupName(){
      this.editGroupName = !this.editGroupName;
      if (this.newGroupName != '') {
        let endpoint = `/api/riskprofilegroups/${this.shownRPObject.id}/`;
        apiService(endpoint, "PATCH", {
          name: this.newGroupName,
        }).then(data => {
          this.$emit('update-rpgroup', data);
          this.newGroupName = "";
        })
      }
    },
    deleteRP(data) {
      // Removes item from the riskprofiles list
      const removeItem = this.riskProfiles.findIndex(i => i.id === data.id);
      if (removeItem) {
        this.$delete(this.riskProfiles, removeItem);
      }
      // Removes item from the changed list (if it's in it)
      const removeFromChanged = this.changeList.findIndex(i => i.id === data.id);
      if (removeFromChanged >= 0) {
        this.$delete(this.changeList, removeFromChanged);
      }
    },
    deleteRPGroup(data) {
      this.$emit('delete-rpgroup', data);
      this.riskProfiles = [];
    },
    setActiveRP() {
      let setActive = null;
      if (this.activeSwitch) {
        setActive = this.shownRP;
      }
      this.$store.commit(SET_ACTIVE_USER_PROP, {
        'prop': 'active_rp',
        'value': setActive
      })
      this.$store.dispatch(USER_UPDATE);
    },
    addRPGroup(data){
      this.$emit('add-rpgroup')
      this.shownRP = data.id;
    },
    addToChanged(profile) {
      if (!(this.changeList.includes(profile))) {
        this.changeList.push(profile);
      } else {
        const i = this.changeList.findIndex(item => item.id === profile.id);
        this.changeList.splice(i, 1);
        this.changeList.push(profile);
      }
    },
    setAAPercentage(event, AAName, riskProfile) {
      // Gets the key of the aaname item (the key is the id)
      const aaID = Object.keys(AAName)[0];
      let found = false;
      // Iterates the risk profile allocations and attempts to find and item
      // with a matching name_id
      for (let allocation of riskProfile.allocations){
        found = false;
          // If it is found, assign, break the loop and change found var
          if (allocation.name.id.toString() === aaID) {
            allocation.percentage = (event/100).toFixed(4);
            found = true;
            break;
          }
      }
      // If not found, create a new allocation object and add to the RP.
      if (!found) {
        let newAllocation = {}
        newAllocation.name = {}
        newAllocation.name.id = aaID;
        newAllocation.percentage = (event/100).toFixed(4);
        newAllocation.riskprofile = riskProfile.id;
        newAllocation.id = null;
        riskProfile.allocations.push(newAllocation);
      }
    },
    getAAPercentage(AAName, riskProfile) {
      let total = 0
      for (let i=0; i < riskProfile.allocations.length; i++) {
        // Test if the custom_name for the risk profile matches the columm header
        if (riskProfile.allocations[i].name.custom_name === Object.values(AAName)[0]) {
          let percentage = Number(riskProfile.allocations[i].percentage)
          if (percentage > 0) {
            // Add percentages together for merged RP AA names
            total += percentage;
          }
        }
      }
      return (total*100).toFixed(2)
    },
    getRiskProfiles() {
      if (this.shownRP) {
        let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/`;
        apiService(endpoint).then(data => {
          this.riskProfiles = data.results;
        });
      }
    },
    getRPAANameData() {
      if (this.shownRP) {
        let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofilenames/`;
        apiService(endpoint).then(data => {
          this.RPAANames = data.results;
        });
      }
    },
    addRP() {
      // validates the last row (the add row)
      if (this.$refs.addForm.validate()){
        let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/`;
        apiService(endpoint, "POST", {
          name: this.newRP.name,
          group: this.shownRP,
          order: this.newRP.order,
        }).then(data => {
          this.addAA(data.id);
        });

      }
    },
    addAA(id) {
      if (this._.isEmpty(this.newRP.allocations)) {
        this.getRiskProfiles();
        this.newRP.name="";
        this.newRP.order=null;
      } else {
        for (const [key, value] of Object.entries(this.newRP.allocations)) {
          let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/${id}/aa/`;
          apiService(endpoint, "POST", {
            name_id: key,
            percentage: value/100,
            riskprofile: id
          }).then(() => {
            this.getRiskProfiles();
            this.newRP.name="";
            this.newRP.order=null;
            this.newRP.allocations = {};
          });
        }
      }
    },
    onSubmit() {
      // If there is a new item in the add row, add it too.
      if (!this._.isEmpty(this.newRP.name)) {
        this.addRP();
      }
      if (this.$refs.mainForm.validate()){
        if (this.changeList) {
          for (let i=0; i < this.changeList.length; i++) {
            let endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/${this.changeList[i].id}/`;
            apiService(endpoint, "PATCH", {
              name: this.changeList[i].name,
              group: this.changeList[i].group,
              order: this.changeList[i].order,
            }).then(data => {
              this.updateAA(data.id, this.changeList[i]);
            });
          };
        };
      }
    },
    updateAA(profileID, profile) {
      for (let i=0; i < profile.allocations.length; i++) {
        let endpoint = '';
        let method = '';
        if (profile.allocations[i].id === null) {
          endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/${profileID}/aa/`;
          method = "POST"
        } else {
          endpoint = `/api/riskprofilegroups/${this.shownRP}/riskprofiles/${profileID}/aa/${profile.allocations[i].id}/`;
          method = "PATCH"
        };
        apiService(endpoint, method, {
          id: profile.allocations[i].id,
          name_id: profile.allocations[i].name.id,
          percentage: profile.allocations[i].percentage,
          riskprofile: profileID
        }).then(() => {
          this.getRiskProfiles();
          this.changeList=[];
        });
      };
    }
  },
  mounted() {
    this.shownRP = this.activeUser.active_rp;
    this.getRPAANameData();
    this.getRiskProfiles();
  }
};
</script>
<style >
/* .header-card {
  border: 1px solid  !important
} */
.allocationNumber input[type='number'] {
  -moz-appearance:textfield;
}
.allocationNumber input::-webkit-outer-spin-button,
.allocationNumber input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
.allocationNumber input {
  font-size: .8rem;
  text-align: center !important;
}
.small-text-9em {
  font-size: .9rem !important;
}
.error-styling  {
  background-color: #ffebee;

}


</style>
