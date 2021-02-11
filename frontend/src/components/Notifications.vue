<template lang="html">
  <v-menu
    :close-on-content-click="false"
    offset-y
    max-width="400px"
    >
    <template v-slot:activator="{ on }">
      <v-btn class="ml-6" small icon v-on="on" @click="setAsRead">
        <v-badge
          :value="numNotifications != null"
          :content="numNotifications"
          overlap >
          <v-icon >mdi-bell-outline</v-icon>
        </v-badge>
      </v-btn>
    </template>
    <v-card>
      <template
        v-for="(notification,index) in lastThreeNotifications">
        <v-container :key="notification.id" class="pa-0">
          <v-list three-line class="pb-0">
            <v-list-item>
              <v-list-item-content >
                <v-list-item-title>{{notification.title}}</v-list-item-title>
                <v-list-item-subtitle>{{notification.content}}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <template v-if="notification.type==='practice_invite'">
            <v-list  class="pa-0">
              <v-list-item  >
                <v-list-item-action>
                  <v-switch v-model="notification.active_practice" color="teal"></v-switch>
                </v-list-item-action>
                <v-list-item-title>Set as active practice</v-list-item-title>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-spacer />
              <v-btn text @click="denyNotification(notification)">Ignore</v-btn>
              <v-btn color="primary" text @click="acceptNotification(notification)">Accept Invitation</v-btn>
            </v-card-actions>
          </template>
          <template v-if="notification.type=='scenario_share'">
            <v-card-actions>
              <v-spacer />
              <v-btn text @click="denyNotification(notification)">Got it</v-btn>
            </v-card-actions>
          </template>
          <v-divider v-if="index < (notifications.length-1)" />
        </v-container>
      </template>
    </v-card>
  </v-menu>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { mapGetters } from "vuex";
import {
  PRACTICE_INVITE_ACCEPT
} from "@/store/actions.type";

export default {
  props: {
  },
  data() {
    return {
      notifications: null,
      active_practice: true,
    }
  },
  computed: {
    ...mapGetters(["activeUser"]),
    visibleNotifications() {
      if (this.notifications) {
        return this.notifications.filter(i => i.visible == true)
      } else {
        return []
      }
    },
    lastThreeNotifications() {
      return this.visibleNotifications.slice(0,3)
    },
    unreadNotifications() {
      return this.visibleNotifications.filter(i => i.read == false)
    },
    numNotifications() {
      if (this.unreadNotifications.length > 0) {
        return this.unreadNotifications.length
      } else {
        return null
      }
    }
  },
  methods: {
    getNotifications() {
      let endpoint = "/api/notifications/";
      apiService(endpoint).then(data => {
        this.notifications = data.results;
      });
    },
    denyNotification(notification){
      this.setInvisible(notification)
    },
    acceptNotification(notification) {
      this.setInvisible(notification);
      if (notification.type == 'practice_invite'){
        this.acceptPracticeInvite(notification);
      }
    },
    acceptPracticeInvite(notification) {
      this.$store.dispatch(PRACTICE_INVITE_ACCEPT, notification)
    },
    setAsRead() {
      let ids = []
      for (let item of this.unreadNotifications) {
        ids.push(item.id);
      }
      for (let id of ids) {
        let result = this.notifications.find(i => i.id === id)
        result.read = true;
        let endpoint = `/api/notifications/${id}/`;
        apiService(endpoint, "PATCH", {
          read: true,
        });
      }
    },
    setInvisible(notification) {
      let endpoint = `/api/notifications/${notification.id}/`;
      apiService(endpoint, "PATCH", {
        visible: false,
      }).then(data => {
        this.$set(notification,'visible', data.visible);
      });
    }
  },
  mounted() {
    this.getNotifications();
  }
}
</script>

<style lang="css" scoped>
</style>
