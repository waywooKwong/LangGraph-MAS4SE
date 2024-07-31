<template>
  <div :class="['message', sender]">
    <img :src="getAvatar(sender)" class="avatar" />

    <div class="message-bubble">
      {{ text }}
    </div>
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
  /* background-color: #409eff; */
  /* color: white; */
  text-align: right;
}

.message.bot {
  flex-direction: row;
  /* background-color: #f1f1f1; */
  /* color: black; */
  text-align: left;
}

.message .avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin: 0 10px;
 
}

.message-bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  background-color: #f1f1f1;
}

.message.user .message-bubble {
 
  background-color: #75afec;
  color: #fff4f4;
  border-bottom-right-radius: 0;
}

.message.bot .message-bubble {
  
  background-color: #f6da87;
  color: #7853B2;
  border-bottom-left-radius: 0;
}
</style>
