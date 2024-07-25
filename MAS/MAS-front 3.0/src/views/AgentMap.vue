<template>
    <Chatbot/>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';

import Chatbot from '@/components/Chatbot/Chatbot.vue'; // 更新路径以确保正确导入

@Component({
    components: {
        Chatbot
    }
})
export default class AgentMap extends Vue {

}
</script>