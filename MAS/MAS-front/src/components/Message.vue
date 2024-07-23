<template>
  <div :class="['message', sender]">
    <img :src="getAvatar(sender)" class="avatar" />
    <span class="message-text">{{ text }}</span>
  </div>
</template>

<script>
export default {
  name: 'ChatMessage',
  props: {
    text: String,
    sender: String,
  },
  methods: {
    getAvatar(sender) {
      if (sender === 'user') {
        return '/icons/用户.png';
      } else {
        return '/icons/Bot.png';
      }
    },
  },
};
</script>

<style scoped>
.message {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}

.message.user {
  flex-direction: row-reverse;
  background-color: #409eff;
  color: white;
  text-align: right;
}

.message.bot {
  flex-direction: row;
  background-color: #f1f1f1;
  color: black;
  text-align: left;
}

.message .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
}

.message-text {
  max-width: 70%;
  word-wrap: break-word;
}
</style>
