<script setup>
import inBalanceButton from "@/components/buttons/inBalanceButton.vue";
import outBalanceButton from "@/components/buttons/outBalanceButton.vue";
import transBalanceButton from "@/components/buttons/transBalanceButton.vue";
import adminButton from "@/components/buttons/adminButton.vue";
components: {
  inBalanceButton, outBalanceButton, transBalanceButton, adminButton;
}
</script>

<template>
  <inBalanceButton />
  <outBalanceButton />
  <transBalanceButton />
  <adminButton />
</template>
<style scoped></style>
